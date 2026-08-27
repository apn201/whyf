"""infra/config.yaml, loaded once.

Everything that differs between accounts, regions and deploys lives in that
file. Nothing else in the codebase names a model id or a region, which is what
made switching from Frankfurt to Ireland a one-line change.
"""
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from .limits import Limits

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_PATH = ROOT / "infra" / "config.yaml"


@dataclass(frozen=True)
class Config:
    region: str = "eu-west-1"
    table_name: str = "whyf"
    search_key_parameter: str = "/whyf/search-api-key"

    classifier_model: str = ""
    synthesiser_model: str = ""
    tier2_enabled: bool = True
    embedding_model: str = ""
    embedding_dimensions: int = 1024
    tier1_shortlist: int = 15

    limits: Limits = field(default_factory=Limits)

    @property
    def embeddings_enabled(self) -> bool:
        """Empty embedding model is a supported state, not a broken one. It is
        what the degraded path looks like when the daily ceiling is hit."""
        return bool(self.embedding_model)


@lru_cache(maxsize=4)
def load(path=None) -> Config:
    """Environment beats the file, so a Lambda can override without a redeploy."""
    path = Path(path or os.environ.get("WHYF_CONFIG") or DEFAULT_PATH)
    data = {}
    if path.exists():
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    models = data.get("models") or {}
    limit_data = data.get("limits") or {}
    known = {f for f in Limits.__dataclass_fields__}

    return Config(
        region=os.environ.get("WHYF_REGION") or data.get("region") or "eu-west-1",
        table_name=os.environ.get("WHYF_TABLE") or data.get("table_name") or "whyf",
        search_key_parameter=data.get("search_key_parameter")
        or "/whyf/search-api-key",
        classifier_model=os.environ.get("WHYF_CLASSIFIER")
        or models.get("classifier") or "",
        synthesiser_model=os.environ.get("WHYF_SYNTHESISER")
        or models.get("synthesiser") or "",
        tier2_enabled=str(os.environ.get("WHYF_TIER2", "")).lower() not in
        ("0", "false", "off"),
        embedding_model=os.environ.get("WHYF_EMBEDDING")
        or models.get("embedding") or "",
        embedding_dimensions=int(models.get("embedding_dimensions") or 1024),
        tier1_shortlist=int(data.get("tier1_shortlist") or 15),
        limits=Limits(**{k: v for k, v in limit_data.items() if k in known}),
    )
