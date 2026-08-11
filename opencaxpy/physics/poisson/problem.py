from dataclasses import dataclass


@dataclass
class PoissonPhysics:
    diffusion: object = 1.0
    source: object = 0.0
