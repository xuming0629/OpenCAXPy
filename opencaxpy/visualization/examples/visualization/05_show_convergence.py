"""Test 6: log-log error convergence and observed order."""

import numpy as np

from opencaxpy.visualization import estimate_convergence_order, show_convergence


h = np.array([0.5, 0.25, 0.125, 0.0625], dtype=float)
error = 0.32 * h**2

result = estimate_convergence_order(h, error)
print("pair orders  =", result.pair_orders)
print("fitted order =", result.fitted_order)

show_convergence(
    h,
    error,
    label="L2 error",
    expected_order=2,
    title="L2 Error Convergence",
)
