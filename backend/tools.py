"""SymPy-verktøy for MatteHjelpen.

Alle symbolske og numeriske beregninger skjer her - aldri i modellens tekst.
Returnerer både resultat og LaTeX-representasjon.
"""

from typing import Any, Dict, List, Union

import sympy as sp


class ToolError(Exception):
    """Feil ved verktøybruk."""
    pass


def _safe_sympify(expr: str, symbols_dict: Dict[str, sp.Symbol] | None = None) -> sp.Basic:
    """Konverter streng til SymPy-uttrykk med sikre symboler."""
    try:
        # Standard symboler
        x = sp.Symbol('x')
        t = sp.Symbol('t')
        y = sp.Symbol('y')
        z = sp.Symbol('z')
        n = sp.Symbol('n')
        
        local_dict = {
            'x': x, 't': t, 'y': y, 'z': z, 'n': n,
            'I': sp.I,
            'E': sp.E,
            'pi': sp.pi,
            'exp': sp.exp,
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'sqrt': sp.sqrt,
            'ln': sp.ln,
            'log': sp.log,
        }
        
        if symbols_dict:
            local_dict.update(symbols_dict)
        
        # Gjør uttrykket trygt
        expr_clean = str(expr).replace('^', '**').replace('∫', 'integral')
        result = sp.sympify(expr_clean, locals=local_dict, transformations=(sp.parsing.transformations.standard_transformations + (sp.parsing.transformations.implicit_multiplication_application,)))
        return result
    except Exception as e:
        raise ToolError(f"Kunne ikke tolke uttrykket '{expr}': {e}")


def derive(uttrykk: str, variabel: str = 'x') -> Dict[str, Any]:
    """Deriver et uttrykk med hensyn på en variabel."""
    try:
        var = sp.Symbol(variabel)
        expr = _safe_sympify(uttrykk, {variabel: var})
        
        # Derivasjon
        result = sp.diff(expr, var)
        result_simplified = sp.simplify(result)
        
        return {
            "result": str(result_simplified),
            "latex": sp.latex(result_simplified),
            "status": "ok",
            "input": str(expr),
            "input_latex": sp.latex(expr),
        }
    except ToolError as e:
        return {"result": None, "status": "error", "message": str(e)}
    except Exception as e:
        return {"result": None, "status": "error", "message": f"Derivasjonsfeil: {e}"}


def integrate(uttrykk: str, variabel: str = 'x') -> Dict[str, Any]:
    """Integrer et uttrykk med hensyn på en variabel."""
    try:
        var = sp.Symbol(variabel)
        expr = _safe_sympify(uttrykk, {variabel: var})
        
        # Integrasjon (ubestemt)
        result = sp.integrate(expr, var)
        
        return {
            "result": str(result),
            "latex": sp.latex(result),
            "status": "ok",
            "input": str(expr),
            "input_latex": sp.latex(expr),
        }
    except ToolError as e:
        return {"result": None, "status": "error", "message": str(e)}
    except Exception as e:
        return {"result": None, "status": "error", "message": f"Integrasjonsfeil: {e}"}


def solve_equation(ligning: str, variabel: str = 'x') -> Dict[str, Any]:
    """Løs en ligning med hensyn på en variabel."""
    try:
        var = sp.Symbol(variabel)
        
        # Parse ligningen
        if "=" not in ligning:
            raise ToolError("Ligningen må inneholde '='.")
        
        lhs_str, rhs_str = ligning.split("=", 1)
        lhs = _safe_sympify(lhs_str, {variabel: var})
        rhs = _safe_sympify(rhs_str, {variabel: var})
        
        # Lag ligning
        eq = sp.Eq(lhs, rhs)
        
        # Løs
        solutions = sp.solve(eq, var)
        
        if not solutions:
            solutions = ["Ingen løsning funnet"]
        
        return {
            "result": str(solutions),
            "latex": sp.latex(solutions),
            "status": "ok",
            "equation_latex": sp.latex(eq),
        }
    except ToolError as e:
        return {"result": None, "status": "error", "message": str(e)}
    except Exception as e:
        return {"result": None, "status": "error", "message": f"Ligningsfeil: {e}"}


def solve_ode(ligning: str) -> Dict[str, Any]:
    """Løs en ordinær differensialligning."""
    try:
        # Prøv direkte løsning
        t = sp.Symbol('t')
        x = sp.Symbol('x')
        y = sp.Function('y')
        
        try:
            # Anta format: "Derivative(y(t), t) = ..." eller "dy/dt = ..."
            eq_str = ligning.replace('dy/dt', "Derivative(y(t), t)").replace('y\'', "Derivative(y(t), t)")
            eq = sp.sympify(eq_str, locals={'y': y, 't': t, 'Derivative': sp.Derivative, 'exp': sp.exp, 'sin': sp.sin, 'cos': sp.cos})
        except:
            eq = sp.Eq(sp.Derivative(y(t), t), _safe_sympify(ligning, {'t': t, 'y': y}))
        
        # Løs ODE
        solution = sp.dsolve(eq, y(t))
        
        return {
            "result": str(solution),
            "latex": sp.latex(solution),
            "status": "ok",
        }
    except Exception as e:
        return {"result": None, "status": "error", "message": f"ODE-feil: {e}"}


def matrix_op(operasjon: str, matrise_data: List[List[float]]) -> Dict[str, Any]:
    """Utfør matriseopperasjoner."""
    try:
        # Konverter til SymPy-matrise
        matrix = sp.Matrix(matrise_data)
        operasjon = operasjon.lower().strip()
        
        if operasjon == "determinant" or operasjon == "det":
            result = matrix.det()
            result_latex = f"\\det(A) = {sp.latex(result)}"
        elif operasjon == "inverse" or operasjon == "inv":
            result = matrix.inv()
            result_latex = sp.latex(result)
        elif operasjon == "eigenvalues" or operasjon == "egenverdier":
            result = matrix.eigenvals()
            result_latex = sp.latex(result)
        elif operasjon == "eigenvectors" or operasjon == "eigenvektorer":
            result = matrix.eigenvects()
            result_latex = "Egenvektorer (komplisert format)"
        elif operasjon == "rank":
            result = matrix.rank()
            result_latex = f"\\text{{rang}}(A) = {result}"
        else:
            raise ToolError(f"Ukjent matriseoperasjon: {operasjon}")
        
        return {
            "result": str(result),
            "latex": result_latex,
            "status": "ok",
        }
    except Exception as e:
        return {"result": None, "status": "error", "message": f"Matrisefeil: {e}"}


def complex_op(operasjon: str, tall: str) -> Dict[str, Any]:
    """Operasjoner på komplekse tall."""
    try:
        z = _safe_sympify(tall, {'I': sp.I})
        operasjon = operasjon.lower().strip()
        
        if operasjon == "polar" or operasjon == "polarform":
            # Modulus og argument
            r = sp.Abs(z)
            theta = sp.arg(z)
            result = f"r = {r}, θ = {theta}"
            result_latex = f"r = {sp.latex(r)}, \\theta = {sp.latex(theta)}"
        elif operasjon == "modulus" or operasjon == "magnitude":
            result = sp.Abs(z)
            result_latex = sp.latex(result)
        elif operasjon == "conjugate" or operasjon == "konjugert":
            result = sp.conjugate(z)
            result_latex = sp.latex(result)
        elif operasjon == "real":
            result = sp.re(z)
            result_latex = sp.latex(result)
        elif operasjon == "imag":
            result = sp.im(z)
            result_latex = sp.latex(result)
        else:
            raise ToolError(f"Ukjent kompleks operasjon: {operasjon}")
        
        return {
            "result": str(result),
            "latex": result_latex,
            "status": "ok",
        }
    except Exception as e:
        return {"result": None, "status": "error", "message": f"Kompleks tallfeil: {e}"}


# All tools tilgjengelig for LLM
AVAILABLE_TOOLS = {
    "derive": derive,
    "integrate": integrate,
    "solve_equation": solve_equation,
    "solve_ode": solve_ode,
    "matrix_op": matrix_op,
    "complex_op": complex_op,
}


def get_tool_schemas() -> List[Dict[str, Any]]:
    """Returnerer tool-definisjoner for OpenAI-kompatibel API."""
    return [
        {
            "type": "function",
            "function": {
                "name": "derive",
                "description": "Deriver et matematisk uttrykk med hensyn på en variabel.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "uttrykk": {"type": "string", "description": "Uttrykket som skal deriveres, f.eks. 'x**2 + 3*x + 1'"},
                        "variabel": {"type": "string", "description": "Variabelen det skal deriveres med hensyn på (standard: 'x')"},
                    },
                    "required": ["uttrykk"],
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "integrate",
                "description": "Integrer et matematisk uttrykk med hensyn på en variabel.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "uttrykk": {"type": "string", "description": "Uttrykket som skal integreres, f.eks. 'x**2 + 1'"},
                        "variabel": {"type": "string", "description": "Variabelen det skal integreres med hensyn på (standard: 'x')"},
                    },
                    "required": ["uttrykk"],
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "solve_equation",
                "description": "Løs en algebraisk ligning.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ligning": {"type": "string", "description": "Ligningen, f.eks. 'x**2 - 4 = 0' eller '2*x + 3 = 7'"},
                        "variabel": {"type": "string", "description": "Variabelen som skal løses for (standard: 'x')"},
                    },
                    "required": ["ligning"],
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "solve_ode",
                "description": "Løs en ordinær differensialligning.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ligning": {"type": "string", "description": "ODE-en, f.eks. 'Derivative(y(t), t) + y(t) = 0'"},
                    },
                    "required": ["ligning"],
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "matrix_op",
                "description": "Utfør matriseopperasjoner (determinant, invers, egenverdier, osv.).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operasjon": {"type": "string", "description": "Operasjon: 'determinant', 'inverse', 'eigenvalues', 'rank'"},
                        "matrise_data": {"type": "array", "description": "Matrisedataene som liste av rader, f.eks. [[1, 2], [3, 4]]"},
                    },
                    "required": ["operasjon", "matrise_data"],
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complex_op",
                "description": "Operasjoner på komplekse tall.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operasjon": {"type": "string", "description": "Operasjon: 'polar', 'modulus', 'conjugate', 'real', 'imag'"},
                        "tall": {"type": "string", "description": "Komplekst tall som streng, f.eks. '1 + 2*I'"},
                    },
                    "required": ["operasjon", "tall"],
                }
            }
        },
    ]
