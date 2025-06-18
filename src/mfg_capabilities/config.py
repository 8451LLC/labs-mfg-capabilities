import os
from dataclasses import dataclass, fields, field
from pathlib import Path
from typing import Any, Optional, Dict

from langchain_core.runnables import RunnableConfig
import pyprojroot

PROJECT_ROOT = pyprojroot.here()


@dataclass(kw_only=True)
class Configuration:
    """The configurable fields for the chatbot."""

    # Model
    default_provider: str = "openai"
    default_model: str = "gpt-4o"
    default_model_kwargs: Optional[Dict[str, Any]] = field(default_factory=dict)

    # Data
    data_dir: Path = PROJECT_ROOT / "data"

    @classmethod
    def from_runnable_config(
        cls,
        config: Optional[RunnableConfig] = None,
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig.

        For each field in the dataclass, this method attempts to resolve its value
        from two sources, in order:

        1. Environment variable: Looks for an environment variable whose name
           matches the field name uppercased (e.g., for a field 'default_llm',
           it looks for 'DEFAULT_LLM').
        2. Configurable dict: If the environment variable is not set, it looks for
           the value in the 'configurable' dictionary (which is typically passed at
           runtime in LangGraph as part of the config).

        Only fields with a value (not None or empty) are passed to the constructor.
        This allows you to flexibly configure your dataclass from either environment
        variables or a runtime config dictionary, with environment variables taking
        precedence. If neither is set, the dataclass default will be used.
        """
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})


config = Configuration()
