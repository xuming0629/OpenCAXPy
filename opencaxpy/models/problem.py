from dataclasses import dataclass, field


@dataclass
class Problem:
    model: object
    physics: list = field(default_factory=list)
    fields: dict = field(default_factory=dict)
    boundary_conditions: list = field(default_factory=list)
    loads: list = field(default_factory=list)
    initial_conditions: list = field(default_factory=list)

    def add_field(self, field):
        self.fields[field.name] = field
        return field
