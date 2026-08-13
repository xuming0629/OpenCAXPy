from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .base import Plot


@dataclass(frozen=True)
class ConvergenceResult:
    h: np.ndarray
    error: np.ndarray
    pair_orders: np.ndarray
    fitted_order: float


def estimate_convergence_order(h, error):
    h=np.asarray(h,float).reshape(-1); e=np.asarray(error,float).reshape(-1)
    if len(h)!=len(e) or len(h)<2: raise ValueError("h and error need same length >= 2")
    if np.any(h<=0) or np.any(e<=0): raise ValueError("h/error must be positive")
    p=np.log(e[:-1]/e[1:])/np.log(h[:-1]/h[1:])
    fit=float(np.polyfit(np.log(h),np.log(e),1)[0])
    return ConvergenceResult(h,e,p,fit)


class ConvergencePlot(Plot):
    def __init__(self, h, error, *, label="error", expected_order=None, title="Error convergence"):
        self.h=h; self.error=error; self.label=label
        self.expected_order=expected_order; self.title=title
        self.result=None

    @property
    def backend(self): return "matplotlib"

    def render(self, context):
        ax=context.ax
        r=estimate_convergence_order(self.h,self.error); self.result=r
        ax.loglog(r.h,r.error,"o-",label=f"{self.label} (p={r.fitted_order:.3f})")
        if self.expected_order is not None:
            p=float(self.expected_order); c=r.error[-1]/(r.h[-1]**p)
            ax.loglog(r.h,c*r.h**p,"--",label=f"O(h^{p:g})")
        ax.set_xlabel("Mesh size h"); ax.set_ylabel("Error")
        ax.set_title(self.title); ax.grid(True,which="both",alpha=.25); ax.legend(); ax.invert_xaxis()
        return r
