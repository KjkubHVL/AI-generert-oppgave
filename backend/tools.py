"""SymPy-verktøy for MatteHjelpen."""

from __future__ import annotations

from typing import Any, Dict, List

import sympy as sp


class ToolError(RuntimeError):
    pass


def _to_expr(value: str, var_name: str = "x") -> sp.Expr:
    text = str(value).strip()
    text = text.replace("^", "**").replace("−", "-").replace("–", "-")
    text = text.replace("×", "*").replace("÷", "/")
    text = text.replace("\u00a0", " ")
    # Convert implicit multiplication like 2x -> 2*x
    text = __import__("re").sub(r"(?<=[0-9A-Za-z)])(?=[A-Za-z(])", "*", text)
    local_ns = {var_name: sp.Symbol(var_name), "x": sp.Symbol("x"), "t": sp.Symbol("t"), "y": sp.Function("y"), "I": sp.I, "pi": sp.pi, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "exp": sp.exp, "ln": sp.ln, "sqrt": sp.sqrt, "log": sp.log, "E": sp.E}
    try:
        return sp.sympify(text, locals=local_ns)
    except Exception as exc:
        raise ToolError(f"Kunne ikke tolke uttrykket: {text}. Feil: {exc}")


def derive(uttrykk: str, variabel: str = "x") -> Dict[str, Any]:
    try:
        var = sp.Symbol(variabel)
        expr = _to_expr(uttrykk, variabel)
        result = sp.simplify(sp.diff(expr, var))
        return {"result": str(result), "latex": sp.latex(result), "status": "ok"}
    except Exception as exc:
        return {"result": None, "status": "error", "message": str(exc)}


def integrate(uttrykk: str, variabel: str = "x") -> Dict[str, Any]:
    try:
        var = sp.Symbol(variabel)
        expr = _to_expr(uttrykk, variabel)
        result = sp.simplify(sp.integrate(expr, var))
        return {"result": str(result), "latex": sp.latex(result), "status": "ok"}
    except Exception as exc:
        return {"result": None, "status": "error", "message": str(exc)}


def solve_equation(ligning: str, variabel: str = "x") -> Dict[str, Any]:
    try:
        if "=" not in ligning:
            raise ToolError("Ligningen må inneholde '='.")
        lhs_str, rhs_str = ligning.split("=", 1)
        var = sp.Symbol(variabel)
        lhs = _to_expr(lhs_str, variabel)
        rhs = _to_expr(rhs_str, variabel)
        solutions = sp.solve(sp.Eq(lhs, rhs), var)
        return {"result": str(solutions), "latex": sp.latex(solutions), "status": "ok"}
    except Exception as exc:
        return {"result": None, "status": "error", "message": str(exc)}


def solve_ode(ligning: str) -> Dict[str, Any]:
    try:
        t = sp.symbols("t")
        y = sp.Function("y")
        normalized = ligning.replace("dy/dt", "Derivative(y(t), t)").replace("y'", "Derivative(y(t), t)")
        eq = sp.sympify(normalized, locals={"t": t, "y": y, "Derivative": sp.Derivative, "sin": sp.sin, "cos": sp.cos, "exp": sp.exp})
        if not isinstance(eq, sp.Equality):
            eq = sp.Eq(sp.diff(y(t), t), eq)
        solution = sp.dsolve(eq, ics={})
        return {"result": str(solution), "latex": sp.latex(solution), "status": "ok"}
    except Exception as exc:
        return {"result": None, "status": "error", "message": str(exc)}


def matrix_op(operasjon: str, matrise: List[List[Any]]) -> Dict[str, Any]:
    try:
        A = sp.Matrix(matrise)
        op = operasjon.lower().strip()
        if op in {"determinant", "det"}:
            result = A.det()
        elif op in {"inverse", "inv"}:
            result = A.inv()
        elif op in {"eigenvalues", "eigenverdier"}:
            result = A.eigenvals()
        elif op in {"rank", "rang"}:
            result = A.rank()
        else:
            raise ToolError(f"Ukjent operasjon: {operasjon}")
        return {"result": str(result), "latex": sp.latex(result), "status": "ok"}
    except Exception as exc:
        return {"result": None, "status": "error", "message": str(exc)}


def complex_op(operasjon: str, tall: str) -> Dict[str, Any]:
    try:
        z = _to_expr(tall, "x")
        op = operasjon.lower().strip()
        if op in {"polar", "polarform"}:
            result = (sp.Abs(z), sp.arg(z))
        elif op in {"modulus", "abs"}:
            result = sp.Abs(z)
        elif op in {"conjugate", "konjugert"}:
            result = sp.conjugate(z)
        elif op in {"real", "re"}:
            result = sp.re(z)
        elif op in {"imag", "im"}:
            result = sp.im(z)
        else:
            raise ToolError(f"Ukjent kompleks operasjon: {operasjon}")
        return {"result": str(result), "latex": sp.latex(result), "status": "ok"}
    except Exception as exc:
        return {"result": None, "status": "error", "message": str(exc)}


ALL_TOOLS = {
    "derive": derive,
    "integrate": integrate,
    "solve_equation": solve_equation,
    "solve_ode": solve_ode,
    "matrix_op": matrix_op,
    "complex_op": complex_op,
}


def get_tool_schemas() -> List[Dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "derive",
                "description": "Deriver et matematisk uttrykk.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "uttrykk": {"type": "string"},
                        "variabel": {"type": "string"},
                    },
                    "required": ["uttrykk"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "integrate",
                "description": "Integrer et matematisk uttrykk.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "uttrykk": {"type": "string"},
                        "variabel": {"type": "string"},
                    },
                    "required": ["uttrykk"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "solve_equation",
                "description": "Løs en ligning.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ligning": {"type": "string"},
                        "variabel": {"type": "string"},
                    },
                    "required": ["ligning"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "solve_ode",
                "description": "Løs en differensialligning.",
                "parameters": {"type": "object", "properties": {"ligning": {"type": "string"}}, "required": ["ligning"]},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "matrix_op",
                "description": "Utfør matrise-operasjon.",
                "parameters": {"type": "object", "properties": {"operasjon": {"type": "string"}, "matrise": {"type": "array"}}, "required": ["operasjon", "matrise"]},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "complex_op",
                "description": "Utfør kompleks operasjon.",
                "parameters": {"type": "object", "properties": {"operasjon": {"type": "string"}, "tall": {"type": "string"}}, "required": ["operasjon", "tall"]},
            },
        },
    ]
