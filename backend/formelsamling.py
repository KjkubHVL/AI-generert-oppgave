"""Formelsamling for MatteHjelpen.

Inneholder sentrale formler fra Edwards & Penney og Thomas' Calculus.
Hver formel har ID, navn, LaTeX-formel, referanse og bruk.
"""

FORMELSAMLING = {
    # Derivasjonsregler
    "D1": {
        "navn": "Potensregel",
        "formel": r"\frac{d}{dx}(x^n) = n x^{n-1}",
        "referanse": "Edwards & Penney, Differential Equations & Linear Algebra, kapittel 3.1",
        "bruk": "Derivasjon av polynomer og potensuttrykk"
    },
    "D2": {
        "navn": "Konstantregel",
        "formel": r"\frac{d}{dx}(c) = 0",
        "referanse": "Thomas' Calculus, kapittel 3.2",
        "bruk": "Derivasjon av konstanter"
    },
    "D3": {
        "navn": "Produktregel",
        "formel": r"\frac{d}{dx}(uv) = u'v + uv'",
        "referanse": "Edwards & Penney, kapittel 3.2",
        "bruk": "Derivasjon av produkter av funksjoner"
    },
    "D4": {
        "navn": "Kjerneregel",
        "formel": r"\frac{d}{dx}f(g(x)) = f'(g(x)) \cdot g'(x)",
        "referanse": "Thomas' Calculus, kapittel 3.5",
        "bruk": "Derivasjon av sammensatte funksjoner"
    },
    "D5": {
        "navn": "Kvotientregel",
        "formel": r"\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{u'v - uv'}{v^2}",
        "referanse": "Edwards & Penney, kapittel 3.2",
        "bruk": "Derivasjon av brøker"
    },
    "D6": {
        "navn": "Eksponentialfunksjon",
        "formel": r"\frac{d}{dx}(e^x) = e^x",
        "referanse": "Thomas' Calculus, kapittel 3.8",
        "bruk": "Derivasjon av e^x"
    },
    "D7": {
        "navn": "Logaritmefunksjon",
        "formel": r"\frac{d}{dx}(\ln x) = \frac{1}{x}",
        "referanse": "Edwards & Penney, kapittel 3.8",
        "bruk": "Derivasjon av naturlig logaritme"
    },
    "D8": {
        "navn": "Sinusfunksjon",
        "formel": r"\frac{d}{dx}(\sin x) = \cos x",
        "referanse": "Thomas' Calculus, kapittel 3.5",
        "bruk": "Derivasjon av sinus"
    },
    "D9": {
        "navn": "Cosinusfunksjon",
        "formel": r"\frac{d}{dx}(\cos x) = -\sin x",
        "referanse": "Thomas' Calculus, kapittel 3.5",
        "bruk": "Derivasjon av cosinus"
    },
    
    # Integrasjonsregler
    "I1": {
        "navn": "Potensintegral",
        "formel": r"\int x^n \, dx = \frac{x^{n+1}}{n+1} + C \quad (n \neq -1)",
        "referanse": "Edwards & Penney, Differential Equations & Linear Algebra, kapittel 6.1",
        "bruk": "Integrasjon av polynomer og potensuttrykk"
    },
    "I2": {
        "navn": "Eksponentialintegral",
        "formel": r"\int e^x \, dx = e^x + C",
        "referanse": "Thomas' Calculus, kapittel 5.6",
        "bruk": "Integrasjon av e^x"
    },
    "I3": {
        "navn": "Logaritmeintegral",
        "formel": r"\int \frac{1}{x} \, dx = \ln|x| + C",
        "referanse": "Edwards & Penney, kapittel 6.2",
        "bruk": "Integrasjon av 1/x"
    },
    "I4": {
        "navn": "Delvis integrasjon",
        "formel": r"\int u \, dv = uv - \int v \, du",
        "referanse": "Thomas' Calculus, kapittel 7.1",
        "bruk": "Integrasjon av produkter av funksjoner"
    },
    "I5": {
        "navn": "Sinusintegral",
        "formel": r"\int \sin x \, dx = -\cos x + C",
        "referanse": "Edwards & Penney, kapittel 6.1",
        "bruk": "Integrasjon av sinus"
    },
    "I6": {
        "navn": "Cosinusintegral",
        "formel": r"\int \cos x \, dx = \sin x + C",
        "referanse": "Thomas' Calculus, kapittel 5.6",
        "bruk": "Integrasjon av cosinus"
    },
    
    # Lineær algebra
    "L1": {
        "navn": "Determinant (2×2)",
        "formel": r"\det\begin{pmatrix}a & b \\ c & d\end{pmatrix} = ad - bc",
        "referanse": "Edwards & Penney, Differential Equations & Linear Algebra, kapittel 4.1",
        "bruk": "Beregning av determinant for 2×2-matriser"
    },
    "L2": {
        "navn": "Matriselikninger",
        "formel": r"A\mathbf{x} = \mathbf{b}",
        "referanse": "Edwards & Penney, kapittel 4.2",
        "bruk": "Løsning av lineære ligningssystemer"
    },
    
    # Differensialligninger
    "O1": {
        "navn": "Karakteristisk ligning",
        "formel": r"ar^2 + br + c = 0",
        "referanse": "Edwards & Penney, Differential Equations & Linear Algebra, kapittel 8.2",
        "bruk": "Løsning av lineære ODE-er med konstante koeffisienter"
    },
    "O2": {
        "navn": "Generell løsning, 2. orden",
        "formel": r"y(t) = y_c(t) + y_p(t)",
        "referanse": "Edwards & Penney, kapittel 8.1",
        "bruk": "Allmen løsningsform for lineære ODE-er"
    },
    
    # Komplekse tall
    "C1": {
        "navn": "Eulers formel",
        "formel": r"e^{ix} = \cos x + i \sin x",
        "referanse": "Edwards & Penney, Differential Equations & Linear Algebra, kapittel 10.1",
        "bruk": "Komplekse tall og trigonometriske representasjoner"
    },
    "C2": {
        "navn": "Polarform",
        "formel": r"z = r(\cos \theta + i \sin \theta) = r e^{i\theta}",
        "referanse": "Thomas' Calculus, kapittel 12.8",
        "bruk": "Representasjon av komplekse tall i polarkoordinater"
    },
    "C3": {
        "navn": "Modulus av komplekst tall",
        "formel": r"|z| = \sqrt{a^2 + b^2} \text{ hvor } z = a + bi",
        "referanse": "Edwards & Penney, kapittel 10.1",
        "bruk": "Beregning av størrelse på komplekst tall"
    },
}


def get_formula(formula_id: str):
    """Hent en formel fra samlingen ved ID."""
    return FORMELSAMLING.get(formula_id, None)


def list_all_formulas():
    """Liste alle tilgjengelige formler."""
    return FORMELSAMLING
