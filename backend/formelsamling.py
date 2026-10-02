"""Formelsamling for MatteHjelpen."""

FORMELSAMLING = {
    "D1": {
        "navn": "Potensregel",
        "formel": r"\frac{d}{dx}(x^n) = n x^{n-1}",
        "referanse": "Edwards & Penney, kapittel 3",
        "bruk": "Derivasjon av potenser"
    },
    "D2": {
        "navn": "Produktregel",
        "formel": r"\frac{d}{dx}(u v) = u'v + uv'",
        "referanse": "Thomas' Calculus, kapittel 3",
        "bruk": "Derivasjon av produkter"
    },
    "D3": {
        "navn": "Kjerneregel",
        "formel": r"\frac{d}{dx}f(g(x)) = f'(g(x))g'(x)",
        "referanse": "Edwards & Penney, kapittel 3",
        "bruk": "Derivasjon av sammensatte funksjoner"
    },
    "I1": {
        "navn": "Potensintegral",
        "formel": r"\int x^n dx = \frac{x^{n+1}}{n+1} + C",
        "referanse": "Thomas' Calculus, kapittel 5",
        "bruk": "Integrasjon av potenser"
    },
    "I2": {
        "navn": "Delvis integrasjon",
        "formel": r"\int u\,dv = uv - \int v\,du",
        "referanse": "Edwards & Penney, kapittel 6",
        "bruk": "Integrasjon av produkter"
    },
    "L1": {
        "navn": "Løsning av ligninger",
        "formel": "Solve med SymPy",
        "referanse": "Thomas' Calculus, kapittel 1",
        "bruk": "Algebraiske ligninger"
    },
    "O1": {
        "navn": "Karakteristisk ligning",
        "formel": r"a r^2 + b r + c = 0",
        "referanse": "Edwards & Penney, kapittel 8",
        "bruk": "Løsning av lineære ODE-er"
    },
    "M1": {
        "navn": "Determinant",
        "formel": r"\det(A)",
        "referanse": "Edwards & Penney, kapittel 4",
        "bruk": "Lineær algebra"
    },
    "C1": {
        "navn": "Eulers formel",
        "formel": r"e^{ix} = \cos x + i\sin x",
        "referanse": "Thomas' Calculus, kapittel 12",
        "bruk": "Komplekse tall"
    },
    "C2": {
        "navn": "Polarform",
        "formel": r"z = r(\cos\theta + i\sin\theta)",
        "referanse": "Edwards & Penney, kapittel 10",
        "bruk": "Komplekse tall i polarform"
    }
}


def get_formula(formula_id: str):
    return FORMELSAMLING.get(formula_id)
