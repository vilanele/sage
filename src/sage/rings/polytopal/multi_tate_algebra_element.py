from sage.categories.algebras import Algebras
from sage.rings.padics.factory import Qp
from sage.geometry.polyhedral_complex import Polyhedron

# from sage.rings.polytopal.polytopal_terms import PolytopalAlgebraTerm
from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.element import CommutativeAlgebraElement
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
                self._poly = PolyDict(
                    {e: parent._field(c) for e, c in x.dict().items()}
                )
            except Exception:
                print("Error from Polydict creation")
        else:
            # print("Sstrange")
            pass

    # The valuation at vertex i
    def val_at(self, i):
        return min([t.val_at(i) for t in self.terms()])

    # The initial part at vertex i
    def initial_at(self, i):
        return sum([t for t in self.terms() if t.val_at(i) == self.val_at(i)])

    # Return the P valuation and optionally the list of indices at which it is reached.
    def valP(self, indices=False):
        valvec = [self.val_at(i) for i in range(self.parent()._nvertices)]
        m = min(valvec)
        if not indices:
            return m
        else:
            return [i for i, v in enumerate(valvec) if v == m]

    # The initial part for the order on indices
    def initial(self):
        i = min(self._valP(indices=True))
        return self.initial_at(i)

    # The leading monomial
    def lm(self):
        i = min(self._valP(indices=True))
        ini = self.initial_at(i)
        return 1

    # The leading coefficient
    def lc(self):
        i = min(self._valP(indices=True))
        ini = self.initial_at(i)
        return 1

    # The leading term
    def lt(self):
        return self.lc() * self.lm()


    # The leading monomial at vertex i
    def lm_at(self, i=None):
        if i is None:
            return self.lm()

        m = min(t.val_at(i) for t in self.terms())
        terms = [t for t in self.terms() if t.val_at(i) == m]
        return terms[0].monomial()

    # The leading coefficient at vertex i
    def lc_at(self):
        pass

    # The leading term at vertex i
    def lt_at(self):
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
        return str(self._poly)

    # All termes
    def terms(self):
        return [
            MultiTateAlgebraTerm(self.parent(), c, e)
            for e, c in self._poly.dict().items()
        ]

    def monomials(self):
        return [term.monomial() for term in self.terms()]

    def V(self, i=None):
        vertices = self.parent()._vertices
        if i is None:
            P = []
            for j in range(len(vertices)):
                P.append(self.V(j))
            return P

        ieqs = []
        for j in [k for k in range(len(vertices)) if k != i]:
            v = vertices[j]
            a = tuple(vector(vertices[i]) - vector(v))
            c = self.val_at(i) - self.val_at(j)
            ieqs.append((-c,) + a)

        return Polyhedron(ieqs=ieqs).intersection(self.parent()._quadrant)

    def lmV(self, i=None):
        vertices = self.parent()._vertices
        if i is None:
            P = []
            for j in range(len(vertices)):
                P.append(self.lmV(j))
            return P

        lmi = self.lm_at(i)
        shift = vector(lmi.exponent())
        print(shift)
        conei = self.parent().V(i)
        return Polyhedron(
            rays=conei.rays(),
            vertices=[list(vector(v) + shift) for v in self.V(i).vertices()],
        )
