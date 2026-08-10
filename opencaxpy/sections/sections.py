from dataclasses import dataclass
@dataclass(frozen=True)
class TrussSection:
    area: float
@dataclass(frozen=True)
class BeamSection:
    area: float
    iy: float=0.0
    iz: float=0.0
    j: float=0.0
    kappa_y: float=5/6
    kappa_z: float=5/6
