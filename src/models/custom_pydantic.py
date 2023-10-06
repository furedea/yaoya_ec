"""Define custom pydantic models."""
from pydantic import BaseModel, ConfigDict


class FrozenBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        validate_default=True,
        frozen=True,
        arbitrary_types_allowed=True
    )
