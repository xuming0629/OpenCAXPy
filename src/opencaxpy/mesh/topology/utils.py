from __future__ import annotations
import numpy as np

def csr_from_pairs(num_rows, rows, cols):
    rows=np.asarray(rows,dtype=np.int64); cols=np.asarray(cols,dtype=np.int64)
    if rows.size==0:
        return np.zeros(num_rows+1,dtype=np.int64), np.empty(0,dtype=np.int64)
    order=np.lexsort((cols,rows)); rows=rows[order]; cols=cols[order]
    keep=np.ones(rows.shape[0],dtype=bool)
    if rows.shape[0]>1:
        keep[1:]=(rows[1:]!=rows[:-1]) | (cols[1:]!=cols[:-1])
    rows=rows[keep]; cols=cols[keep]
    counts=np.bincount(rows,minlength=num_rows)
    offsets=np.empty(num_rows+1,dtype=np.int64); offsets[0]=0; np.cumsum(counts,out=offsets[1:])
    return offsets, cols

def build_unique_entities(cells, local_entities):
    local=np.asarray(local_entities,dtype=np.int64)
    instances=cells[:,local].reshape(-1,local.shape[1])
    canonical=np.sort(instances,axis=1)
    entities,inverse,counts=np.unique(canonical,axis=0,return_inverse=True,return_counts=True)
    c2e=inverse.reshape(cells.shape[0],local.shape[0])
    owners=np.repeat(np.arange(cells.shape[0]),local.shape[0])
    offsets,owner_ids=csr_from_pairs(entities.shape[0],inverse,owners)
    return entities,c2e,offsets,owner_ids,counts

def build_node_to_cell(num_nodes,cells):
    return csr_from_pairs(num_nodes,cells.reshape(-1),np.repeat(np.arange(cells.shape[0]),cells.shape[1]))

def build_node_to_node(num_nodes,edges):
    return csr_from_pairs(num_nodes,np.concatenate((edges[:,0],edges[:,1])),np.concatenate((edges[:,1],edges[:,0])))

def build_cell_adjacency(num_cells,offsets,owners):
    rows=[]; cols=[]
    for eid in range(len(offsets)-1):
        own=owners[offsets[eid]:offsets[eid+1]]
        for a in own:
            for b in own:
                if a!=b: rows.append(a); cols.append(b)
    return csr_from_pairs(num_cells,np.asarray(rows,dtype=np.int64),np.asarray(cols,dtype=np.int64))

def boundary_edge_ids_from_boundary_faces(edges,boundary_faces):
    lookup={tuple(e):i for i,e in enumerate(edges.tolist())}; ids=set()
    for face in boundary_faces:
        for i in range(len(face)):
            for j in range(i+1,len(face)):
                key=tuple(sorted((int(face[i]),int(face[j]))))
                if key in lookup: ids.add(lookup[key])
    return np.asarray(sorted(ids),dtype=np.int64)
