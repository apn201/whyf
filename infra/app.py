#!/usr/bin/env python3
"""CDK entry point.

    python tools/build_lambda.py
    cd infra && npx cdk deploy --profile whyf

Account comes from the profile at synth time and is never written down. Region
comes from infra/config.yaml, which is the single place this project names one.
"""
import os
import pathlib

import aws_cdk as cdk
import yaml

from whyf_stack import WhyfStack

ROOT = pathlib.Path(__file__).resolve().parent.parent
config = yaml.safe_load((ROOT / "infra" / "config.yaml").read_text(
    encoding="utf-8")) or {}

app = cdk.App()
WhyfStack(
    app, "WhyfStack",
    stack_name="whyf",
    env=cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=config.get("region") or os.environ.get("CDK_DEFAULT_REGION"),
    ),
    description="WHY THE F - explains one supplier security questionnaire row",
)
app.synth()
