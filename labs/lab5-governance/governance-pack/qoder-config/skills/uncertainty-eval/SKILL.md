---
name: uncertainty-eval
description: Evaluates measurement uncertainty following the GUM approach (Type A / Type B evaluation, combined standard uncertainty, expanded uncertainty U=k*uc). Use when implementing or reviewing calibration uncertainty calculations.
version: 1.0.0
---

# Measurement uncertainty evaluation (GUM)

Follow this procedure when implementing or reviewing uncertainty calculations:

1. Type A evaluation: standard deviation of repeated measurements, u_a = s / sqrt(n).
2. Type B evaluation: from calibration certificates or specifications, assuming a
   distribution (rectangular: a / sqrt(3); triangular: a / sqrt(6); normal: a / k).
3. Combined standard uncertainty: uc(y) = sqrt(sum(ui^2)) for uncorrelated inputs.
4. Expanded uncertainty: U = k * uc(y), normally k = 2 (approx. 95% coverage).
5. Report every component with its source, distribution, divisor, and the final U with k.

Pitfalls:

- Do not mix standard uncertainties and expanded uncertainties in the same sum.
- Always state the k value and the coverage probability explicitly.
- For correlated inputs, add covariance terms; flag this instead of silently ignoring it.
