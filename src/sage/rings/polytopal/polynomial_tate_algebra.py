from sage.categories.algebras import Algebras
from sage.geometry.polyhedral_complex import Polyhedron
from sage.rings.polynomial.multi_polynomial_ring import MPolynomialRing_polydict
from sage.rings.polynomial.polynomial_ring import PolynomialRing_field
from sage.rings.polytopal.multi_tate_algebra_element import MultiTateAlgebraElement
from sage.structure.unique_representation import UniqueRepresentation

# from sage.structure.element import Element
from sage.structure.parent import Parent
from sage.rings.all import PolynomialRing
from sage.modules.free_module_element import vector
from sage.rings.polytopal.polytopal_algebra_element import PolytopalAlgebraElement
from sage.rings.polynomial.polydict import PolyDict, ETuple
from sage.geometry.cone import Cone
from sage.geometry.cone_catalog import nonnegative_orthant
from sage.geometry.fan import Fan

from sage.plot.point import point
from sage.plot.colors import Color

import random, itertools


class PolynomialTateAlgebra(MPolynomialRing_polydict):
    def __init__(self, field, vertices, n, names, order="degrevlex"):
        MPolynomialRing_polydict.__init__(self, field, n, names, order)
        self._vertices = vertices
        self._n_vertices = len(vertices)
        self._colors = [
            Color(random.random(), random.random(), random.random())
            for i in range(self._n_vertices)
        ]
        self._quadrant = nonnegative_orthant(self.ngens()).polyhedron()
        self._negquadrant = Polyhedron(
            rays=[tuple(-1 * vector(ray)) for ray in self._quadrant.rays()]
        )

    # Compute V_i as a cone
    def V(self, i):
        ieqs = []
        for v in self._vertices[:i] + self._vertices[i + 1 :]:
            a = tuple(vector(self._vertices[i]) - vector(v))
            ieqs.append((0,) + a)

        return Polyhedron(ieqs=ieqs).intersection(self._quadrant)

    def Vf(self, f, i=None):
        vertices = self._vertices
        if i is None:
            P = []
            for j in range(len(vertices)):
                P.append(self.Vf(f, j))
            return P

        ieqs = []
        for j in [k for k in range(len(vertices)) if k != i]:
            v = vertices[j]
            a = tuple(vector(vertices[i]) - vector(v))
            c = self.val_at(f, i) - self.val_at(f, j)
            ieqs.append((-c,) + a)

        return Polyhedron(ieqs=ieqs).intersection(self._quadrant)

    def Vf_real(self, f, i=None):
        vertices = self._vertices
        if i is None:
            P = []
            for j in range(len(vertices)):
                P.append(self.Vf_real(f, j))
            return P

        ieqs = []
        for j in [k for k in range(len(vertices)) if k != i]:
            v = vertices[j]
            a = tuple(vector(vertices[i]) - vector(v))
            c = self.val_at(f, i) - self.val_at(f, j)
            if j < i:
                c += 1
            ieqs.append((-c,) + a)

        return Polyhedron(ieqs=ieqs).intersection(self._quadrant)

    def lmV(self, f, i=None):
        vertices = self._vertices
        if i is None:
            P = []
            for j in range(len(vertices)):
                P.append(self.lmV(f, j))
            return P

        lmi = self.lm_at(f, i)
        shift = vector(lmi.exponents()[0])
        print(shift)
        conei = self.Vf(f, i)
        return Polyhedron(
            rays=conei.rays(),
            vertices=[list(vector(v) + shift) for v in self.Vf(f, i).vertices()],
            backend="normaliz",
        )

    def crible(self, f, n):
        points = []
        for a in itertools.product(range(n), repeat=self.ngens()):
            m = self({a: 1})
            points.append(self.lm(m * f).exponents()[0])

        pl = point(points, color="red", size=2).plot()
        generators = []
        for i in range(self._n_vertices):
            pl += sum(
                [
                    point(p, color=self._colors[i], size="20").plot()
                    for p in self.lmV_real(f, i).integral_points_generators()[0]
                ]
            )
        return pl

    def lmV_real(self, f, i=None):
        vertices = self._vertices
        if i is None:
            P = []
            for j in range(len(vertices)):
                P.append(self.lmV_real(f, j))
            return P

        lmi = self.lm_at(f, i)
        shift = vector(lmi.exponents()[0])
        print(shift)
        conei = self.Vf(f, i)
        return Polyhedron(
            rays=conei.rays(),
            vertices=[list(vector(v) + shift) for v in self.Vf_real(f, i).vertices()],
            backend="normaliz",
        )

    def generators(self, f, i):
        return self.lmV(f, i).integral_points_generators()[0]

    def generators_pair(self, f, g, i):
        return (
            self.lmV(f, i).intersection(self.lmV(f, i)).integral_points_generators()[0]
        )

    def fan(self):
        cones = []
        for i in range(len(self._vertices)):
            cones.append(Cone(self.V(i)))

        return Fan(cones=cones)

    def polyhedron(self):
        return Polyhedron(
            vertices=self._vertices,
            rays=self._negquadrant.rays(),
        )

    # Valuation of term at vertex i
    def val_term_at(self, t, i):
        c = t.coefficients()[0]
        m = t.exponents()[0]
        return c.valuation() - vector(self._vertices[i]).dot_product(vector(m))

    # Valuation of f at vertex i
    def val_at(self, f, i):
        return min([self.val_term_at(t, i) for t in f.terms()])

    # Valuation of f
    def val(self, f, indices=False):
        val_list = [self.val_at(f, i) for i in range(self._n_vertices)]
        m = min(val_list)
        if not indices:
            return m
        else:
            return [i for i, v in enumerate(val_list) if v == m]

    # Initial part of f at vertex i
    def initial_at(self, f, i):
        m = self.val_at(f, i)
        return sum([t for t in f.terms() if self.val_term_at(t, i) == m])

    # Initial part of f
    def initial(self, f):
        indices = self.val(f, indices=True)
        i = min(indices)
        return self.initial_at(f, i)

    # Initial monomial of f
    def lm(self, f):
        return self.initial(f).leading_monomial()

    # Initial coefficient of f
    def lc(self, f):
        return f[self.lm(f)]

    # Initial term of f
    def lt(self, f):
        return self.lc(f) * self.lm(f)

    # Leading monomial for vertex i
    def lm_at(self, f, i):
        return self.initial_at(f, i).leading_monomial()

    # Leading coefficient for vertex i
    def lc_at(self, f, i):
        return f[self.lm_at(f, i)]

    # Leading term for vertex i
    def lt_at(self, f, i):
        return self.lc_at(f, i) * self.lm_at(f, i)
