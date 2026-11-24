# Changelog

## 2.0.1

- Compare JSON protocol declarations structurally in JavaScript; preserve array order but ignore object key order. Reject non-synthetic records with unknown timing, consistent with the Python comparison gate.
- Prevent nonfinite normalization results for extreme finite scale endpoints by rescaling overflow-prone spans; reject invalid or unrepresentable inputs.
- Add regression tests for these cases and asymmetric missing-coordinate bounds (100 seeded cases).
- Explicit UTF-8/LF for generated JSON; Git attributes preserve checked-in data bytes.
- Add release citation, licensing and GitHub-ready documentation and integrity records.
- Profile schema stays at 2.0; original study inputs, formulas and reported results are unchanged.
