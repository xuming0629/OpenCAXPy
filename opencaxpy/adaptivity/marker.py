import numpy as np
def dorfler_mark(indicator,theta=0.5):
    eta=np.asarray(indicator,float); order=np.argsort(-eta); total=eta.sum()
    out=[]; acc=0.0
    for i in order:
        out.append(int(i)); acc+=eta[i]
        if acc>=theta*total: break
    return np.asarray(out,int)
