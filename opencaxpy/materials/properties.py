from dataclasses import dataclass
@dataclass(frozen=True)
class MechanicalProperties:
    E: float; nu: float; density: float=0.0
    @property
    def G(self): return self.E/(2*(1+self.nu))
@dataclass(frozen=True)
class ThermalProperties:
    conductivity: float; heat_capacity: float=0.0; density: float=0.0
@dataclass(frozen=True)
class FluidProperties:
    density: float; viscosity: float
@dataclass(frozen=True)
class ElectromagneticProperties:
    permittivity: float=1.0; permeability: float=1.0; conductivity: float=0.0
