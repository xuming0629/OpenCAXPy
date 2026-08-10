from dataclasses import dataclass
@dataclass
class Material:
    name: str
    mechanical: object|None=None
    thermal: object|None=None
    fluid: object|None=None
    electromagnetic: object|None=None
