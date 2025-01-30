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

    def _valP(self):
        return min([self.val_at(i) for i in range(self.parent()._vertices)])

    def val(self,r, check=False):
        pass

    def val_at(self,i=None):
        if i is None:
            return self._valP()

        return min([t.val_at(i) for t in self.terms()])
            
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
        
    def T(self,i=None):

        vertices = self.parent()._vertices
        if i is None:
            P = []
            for j in range(len(vertices)):
                P.append(self.T(j))
            return P


        ieqs = []
        for j in [k for k in range(len(vertices)) if k != i]:
            v = vertices[j] 
            a = tuple(vector(vertices[i]) - vector(v))
            c = self.val_at(i) - self.val_at(j)
            ieqs.append((c,) + a)

        return Polyhedron(ieqs=ieqs).intersection(self.parent()._quadrant)
         

