from __future__ import annotations
import numpy as np
from ..connectivity import CSRConnectivity
from .utils import build_unique_entities, build_node_to_cell, build_node_to_node, build_cell_adjacency, boundary_edge_ids_from_boundary_faces

class BaseTopology:
    local_edges=()
    local_faces=None
    def __init__(self,mesh): self.mesh=mesh; self.backend=mesh.backend; self._built=False
    def _array(self,data): return self.backend.asarray(data,device=self.mesh.device)
    def build(self):
        if self._built: return self
        cells=self.backend.to_numpy(self.mesh.cells).astype(np.int64,copy=False)
        edges,c2e,eoff,eowners,ecounts=build_unique_entities(cells,self.local_edges)
        noff,ncells=build_node_to_cell(self.mesh.num_nodes,cells)
        nnoff,nnidx=build_node_to_node(self.mesh.num_nodes,edges)
        self.edges=self._array(edges); self.cell_to_edge=self._array(c2e)
        self.edge_to_cell=CSRConnectivity(self._array(eoff),self._array(eowners))
        self.node_to_cell=CSRConnectivity(self._array(noff),self._array(ncells))
        self.node_to_node=CSRConnectivity(self._array(nnoff),self._array(nnidx))
        self.faces=self.cell_to_face=self.face_to_cell=self.boundary_face_ids=None
        aoff,aowners=eoff,eowners
        if self.local_faces is not None:
            faces,c2f,foff,fowners,fcounts=build_unique_entities(cells,self.local_faces)
            self.faces=self._array(faces); self.cell_to_face=self._array(c2f)
            self.face_to_cell=CSRConnectivity(self._array(foff),self._array(fowners))
            self.boundary_face_ids=self._array(np.flatnonzero(fcounts==1))
            self.boundary_edge_ids=self._array(boundary_edge_ids_from_boundary_faces(edges,faces[fcounts==1]))
            aoff,aowners=foff,fowners
        else:
            self.boundary_edge_ids=self._array(np.flatnonzero(ecounts==1))
        ccoff,ccidx=build_cell_adjacency(self.mesh.num_cells,aoff,aowners)
        self.cell_to_cell=CSRConnectivity(self._array(ccoff),self._array(ccidx))
        self._built=True; return self
    @property
    def num_edges(self): self.build(); return int(self.edges.shape[0])
    @property
    def num_faces(self): self.build(); return 0 if self.faces is None else int(self.faces.shape[0])
    @property
    def boundary_edges(self): self.build(); return self.edges[self.boundary_edge_ids]
    @property
    def boundary_faces(self):
        self.build()
        if self.faces is None: raise ValueError('This topology does not define 3D faces')
        return self.faces[self.boundary_face_ids]
    @property
    def boundary_nodes(self):
        self.build(); ents=self.backend.to_numpy(self.boundary_faces if self.faces is not None else self.boundary_edges)
        return self._array(np.unique(ents.reshape(-1)))
    def summary(self):
        self.build(); return {'topology':type(self).__name__,'num_nodes':self.mesh.num_nodes,'num_edges':self.num_edges,'num_faces':self.num_faces,'num_cells':self.mesh.num_cells,'num_boundary_edges':int(self.boundary_edges.shape[0]),'num_boundary_faces':0 if self.faces is None else int(self.boundary_faces.shape[0]),'num_boundary_nodes':int(self.boundary_nodes.shape[0])}
