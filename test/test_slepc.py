import pytest
from petsc4py import PETSc
from slepc4py import SLEPc


def test_slepc_eigenvalues():
    # Create a simple 2x2 matrix
    A = PETSc.Mat().create()
    A.setSizes([2, 2])
    A.setFromOptions()
    A.setUp()

    A[0, 0] = 2.0
    A[0, 1] = 1.0
    A[1, 0] = 1.0
    A[1, 1] = 3.0
    A.assemble()

    # Create eigensolver
    E = SLEPc.EPS().create()
    E.setOperators(A)
    E.setProblemType(SLEPc.EPS.ProblemType.HEP)

    E.solve()

    nconv = E.getConverged()
    assert nconv > 0, "No eigenvalues converged"

    vr, vi = A.getVecs()
    eigvals = []

    for i in range(nconv):
        eig = E.getEigenpair(i, vr, vi)
        eigvals.append(eig.real)

    eigvals.sort()

    # Known eigenvalues of [[2,1],[1,3]]
    assert pytest.approx(eigvals[0], rel=1e-6) == 1.381966
    assert pytest.approx(eigvals[1], rel=1e-6) == 3.618034

