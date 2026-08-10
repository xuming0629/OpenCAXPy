from dataclasses import dataclass, field
import numpy as np
@dataclass
class FieldResult:
    name: str
    values: np.ndarray
    location: str="node"
    components: int=1

@dataclass
class Result:
    solution: np.ndarray|None=None
    reaction: np.ndarray|None=None
    fields: dict=field(default_factory=dict)
    metadata: dict=field(default_factory=dict)
    def add_field(self,name,values,location="node",components=1):
        self.fields[name]=FieldResult(name,np.asarray(values),location,components)
        return self.fields[name]
    def field(self,name): return self.fields[name]
