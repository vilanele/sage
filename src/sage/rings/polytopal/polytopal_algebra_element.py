from sage.categories.algebras import Algebras
from sage.rings.padics.factory import Qp
from sage.geometry.polyhedral_complex import Polyhedron
from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.element import Element
from sage.modules.all import vector
from sage.arith.misc import valuation


# %%
class PolytopalAlgebraElement(Element):
    def __init__(self, parent, poly):
        self.parent = parent
        self.poly = poly
        Element.__init__(self, parent)

    def _add_(self, other):
        return self.__class__(self.parent, self.poly + other.poly)

    def _sub_(self, other):
        return self.__class__(self.parent, self.poly - other.poly)

    def _mul_(self, other):
        return self.__class__(self.parent, self.poly * other.poly)

    def _neg_(self):
        return self.__class__(self.parent, -self.poly)

    def valr(self, r):
        return min(
            [
                valuation(c, self.parent._p) - vector(r).dot_product(vector(e))
                for (e, c) in self.poly.dict().items()
            ]
        )

    def vali(self, i):
        return self.valr(self.parent._polyhedron.vertices()[i])

    def valP(self):
        polyhedron = self.parent._polyhedron
        return min([self.valr(r) for r in polyhedron.vertices()])

    def Gi(self, i):
        polyhedron =  self.parent._polyhedron
        r = polyhedron.vertices()[i]
        print(f"r: {r}")
        V = polyhedron.vertices()[:i] + polyhedron.vertices()[i + 1 :]
        print(f"V: {V}")
        ieqs=[
            [self.valr(v) - self.valr(r)] + list(vector(v) - vector(r))
            for (j, v) in enumerate(V)
        ]
        print(ieqs)
        return self.parent._port.intersection(
            Polyhedron(ieqs=ieqs
            )
        )
