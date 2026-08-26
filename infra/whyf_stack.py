"""The whole deployment. One table, one function, one URL.

Deliberately small. There is no API Gateway, no VPC, no NAT, no OpenSearch and
no container image, because none of them earn their place for a public demo
that answers one question at a time. The interesting engineering in this
project is in the tier system and the knowledge, not in the topology.

Least privilege here is not decoration. If the agent is ever prompt-injected
through a fetched web page, the blast radius is one cache write.
"""
import pathlib

import yaml
from aws_cdk import (
    CfnOutput, Duration, RemovalPolicy, Stack,
)
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_logs as logs
from constructs import Construct

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "build" / "lambda"


def load_config():
    data = yaml.safe_load((ROOT / "infra" / "config.yaml").read_text(
        encoding="utf-8")) or {}
    return data


class WhyfStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        config = load_config()
        models = config.get("models") or {}
        limits = config.get("limits") or {}
        profile_regions = config.get("inference_profile_regions") or [self.region]

        if not BUNDLE.exists():
            raise FileNotFoundError(
                "no bundle at build/lambda. Run: python tools/build_lambda.py")

        # ---- one table: cache, and the daily spend counter -----------------
        table = dynamodb.Table(
            self, "Table",
            table_name=config.get("table_name", "whyf"),
            partition_key=dynamodb.Attribute(
                name="PK", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(
                name="SK", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute="ttl",
            # It is a cache and a counter. Nothing in it is worth keeping, and
            # a retained table is a bill after judging ends.
            removal_policy=RemovalPolicy.DESTROY,
        )

        # ---- the runtime role ---------------------------------------------
        role = iam.Role(
            self, "AgentRole",
            role_name="WhyFAgentRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Runtime role for the WHY THE F agent. Read the "
                        "policies: this is the part of the repo that should be "
                        "checked, not the diagram.",
        )

        role.add_to_policy(iam.PolicyStatement(
            sid="Logs",
            actions=["logs:CreateLogGroup", "logs:CreateLogStream",
                     "logs:PutLogEvents"],
            resources=["arn:aws:logs:{}:{}:log-group:/aws/lambda/whyf-*:*".format(
                self.region, self.account)],
        ))

        # A cross-region inference profile can route to any region in the
        # profile, so the policy has to name the foundation models in all of
        # them, not just the one this stack is deployed to. This is the line
        # everybody gets wrong once.
        bedrock_resources = []
        for region in profile_regions:
            bedrock_resources.append(
                "arn:aws:bedrock:{}::foundation-model/*".format(region))
        bedrock_resources.append(
            "arn:aws:bedrock:{}:{}:inference-profile/*".format(
                self.region, self.account))

        role.add_to_policy(iam.PolicyStatement(
            sid="BedrockInvoke",
            actions=["bedrock:InvokeModel",
                     "bedrock:InvokeModelWithResponseStream"],
            resources=bedrock_resources,
        ))

        # No DeleteItem, no Scan. The agent writes cache entries and bumps a
        # counter; it has no reason to be able to remove anything or to read
        # the whole table.
        role.add_to_policy(iam.PolicyStatement(
            sid="CacheAndCounter",
            actions=["dynamodb:GetItem", "dynamodb:PutItem",
                     "dynamodb:UpdateItem"],
            resources=[table.table_arn],
        ))

        # Created explicitly so the retention is part of the stack rather than
        # applied afterwards by a custom resource, which is what the deprecated
        # log_retention property does.
        log_group = logs.LogGroup(
            self, "AgentLogs",
            log_group_name="/aws/lambda/whyf-agent",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # ---- the function ---------------------------------------------------
        function = lambda_.Function(
            self, "Agent",
            function_name="whyf-agent",
            runtime=lambda_.Runtime.PYTHON_3_12,
            architecture=lambda_.Architecture.X86_64,
            handler="whyf.handler.handler",
            code=lambda_.Code.from_asset(str(BUNDLE)),
            role=role,
            # Cold start loads 80 cards and 80 embedding vectors. More memory
            # buys proportionally more CPU, which is what actually shortens it.
            memory_size=1536,
            timeout=Duration.seconds(60),
            log_group=log_group,
            environment={
                "WHYF_REGION": self.region,
                "WHYF_TABLE": table.table_name,
                "WHYF_CLASSIFIER": models.get("classifier", ""),
                "WHYF_SYNTHESISER": models.get("synthesiser", ""),
                "WHYF_EMBEDDING": models.get("embedding", ""),
                "WHYF_DAILY_CEILING": str(
                    limits.get("daily_model_call_ceiling", 2000)),
                "PYTHONUNBUFFERED": "1",
            },
        )

        url = function.add_function_url(
            # Public and unauthenticated on purpose. The submission rules
            # require the demo to be reachable and free until judging ends, and
            # the agent holds nothing about anybody: there is no session, no
            # account and nothing to protect behind a login.
            auth_type=lambda_.FunctionUrlAuthType.NONE,
            cors=lambda_.FunctionUrlCorsOptions(
                allowed_origins=["*"],
                allowed_methods=[lambda_.HttpMethod.POST],
                allowed_headers=["content-type"],
                max_age=Duration.hours(1),
            ),
        )

        CfnOutput(self, "DemoUrl", value=url.url,
                  description="POST {\"question\": \"...\"} here")
        CfnOutput(self, "TableName", value=table.table_name)
        CfnOutput(self, "LogGroup",
                  value="/aws/lambda/" + function.function_name)
