from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np

from .vtk_converter import VtkConverter


def _format_array(array) -> str:
    return " ".join(str(value) for value in np.asarray(array).reshape(-1))


class VtkExporter:
    @staticmethod
    def write(mesh, filename):
        path = Path(filename)
        if path.suffix.lower() != ".vtu":
            path = path.with_suffix(".vtu")

        arrays = VtkConverter.arrays(mesh)

        point_data = []
        for name, values in mesh.point_data.items():
            data = mesh.backend.to_numpy(values)
            components = 1 if data.ndim == 1 else data.shape[1]
            point_data.append(
                f'<DataArray type="Float64" Name="{escape(name)}" '
                f'NumberOfComponents="{components}" format="ascii">'
                f'{_format_array(data)}</DataArray>'
            )

        cell_data = []
        for name, values in mesh.cell_data.items():
            data = mesh.backend.to_numpy(values)
            components = 1 if data.ndim == 1 else data.shape[1]
            cell_data.append(
                f'<DataArray type="Float64" Name="{escape(name)}" '
                f'NumberOfComponents="{components}" format="ascii">'
                f'{_format_array(data)}</DataArray>'
            )

        xml = "\n".join([
            '<?xml version="1.0"?>',
            '<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">',
            '  <UnstructuredGrid>',
            f'    <Piece NumberOfPoints="{mesh.num_nodes}" NumberOfCells="{mesh.num_cells}">',
            f'      <PointData>{"".join(point_data)}</PointData>',
            f'      <CellData>{"".join(cell_data)}</CellData>',
            '      <Points>',
            f'        <DataArray type="Float64" NumberOfComponents="3" format="ascii">{_format_array(arrays["points"])}</DataArray>',
            '      </Points>',
            '      <Cells>',
            f'        <DataArray type="Int64" Name="connectivity" format="ascii">{_format_array(arrays["connectivity"])}</DataArray>',
            f'        <DataArray type="Int64" Name="offsets" format="ascii">{_format_array(arrays["offsets"])}</DataArray>',
            f'        <DataArray type="UInt8" Name="types" format="ascii">{_format_array(arrays["cell_types"])}</DataArray>',
            '      </Cells>',
            '    </Piece>',
            '  </UnstructuredGrid>',
            '</VTKFile>',
            '',
        ])

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(xml, encoding="utf-8")
        return path
