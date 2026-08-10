from dataclasses import dataclass, field
@dataclass
class Model:
    geometry: object|None=None
    mesh: object|None=None
    materials: dict=field(default_factory=dict)
    sections: dict=field(default_factory=dict)
    regions: dict=field(default_factory=dict)
