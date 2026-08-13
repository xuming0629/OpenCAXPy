from __future__ import annotations
from dataclasses import dataclass, field
from .field import Field


@dataclass
class Solution:
    """Backend-independent numerical solution/result container."""
    fields: dict[str, Field] = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def add_field(self, field: Field):
        self.fields[field.name] = field
        return self

    def __getitem__(self, name: str) -> Field:
        return self.fields[name]

    def get(self, name: str, default=None):
        return self.fields.get(name, default)
