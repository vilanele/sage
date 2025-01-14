from sage.categories.algebras import Algebras
from sage.geometry.polyhedral_complex import Polyhedron
from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.element import Element
from sage.structure.parent import Parent
from sage.rings.all import PolynomialRing
from sage.modules.free_module_element import vector
from sage.rings.polytopal.polytopal_algebra_element import PolytopalAlgebraElement



class PolytopalAlgebra(Parent, UniqueRepresentation):
    def __init__(self, field, polyhedron, p, names, order="degrevlex"):
        self._p = p
        self._field = field
        self._polyhedron = polyhedron
        self._names = names
        self._order = order
        self._polynomial_ring = PolynomialRing(field, names, order=order)
        self._n = self._polynomial_ring.ngens()
        self._port = Polyhedron(
            rays=[[1 if i == j else 0 for i in range(self._n)] for j in range(self._n)]
        )
        Parent.__init__(self, category=Algebras(field).Commutative())

    def gens(self):
        return (self(x) for x in self._polynomial_ring.gens())

    def _element_constructor_(self, *args, **kwargs):
        return self.element_class(self, self._polynomial_ring(*args))

    def _coerce_map_from_(self, R):
        if self._field.has_coerce_map_from(R):
            return True
        else:
            return False

    def Ui(self, i):
        r = self._polyhedron.vertices()[i]
        print(f"r: {r}")
        V = self._polyhedron.vertices()[:i] + self._polyhedron.vertices()[i + 1 :]
        print(f"V: {V}")
        ieqs=[[0] + list(vector(v) - vector(r)) for v in V]
        print(ieqs)
        return self._port.intersection(
            Polyhedron(ieqs=ieqs)
        )

    Element = PolytopalAlgebraElement

