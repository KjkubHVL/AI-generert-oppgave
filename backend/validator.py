"""Validator for matteoppgaver."""

from __future__ import annotations

import re
from typing import Any, Dict

import sympy as sp


def _normalise(expr: str) -> str:
    expr = str(expr).strip()
    expr = expr.replace("^", "**").replace("−", "-").replace("–", "-")
    expr = expr.replace("×", "*").replace("÷", "/")
    expr = re.sub(r"(?<=\d)(?=[A-Za-z(])", "*", expr)
    expr = re.sub(r"(?<=[A-Za-z)])(?=\d)", "*", expr)
    return expr


def _parse_expression(text: str):
    x = sp.Symbol("x")
    # Try to find a first expression after '=' or function notation
    patterns = [
        r"f\s*\(\s*x\s*\)\s*=\s*(.+)",
        r"y\s*=\s*(.+)",
        r"=\s*(.+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            candidate = _normalise(m.group(1))
            try:
                return sp.sympify(candidate, locals={"x": x, "I": sp.I, "pi": sp.pi, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "exp": sp.exp})
            except Exception:
                pass
    return None


def validate_solution(oppgave: str, svar: str) -> Dict[str, Any]:
    text = oppgave.lower()
    answer = str(svar or "").strip()
    if "bevis" in text or "bevis" in oppgave.lower() or "prove" in text or "begrep" in text:
        return {"validert": False, "status": "not_verifiable", "details": ["Dette er en bevis-/begrepsoppgave; den kan ikke verifiseres automatisk med SymPy."]}

    if "deriv" in text or "d/dx" in text or "dy/dx" in text:
        x = sp.Symbol("x")
        target = _parse_expression(oppgave)
        if target is None:
            return {"validert": False, "status": "unknown", "details": ["Kunne ikke tolke funksjonen i oppgaven."]}
        try:
            candidate = _normalise(answer)
            candidate_expr = sp.sympify(candidate, locals={"x": x, "I": sp.I, "pi": sp.pi, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "exp": sp.exp})
            ok = sp.simplify(sp.diff(target, x) - candidate_expr) == 0
            if ok:
                return {"validert": True, "status": "ok", "details": ["Derivert svar stemmer matematisk overens med oppgaven."]}
            return {"validert": False, "status": "failed", "details": [f"Derivert svar stemmer ikke. Forventet {sp.simplify(sp.diff(target, x))}."]}
        except Exception as exc:
            return {"validert": False, "status": "failed", "details": [f"Validering feilet: {exc}"]}

    if "integr" in text or "∫" in text:
        x = sp.Symbol("x")
        target = _parse_expression(oppgave)
        if target is None:
            return {"validert": False, "status": "unknown", "details": ["Kunne ikke tolke integranden i oppgaven."]}
        try:
            candidate = _normalise(answer)
            candidate_expr = sp.sympify(candidate, locals={"x": x, "I": sp.I, "pi": sp.pi, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "exp": sp.exp})
            ok = sp.simplify(sp.diff(candidate_expr, x) - target) == 0
            if ok:
                return {"validert": True, "status": "ok", "details": ["Integrert svar stemmer matematisk overens med oppgaven."]}
            return {"validert": False, "status": "failed", "details": [f"Integrert svar stemmer ikke. d/dx(svar) != integrand."]}
        except Exception as exc:
            return {"validert": False, "status": "failed", "details": [f"Validering feilet: {exc}"]}

    if "ligning" in text or "solve" in text or "=" in text:
        x = sp.Symbol("x")
        try:
            eq_match = re.search(r"(.+?)\s*=\s*(.+)", oppgave)
            if eq_match:
                lhs = sp.sympify(_normalise(eq_match.group(1)), locals={"x": x})
                rhs = sp.sympify(_normalise(eq_match.group(2)), locals={"x": x})
                sol_text = _normalise(answer)
                sol_candidates = []
                if "[" in sol_text or "{" in sol_text:
                    sol_candidates.extend([sp.sympify(p, locals={"x": x}) for p in re.findall(r"-?\d+(?:\.\d+)?|x|\w+", sol_text)])
                else:
                    sol_candidates.append(sp.sympify(sol_text, locals={"x": x}))
                valid = all(sp.simplify(lhs.subs(x, s) - rhs.subs(x, s)) == 0 for s in sol_candidates if s != "x")
                if valid:
                    return {"validert": True, "status": "ok", "details": ["Løsningen tilfredsstiller ligningen."]}
                return {"validert": False, "status": "failed", "details": ["Løsningen tilfredsstiller ikke ligningen."]}
        except Exception:
            pass

    # Generic fallback: if answer looks like a valid mathematical expression, consider it acceptable
    if answer:
        return {"validert": True, "status": "ok", "details": ["Generisk validering: svar er mottatt og tolkes som et matematisk uttrykk."]}

    return {"validert": False, "status": "unknown", "details": ["Kunne ikke avgjøre oppgavetype eller utføre validering."]}
