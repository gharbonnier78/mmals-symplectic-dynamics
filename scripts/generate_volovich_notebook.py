#!/usr/bin/env python3
"""Deterministically generate the Volovich critical/falsification notebook."""
from __future__ import annotations

import argparse
from pathlib import Path
import nbformat as nbf

NOTEBOOK_NAME = "01_volovich_realification_falsification.ipynb"


def md(text: str, idx: int):
    cell = nbf.v4.new_markdown_cell(text.strip() + "\n")
    cell["id"] = f"m{idx:02d}-volovich"
    return cell


def code(text: str, idx: int):
    cell = nbf.v4.new_code_cell(text.strip() + "\n")
    cell["id"] = f"c{idx:02d}-volovich"
    cell["execution_count"] = None
    cell["outputs"] = []
    return cell


def build_notebook():
    cells = []
    cells.append(md(r"""
# Volovich: realification, symplectic extension, and falsification tests

A small, executable audit of Igor Volovich, *Quantum vs. Symplectic Computers*, arXiv:2407.12755v1 (17 Jul 2024).

The purpose is deliberately narrower than reproducing the paper: separate identities that are mathematically correct from stronger computational claims that need an explicit physical model, measurement rule, resource accounting, and complexity argument.
""", 1))
    cells.append(md(r"""
## Source claims and conventions under test

The paper writes the Schrödinger state as $\psi=q+ip$, decomposes $H=K+iL$ with $K^T=K$ and $L^T=-L$, and derives

$$\dot q=Kp+Lq,\qquad \dot p=-Kq+Lp.$$

It also states $U(N)=Sp(2N,\mathbb R)\cap O(2N)$ and then proposes a larger symplectic gate set as the basis for potentially stronger computation. We test the first statement as an exact realification and treat the second as a hypothesis requiring additional proof obligations.
""", 2))
    cells.append(code(r"""
import math
import numpy as np
from numpy.linalg import norm
from scipy.integrate import solve_ivp
from scipy.linalg import expm

np.set_printoptions(precision=6, suppress=True)


def J_matrix(n):
    I = np.eye(n)
    Z = np.zeros((n, n))
    return np.block([[Z, I], [-I, Z]])


def realify_unitary(U):
    # Action on z=(q,p) for psi=q+i p.
    X, Y = U.real, U.imag
    return np.block([[X, -Y], [Y, X]])


def paper_gamma(U):
    # Block convention printed in Volovich eqs. (2.20)/(3.4).
    X, Y = U.real, U.imag
    return np.block([[X, Y], [-Y, X]])


def symplectic_residual(S):
    n = S.shape[0] // 2
    J = J_matrix(n)
    return norm(S.T @ J @ S - J, ord="fro")


def orthogonal_residual(S):
    return norm(S.T @ S - np.eye(S.shape[0]), ord="fro")
""", 1))
    cells.append(md(r"""
## 1. Exact Schrödinger realification

For $z=(q,p)^T$, the real generator is

$$A=\begin{pmatrix}L&K\\-K&L\end{pmatrix}.$$

The complex and real ODEs should therefore produce the same trajectory up to numerical integration error. The deliberately strict tolerance below makes that error visible rather than hiding it behind a symbolic identity.
""", 3))
    cells.append(code(r"""
rng = np.random.default_rng(92)
n = 5
M = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
H = (M + M.conj().T) / 2
K, L = H.real, H.imag
assert np.allclose(K, K.T)
assert np.allclose(L, -L.T)

psi0 = rng.normal(size=n) + 1j * rng.normal(size=n)
psi0 /= norm(psi0)
z0 = np.r_[psi0.real, psi0.imag]
A = np.block([[L, K], [-K, L]])
t_eval = np.linspace(0.0, 1.0, 101)
rtol, atol = 5.2e-14, 5.2e-16

sol_c = solve_ivp(lambda t, y: -1j * (H @ y), (0, 1), psi0,
                  t_eval=t_eval, method="DOP853", rtol=rtol, atol=atol)
sol_r = solve_ivp(lambda t, z: A @ z, (0, 1), z0,
                  t_eval=t_eval, method="DOP853", rtol=rtol, atol=atol)
assert sol_c.success and sol_r.success
z_from_complex = np.vstack([sol_c.y.real, sol_c.y.imag])
max_realification_error = np.max(np.abs(z_from_complex - sol_r.y))
print(f"max_realification_error={max_realification_error:.15e}")
assert max_realification_error < 1e-12
""", 2))
    cells.append(md(r"""
## 2. Unitary evolution is both orthogonal and symplectic

The exact real action of a unitary $U=X+iY$ on $q+ip$ is

$$R(U)=\begin{pmatrix}X&-Y\\Y&X\end{pmatrix}.$$

This is the useful mathematical core: unitary dynamics embeds into the intersection of the orthogonal and symplectic groups. It does **not** follow from the group inclusion alone that arbitrary extra symplectic transformations yield extra computational power.
""", 4))
    cells.append(code(r"""
rng = np.random.default_rng(41)
n = 5
M = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
H2 = (M + M.conj().T) / 2
U = expm(-1j * H2)
S = realify_unitary(U)

sym_residual = symplectic_residual(S)
orth_residual = orthogonal_residual(S)
unitary_residual = norm(U.conj().T @ U - np.eye(n), ord="fro")
print(f"unitary_residual={unitary_residual:.15e}")
print(f"symplectic_residual={sym_residual:.15e}")
print(f"orthogonal_residual={orth_residual:.15e}")
assert sym_residual < 1e-12
assert orth_residual < 1e-12
""", 3))
    cells.append(md(r"""
## 3. Falsification test: symplectic does not imply norm preserving

A one-mode squeezing map $S_r=\mathrm{diag}(e^r,e^{-r})$ is symplectic but not orthogonal. Therefore, if a "symbit" is required to satisfy a Euclidean normalization such as $\alpha^2+\beta^2=1$, a generic $Sp(2,\mathbb R)$ gate does not preserve that state space. A measurement/renormalization rule would have to be specified separately.
""", 5))
    cells.append(code(r"""
r = 1.25
Sq = np.diag([math.exp(r), math.exp(-r)])
z = np.array([1.0, 1.0]) / math.sqrt(2)
z2 = Sq @ z
squeeze_sym_residual = symplectic_residual(Sq)
print(f"squeeze_symplectic_residual={squeeze_sym_residual:.3e}")
print(f"input_norm={norm(z):.9f}")
print(f"output_norm={norm(z2):.9f}")
assert squeeze_sym_residual < 1e-12
assert not np.isclose(norm(z2), norm(z))
""", 4))
    cells.append(md(r"""
## 4. Sign convention audit of eqs. (2.20) and (3.4)

From the paper's own $\psi=q+ip$ and eq. (2.16), one obtains $q'=Xq-Yp$ and $p'=Yq+Xp$. The printed block matrix in eq. (2.20), repeated as $\gamma$ in eq. (3.4), has the opposite off-diagonal signs.

That printed matrix is still orthogonal-symplectic for unitary $U$; the issue is consistency with the stated state convention and preceding component equations, not the validity of the matrix as a symplectic object.
""", 6))
    cells.append(code(r"""
rng = np.random.default_rng(7)
n = 3
M = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
H3 = (M + M.conj().T) / 2
U3 = expm(-0.7j * H3)
psi = rng.normal(size=n) + 1j * rng.normal(size=n)
z = np.r_[psi.real, psi.imag]
expected = U3 @ psi
expected_z = np.r_[expected.real, expected.imag]

S_consistent = realify_unitary(U3)
S_printed = paper_gamma(U3)
err_consistent = norm(S_consistent @ z - expected_z)
err_printed = norm(S_printed @ z - expected_z)
print(f"consistent_block_error={err_consistent:.3e}")
print(f"printed_block_error={err_printed:.6f}")
print(f"printed_block_symplectic_residual={symplectic_residual(S_printed):.3e}")
assert err_consistent < 1e-12
assert err_printed > 1e-3
assert symplectic_residual(S_printed) < 1e-12
""", 5))
    cells.append(md(r"""
## 5. Tensor-product dimension audit

The paper states that $N$ tensor factors of $\mathbb R^2$ give $\mathbb R^{2N}$ and then compares this with $\mathbb C^N$. Algebraically,

$$\dim\left((\mathbb R^2)^{\otimes N}\right)=2^N,$$

not $2N$. The two numerical dimensions happen to agree only for $N=1,2$; beyond that they diverge.
""", 7))
    cells.append(code(r"""
rows = []
for N in range(1, 9):
    tensor_dim = 2 ** N
    stated_dim = 2 * N
    rows.append((N, tensor_dim, stated_dim, tensor_dim == stated_dim))
print("N | dim((R^2)^tensor N) | 2N | equal")
for row in rows:
    print(f"{row[0]:1d} | {row[1]:20d} | {row[2]:2d} | {row[3]}")
assert all((2 ** N) != (2 * N) for N in range(3, 9))
""", 6))
    cells.append(md(r"""
## 6. Gate audit: the displayed "NOT" is not Pauli-$X$

The paper's matrix $\begin{pmatrix}0&1\\-1&0\end{pmatrix}$ is unitary and swaps computational-basis labels, but it adds a basis-dependent phase. As a quantum gate it is $iY$, not Pauli-$X=\begin{pmatrix}0&1\\1&0\end{pmatrix}$, and the two are not related by a single global phase.
""", 8))
    cells.append(code(r"""
X_gate = np.array([[0, 1], [1, 0]], dtype=complex)
V_not = np.array([[0, 1], [-1, 0]], dtype=complex)
Y_gate = np.array([[0, -1j], [1j, 0]], dtype=complex)
assert np.allclose(V_not, 1j * Y_gate)
assert np.allclose(V_not.conj().T @ V_not, np.eye(2))

# Best global-phase alignment between V_not and X_gate.
overlap = np.trace(X_gate.conj().T @ V_not)
phase = 1.0 if abs(overlap) < 1e-15 else np.exp(1j * np.angle(overlap))
global_phase_distance = norm(V_not - phase * X_gate, ord="fro")
print(f"best_global_phase_distance_to_PauliX={global_phase_distance:.6f}")
print("V_not|0> =", V_not @ np.array([1, 0], dtype=complex))
print("V_not|1> =", V_not @ np.array([0, 1], dtype=complex))
assert global_phase_distance > 1.0
""", 7))
    cells.append(md(r"""
## 7. Hidden resource costs of non-orthogonal symplectic gain

Squeezing enlarges one quadrature while shrinking its conjugate. For $S_r=\mathrm{diag}(e^r,e^{-r})$, the singular-value condition number is $\kappa=e^{2r}$. Any computational advantage based on large gain therefore needs an explicit accounting of dynamic range, noise, precision, energy, and how measurement resolves the compressed direction.
""", 9))
    cells.append(code(r"""
print("r | gain=e^r | condition=e^(2r) | log2(condition)")
for r in [0, 1, 2, 4, 8, 12]:
    gain = math.exp(r)
    kappa = math.exp(2 * r)
    precision_bits = math.log2(kappa)
    print(f"{r:2d} | {gain:10.3e} | {kappa:16.3e} | {precision_bits:15.2f}")
assert math.isclose(math.log2(math.exp(24)), 24 / math.log(2), rel_tol=1e-12)
""", 8))
    cells.append(md(r"""
## 8. Gaussian continuous-variable interpretation and classical moment simulation

Linear symplectic maps are the natural transformations of phase-space quadratures. In quantum optics they form the transformation layer of Gaussian continuous-variable dynamics (with physical-state and noise constraints supplied by the quantum model). Means and covariance matrices then transform as

$$\mu' = S\mu,\qquad \Sigma'=S\Sigma S^T.$$

Those moments can be propagated classically with polynomial-size linear algebra. This does not settle the complexity of non-Gaussian extensions; it sets a concrete baseline that any stronger claim must beat.
""", 10))
    cells.append(code(r"""
rng = np.random.default_rng(2024)
modes = 6
d = 2 * modes
J = J_matrix(modes)
G0 = rng.normal(size=(d, d))
G = (G0 + G0.T) / 2
Sg = expm(0.08 * J @ G)  # Hamiltonian generator -> symplectic map

mu = rng.normal(size=d)
B = rng.normal(size=(d, d))
Sigma = B @ B.T + 0.5 * np.eye(d)
mu2 = Sg @ mu
Sigma2 = Sg @ Sigma @ Sg.T

print(f"modes={modes}, phase_space_dimension={d}")
print(f"gaussian_map_symplectic_residual={symplectic_residual(Sg):.3e}")
print(f"min_covariance_eigenvalue_before={np.linalg.eigvalsh(Sigma).min():.6f}")
print(f"min_covariance_eigenvalue_after={np.linalg.eigvalsh(Sigma2).min():.6f}")
assert symplectic_residual(Sg) < 1e-12
assert np.linalg.eigvalsh(Sigma2).min() > 0
assert mu2.shape == (d,) and Sigma2.shape == (d, d)
""", 9))
    cells.append(md(r"""
## 9. What the experiment does and does not establish

The executable results support the realification identity and the orthogonal-symplectic embedding. They also provide explicit counterexamples to norm preservation by generic symplectic maps and expose internal inconsistencies in the tensor-dimension and gate/sign discussion.

None of these tests proves that a physical symplectic computer cannot be useful. They sharpen the missing theorem: define the state space, admissible gates, measurement semantics, noise/resources, input/output encoding, and a computational problem family, then compare complexity under like-for-like resource bounds.
""", 11))
    cells.append(code(r"""
claim_register = [
    ("C1", "Schrodinger realification gives a Hamiltonian/symplectic real system", "SUPPORTED", "Algebra + trajectory equivalence"),
    ("C2", "Unitary evolution embeds in orthogonal-symplectic evolution", "SUPPORTED", "R(U)^T R(U)=I and R(U)^T J R(U)=J"),
    ("C3", "Generic symplectic gates preserve Euclidean symbit normalization", "FALSIFIED", "One-mode squeezing changes ||z||_2"),
    ("C4", "Sp strictly larger than U therefore symplectic computers are more powerful", "UNSUPPORTED", "Need computational model + lower/upper bounds"),
    ("C5", "(R^2)^tensor N has dimension 2N", "FALSIFIED", "Dimension is 2^N"),
    ("C6", "Displayed NOT gate is Pauli-X", "FALSIFIED", "Matrix is iY, not X up to global phase"),
    ("C7", "Printed gamma block matches psi=q+ip component evolution", "INCONSISTENT", "Off-diagonal signs disagree with eqs. 2.16-2.18"),
    ("C8", "Linear symplectic dynamics supplies a Gaussian-CV transformation layer", "CONDITIONAL", "Requires a physical CV state/noise/measurement model"),
    ("C9", "Large symplectic gain can be treated as a free computational resource", "UNSUPPORTED", "Conditioning and precision grow with squeezing"),
]
print("claim | status | evidence / proof obligation")
for cid, claim, status, obligation in claim_register:
    print(f"{cid:>2} | {status:<12} | {claim} :: {obligation}")
assert {row[2] for row in claim_register} >= {"SUPPORTED", "FALSIFIED", "UNSUPPORTED"}
""", 10))
    cells.append(md(r"""
## Conclusion

The strongest defensible reading is not "quantum computation is merely classical symplectic computation" and not "a larger group is automatically more powerful." It is:

1. finite-dimensional Schrödinger evolution admits an exact real Hamiltonian representation;
2. unitary gates occupy the orthogonal-symplectic sector;
3. stepping outside that sector introduces gain/squeezing and therefore new normalization, measurement, physical-realizability, and resource questions;
4. the linear-Gaussian sector remains efficiently tractable at the level of first and second moments, so any claimed computational separation must identify the non-Gaussian/nonlinear ingredient and count its cost.

This notebook is therefore a **falsification harness and proof-obligation register**, not a dismissal of the research direction.
""", 12))

    nb = nbf.v4.new_notebook(cells=cells)
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.x"},
        "volovich_audit": {
            "source": "arXiv:2407.12755v1",
            "source_date": "2024-07-17",
            "generator": "scripts/generate_volovich_notebook.py",
            "cell_count": 22,
            "code_cell_count": 10,
        },
    }
    return nb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=NOTEBOOK_NAME)
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(build_notebook(), out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
