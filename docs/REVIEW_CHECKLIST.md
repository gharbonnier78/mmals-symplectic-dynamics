# Reviewer checklist

## Mathematical correctness

- [x] Unitary realification uses a consistent block-sign convention.
- [x] Orthogonal and symplectic preservation are stated separately.
- [x] Symbit tensor-product dimensions are corrected.
- [x] Linear-Gaussian simulation boundary is acknowledged.
- [x] Pure symplectic flow is not claimed to provide dissipation or convergence.
- [x] Energy-balance statements list their assumptions.

## Volovich executable audit

- [x] `psi=q+ip`, `H=K+iL` realification is reproduced numerically from both ODE forms.
- [x] The unitary realification is verified as both orthogonal and symplectic.
- [x] A one-mode squeezing counterexample shows that generic symplectic maps do not preserve Euclidean normalization.
- [x] Eqs. (2.20)/(3.4) are checked against the paper's own `psi=q+ip` sign convention.
- [x] The `R^2` tensor-product dimension statement is checked explicitly (`2^N`, not `2N`).
- [x] The displayed "NOT" matrix is distinguished from Pauli-X (it is `iY`).
- [x] Gain, conditioning, and precision growth are made explicit for squeezing.
- [x] Classical first/second-moment propagation is demonstrated for the linear Gaussian sector.
- [x] Notebook structure is deterministic: 22 cells, 10 executable cells, all assertions pass.
- [ ] Define a complete symplectic-computer state, measurement, noise, and resource model before making a complexity-separation claim.
- [ ] Identify a problem family and prove a like-for-like complexity advantage over the relevant classical/quantum baselines.
- [ ] Separate linear-Gaussian capability from any non-Gaussian or nonlinear resource claimed to provide computational separation.

## MMALS scientific discipline

- [x] Hosts, mycelial medium, and mycorrhizal interfaces remain distinct.
- [x] Inferred context is separated from route selection.
- [x] Audit memory is separated from compiled functional memory.
- [x] Specialization requires causal and cross-seed evidence.
- [x] Calibration is not equated with competence.
- [x] Existing internal values are labeled as previously reported evidence.
- [ ] Re-run the proposed symplectic experiments from immutable evidence bundles.

## Publication

- [x] Full LaTeX source and BibTeX included.
- [x] PDF compiles without external fonts or shell escape.
- [x] Diderot and magazine integration assets included.
- [ ] Replace independent affiliation if an institutional affiliation is required.
- [ ] Choose final arXiv license.
- [ ] Verify all repository URLs after publication.
