# Task 5: Cost Optimization Analysis

All figures are **resource sizes and requests**, not money. No cloud prices, billing data or monetary savings are used or claimed.
The Kubernetes environment is a local Minikube setup.

| # | Technique | Before | After | Change | Type |
|---|---|---|---|---|---|
| 1 | Docker image size reduction (`python:3.12-slim`, `--no-cache-dir`, copy only `app.py`, `.dockerignore`) | Unoptimized comparison image `visitor-counter:unoptimized`: 419,941,666 bytes (~420 MB) | Current image `visitor-counter:current`: 46,138,672 bytes (~46.1 MB) | 89.01% smaller | **Measured** (controlled comparison build) |
| 2 | Resource right-sizing of web pods (2 pods combined) | Configured requests: 200m CPU, 128Mi memory | Measured usage (final snapshot): 2m CPU, 128Mi memory | Memory request matches usage; CPU request is well above idle usage | **Measured** usage vs configured values (not a before/after of an older deployment) |
| 3 | HPA autoscaling (min 2, max 6) instead of fixed 6 replicas | Fixed 6 replicas: 600m CPU, 384Mi memory requested | HPA at low load, 2 replicas: 200m CPU, 128Mi memory requested | 66.7% lower requests at low load | **Calculated** from configured requests. The scaling 2 to 6 to 2 itself was **measured**. |

## Notes

- **Technique 1.** The original Dockerfile was already optimized, so against the first saved baseline the measured difference is 0% (46,138,672 bytes in both). The unoptimized image was built from `docs/Dockerfile.unoptimized` (full `python:3.12` base, `COPY . .`, no cache flag) only to measure the effect of the technique. It is not a historical measurement. Reduction = (419,941,666 - 46,138,672) / 419,941,666 = 89.01%.
- **Technique 2.** Each web pod has a 64Mi memory request and measured about 63-65Mi. Each pod measured about 1m CPU against a 100m request. The CPU request stays at 100m because the HPA calculates utilization as a percentage of the request. No earlier over-provisioned deployment was measured, so no historical before/after is claimed.
- **Technique 3.** 6 x 100m = 600m and 6 x 64Mi = 384Mi (fixed). 2 x 100m = 200m and 2 x 64Mi = 128Mi (HPA minimum). (600 - 200) / 600 = 66.7%. This compares requested resources, not billing. Under load the HPA scales up to 6 replicas, so the reduction applies to idle or low-load periods only.
- Resource usage values are single `kubectl top` snapshots, not long-term averages.
