import numpy as np
def von_mises_3d(stress):
    s=np.asarray(stress,float)
    sx,sy,sz,txy,tyz,tzx=[s[...,i] for i in range(6)]
    return np.sqrt(0.5*((sx-sy)**2+(sy-sz)**2+(sz-sx)**2)+3*(txy**2+tyz**2+tzx**2))
