from sage.monoids.monoid import Monoid_class
from sage.structure.element import MonoidElement
from sage.structure.unique_representation import UniqueRepresentation
from sage.modules.all import vector


class MultiTateAlgebraTerm(MonoidElement):
    def __init__(self, parent, coeff, exponent=None):
        MonoidElement.__init__(self, parent)
        self._coeff = coeff
        self._exponent = exponent

    def coefficient(self):
        return self._coeff

    def exponent(self):
        return self._exponent

    def monomial(self):
        return self.__class__(self._parent, self._parent._field(1), self._exponent)

    # Return P-valuation
    def _valP(self):
        return min([self.val_at(i) for i in range(len(self.parent()._vertices))])

    # Return valuation at r.
    def val(self, r, check=False):
        if check:
            pass

        return self._coeff.valuation() - vector(r).dot_product(
            vector(self._exponent)
        )

    # Return valuation at vertex
    def val_at(self, i=None):
        if i is None:
            return self._valP()

        return self.val(self.parent()._vertices[i])

    def mul(self, other):
        ans_coeff = self._coeff * other.coefficient()
        ans_exp = self._exponent.eadd(other.exponent())
        return self.__class__(self._parent, ans_coeff, ans_exp)

    def _repr_(self):
        return f"{self._coeff}^{self._exponent}"


class MultiTateTermMonoid(Monoid_class, UniqueRepresentation):
    Element = MultiTateAlgebraTerm

    def __init__(self, A):
        names = A.variables_names()
        Monoid_class.__init__(self, names)
