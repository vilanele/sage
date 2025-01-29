from sage.categories.algebras import Algebras
from sage.geometry.polyhedral_complex import Polyhedron
from sage.rings.polytopal.multi_tate_algebra_element import MultiTateAlgebraElement
from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.element import Element
from sage.structure.parent import Parent
from sage.rings.all import PolynomialRing
from sage.modules.free_module_element import vector
from sage.rings.polytopal.polytopal_algebra_element import PolytopalAlgebraElement
from sage.rings.polynomial.polydict import PolyDict


class MultiTateAlgebra(Parent, UniqueRepresentation):
    def __init__(self, field, vertices, p, names, order="degrevlex"):
        self._p = p
        self._field = field
        self._vertices = vertices
        self._names = names
        self._order = order
        self.element_class = MultiTateAlgebraElement
        self._polynomial_ring = PolynomialRing(field, names, order=order)
        self._ngens = self._polynomial_ring.ngens()
        Parent.__init__(self, category=Algebras(field).Commutative())

    def gens(self):
        return tuple(
            self.element_class(
                self, PolyDict({(0,) * i + (1,) + (0,) * (self._ngens - i - 1): 1})
            )
            for i in range(self._ngens)
        )

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

