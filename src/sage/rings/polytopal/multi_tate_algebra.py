from sage.categories.algebras import Algebras
from sage.geometry.polyhedral_complex import Polyhedron
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

import random, itertools


class MultiTateAlgebra(Parent, UniqueRepresentation):
    def __init__(self, field, vertices, names, order="degrevlex"):
        self._field = field
        self._vertices = vertices
        self._nvertices = len(vertices)
        self._names = names
        self._order = order
        self.element_class = MultiTateAlgebraElement
        self._polynomial_ring = PolynomialRing(field, names, order=order)
        self._ngens = self._polynomial_ring.ngens()
        self._quadrant = nonnegative_orthant(self._ngens).polyhedron()
        self._negquadrant = Polyhedron(
            rays=[tuple(-1 * vector(ray)) for ray in self._quadrant.rays()]
        )
        Parent.__init__(self, category=Algebras(field).Commutative())

    def gens(self):
        return tuple(
            self.element_class(
                self, PolyDict({(0,) * i + (1,) + (0,) * (self._ngens - i - 1): 1})
            )
            for i in range(self._ngens)
        )

    def random_element(self, n_exps, n_max):
        n = self._ngens
        poly = {}
        for i in range(n_exps):
            poly[tuple(random.randint(0,n_max) for t in range(n))] = self._field.random_element()
    
        return self.element_class(self, PolyDict(poly))

    def one(self):
        return self.element_class(self, PolyDict({(0,) * self._ngens: 1}))

    def gen(self, i):
        return self.gens()[i]

    def _element_constructor_(self, x):
        try:
            y = self._field(x)
            return self.element_class(self, PolyDict({(0,) * self._ngens: y}))
        except Exception:
            print("element constructor error")

    def _coerce_map_from_(self, R):
        if self._field.has_coerce_map_from(R):
            return True
        else:
            return False

    # Compute V_i as a cone
    def V(self, i):
        ieqs = []
        for v in self._vertices[:i] + self._vertices[i + 1 :]:
            a = tuple(vector(self._vertices[i]) - vector(v))
            ieqs.append((0,) + a)

        return Polyhedron(ieqs=ieqs).intersection(self._quadrant)

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
