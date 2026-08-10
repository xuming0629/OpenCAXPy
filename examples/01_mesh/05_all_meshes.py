from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from opencaxpy import (
    IntervalMesh,
    TriangleMesh,
    QuadrangleMesh,
    TetrahedronMesh,
    HexahedronMesh,
)

meshes = [
    IntervalMesh.from_interval((0,1),4),
    TriangleMesh.from_box((0,1,0,1),2,2),
    QuadrangleMesh.from_box((0,1,0,1),2,2),
    TetrahedronMesh.from_box(),
    HexahedronMesh.from_box((0,1,0,1,0,1),1,1,1),
]

for mesh in meshes:
    print("="*72)
    for key, value in mesh.summary().items():
        print(f"{key:24s} = {value}")
