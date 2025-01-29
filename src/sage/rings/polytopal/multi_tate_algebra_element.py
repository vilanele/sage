from sage.categories.algebras import Algebras
from sage.rings.padics.factory import Qp
from sage.geometry.polyhedral_complex import Polyhedron
# from sage.rings.polytopal.polytopal_terms import PolytopalAlgebraTerm
from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.element import  CommutativeAlgebraElement
from sage.modules.all import vector
from sage.arith.misc import valuation
from sage.rings.polynomial.polydict import PolyDict
from sage.rings.polytopal.multi_tate_terms import MultiTateAlgebraTerm


# %%
class MultiTateAlgebraElement(CommutativeAlgebraElement):
    def __init__(self, parent, x=None):
        CommutativeAlgebraElement.__init__(self, parent)
        if isinstance(x, MultiTateAlgebraElement):
            if x.parent() == parent:
                self._poly = PolyDict(x._poly.dict())
            else:
                raise TypeError("Parents do not match")
        elif isinstance(x, PolyDict):
            try:
                self._poly = PolyDict({e:parent._field(c) for e,c in x.dict().items() })
            except Exception:
                print("Error from Polydict creation")
        else:
            # print("Sstrange")
            pass
            
    def _add_(self, other):
        ans = self.__class__(self.parent())
        ans._poly = self._poly + other._poly
        return ans

    def _sub_(self, other):
        ans = self.__class__(self.parent())
        ans._poly = self._poly - other._poly
        return ans

    def _mul_(self, other):
        ans = self.__class__(self.parent())
        ans._poly = self._poly * other._poly
        return ans

    def _neg_(self):
        ans = self.__class__(self.parent())
        ans._poly = self._poly.scalar_lmult(-1)
        return ans

    def _repr_(self):
        return self.parent()._names[0]

    def terms(self):
        return [ MultiTateAlgebraTerm(self.parent(), c, e)  for e,c in self._poly.dict().items()]
        

