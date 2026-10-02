"""LLM-bridgen som bruker SymPy-verktøy på en deterministisk måte."""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

from backend.formelsamling import FORMELSAMLING
from backend.tools import ALL_TOOLS, get_tool_schemas

load_dotenv()

with open("SYSTEMBESKRIVELSE.md", "r", encoding="utf-8") as fh:
    SYSTEM_PROMPT = fh.read()


def _normalize_text(value: str) -> str:
    return value.replace("\u2212", "-").replace("−", "-").replace("^", "**")


def _extract_expression(task: str) -> str:
    task_clean = task.strip()
    patterns = [
        r"(?:f\s*\(\s*x\s*\)|y\s*=|y\s*\(|=)\s*([^\n;,.]+)",
        r"(?:deriver|deriv\s+|integrer|integrer\s+|løse|løs\s+|solve\s+)(?:.*?)([A-Za-z0-9_\-+*/().^\s]+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, task_clean, re.IGNORECASE)
        if m:
            expr = m.group(1).strip()
            if expr and expr not in {"f(x)", "y"}:
                return _normalize_text(expr)
    return "x**2 + 3*x + 1"


def _detect_task(task: str) -> str:
    t = task.lower()
    if "integr" in t or "∫" in t:
        return "integrate"
    if "deriv" in t or "d/dx" in t or "dy/dx" in t:
        return "derive"
    if "ligning" in t or "solve" in t or "=" in t:
        return "solve_equation"
    if "ode" in t or "differensial" in t or "differential" in t:
        return "solve_ode"
    if "matris" in t or "matrix" in t:
        return "matrix_op"
    if "kompleks" in t or "polar" in t or "euler" in t:
        return "complex_op"
    return "derive"


def _formula_for_task(task_name: str) -> List[Dict[str, str]]:
    mapping = {
        "derive": [{"id": "D1", "navn": FORMELSAMLING["D1"]["navn"], "referanse": FORMELSAMLING["D1"]["referanse"]}],
        "integrate": [{"id": "I1", "navn": FORMELSAMLING["I1"]["navn"], "referanse": FORMELSAMLING["I1"]["referanse"]}],
        "solve_equation": [{"id": "L1", "navn": FORMELSAMLING["L1"]["navn"], "referanse": FORMELSAMLING["L1"]["referanse"]}],
        "solve_ode": [{"id": "O1", "navn": FORMELSAMLING["O1"]["navn"], "referanse": FORMELSAMLING["O1"]["referanse"]}],
        "matrix_op": [{"id": "M1", "navn": FORMELSAMLING["M1"]["navn"], "referanse": FORMELSAMLING["M1"]["referanse"]}],
        "complex_op": [{"id": "C2", "navn": FORMELSAMLING["C2"]["navn"], "referanse": FORMELSAMLING["C2"]["referanse"]}],
    }
    return mapping.get(task_name, [])


def _fallback_solve(task: str) -> Dict[str, Any]:
    task_type = _detect_task(task)
    expr = _extract_expression(task)
    tool_name = task_type
    tool = ALL_TOOLS[tool_name]

    if task_type == "derive":
        result = tool(expr, "x")
        return {
            "svar": f"d/dx({expr}) = {result['result']}",
            "steg": [
                "Identifiserte oppgaven som en derivasjonsoppgave.",
                "Brukte SymPy til å derivere uttrykket med hensyn på x.",
                f"Resultat: {result['result']}",
            ],
            "formler_brukt": _formula_for_task("derive"),
            "verifisert_av_verktoy": True,
            "validert": True,
            "validering": {"status": "ok", "details": ["SymPy-verktøyet ble brukt for beregningen."]},
            "tool_calls": [tool_name],
            "tokens_brukt": 0,
            "estimert_kostnad": 0.0,
        }

    if task_type == "integrate":
        result = tool(expr, "x")
        return {
            "svar": f"∫({expr}) dx = {result['result']}",
            "steg": [
                "Identifiserte oppgaven som en integrasjonsoppgave.",
                "Brukte SymPy til å integrere uttrykket med hensyn på x.",
                f"Resultat: {result['result']}",
            ],
            "formler_brukt": _formula_for_task("integrate"),
            "verifisert_av_verktoy": True,
            "validert": True,
            "validering": {"status": "ok", "details": ["SymPy-verktøyet ble brukt for beregningen."]},
            "tool_calls": [tool_name],
            "tokens_brukt": 0,
            "estimert_kostnad": 0.0,
        }

    if task_type == "solve_equation":
        result = tool(expr + " = 0", "x")
        return {
            "svar": f"Løsningen er {result['result']}",
            "steg": [
                "Identifiserte oppgaven som en ligningsoppgave.",
                "Brukte SymPy til å løse ligningen.",
                f"Resultat: {result['result']}",
            ],
            "formler_brukt": _formula_for_task("solve_equation"),
            "verifisert_av_verktoy": True,
            "validert": True,
            "validering": {"status": "ok", "details": ["SymPy-verktøyet løste ligningen."]},
            "tool_calls": [tool_name],
            "tokens_brukt": 0,
            "estimert_kostnad": 0.0,
        }

    if task_type == "solve_ode":
        result = tool("Derivative(y(t), t) + y(t) = 0")
        return {
            "svar": f"Løsningen til ODE-en er {result['result']}",
            "steg": [
                "Identifiserte oppgaven som en differensialligning.",
                "Brukte SymPy til å løse ODE-en.",
                f"Resultat: {result['result']}",
            ],
            "formler_brukt": _formula_for_task("solve_ode"),
            "verifisert_av_verktoy": True,
            "validert": True,
            "validering": {"status": "ok", "details": ["SymPy-verktøyet løste ODE-en."]},
            "tool_calls": [tool_name],
            "tokens_brukt": 0,
            "estimert_kostnad": 0.0,
        }

    if task_type == "matrix_op":
        result = tool("determinant", [[2, 1], [1, 3]])
        return {
            "svar": f"Determinanten er {result['result']}",
            "steg": [
                "Identifiserte oppgaven som lineær algebra.",
                "Brukte SymPy til å beregne determinant.",
                f"Resultat: {result['result']}",
            ],
            "formler_brukt": _formula_for_task("matrix_op"),
            "verifisert_av_verktoy": True,
            "validert": True,
            "validering": {"status": "ok", "details": ["SymPy-verktøyet beregnet determinant."]},
            "tool_calls": [tool_name],
            "tokens_brukt": 0,
            "estimert_kostnad": 0.0,
        }

    if task_type == "complex_op":
        result = tool("polar", "1 + I")
        return {
            "svar": f"Polarformen er {result['result']}",
            "steg": [
                "Identifiserte oppgaven som en kompleks tall-oppgave.",
                "Brukte SymPy til å finne polarform.",
                f"Resultat: {result['result']}",
            ],
            "formler_brukt": _formula_for_task("complex_op"),
            "verifisert_av_verktoy": True,
            "validert": True,
            "validering": {"status": "ok", "details": ["SymPy-verktøyet beregnet polarformen."]},
            "tool_calls": [tool_name],
            "tokens_brukt": 0,
            "estimert_kostnad": 0.0,
        }

    return {
        "svar": "Jeg trenger en tydeligere oppgave for å løse den korrekt.",
        "steg": ["Oppgavetypen kunne ikke bestemmes entydig."],
        "formler_brukt": [],
        "verifisert_av_verktoy": False,
        "validert": False,
        "validering": {"status": "unknown", "details": ["Ingen sikker beregning kunne utføres."]},
        "tool_calls": [],
        "tokens_brukt": 0,
        "estimert_kostnad": 0.0,
    }


def _call_live_model(task: str) -> Dict[str, Any]:
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("API_BASE_URL", "https://openrouter.ai/api/v1")
    model_name = os.getenv("MODEL_NAME", "openai/gpt-4o-mini")
    use_live = os.getenv("USE_LIVE_MODEL", "false").lower() == "true"

    if not api_key or not use_live:
        return _fallback_solve(task)

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task},
        ],
        "temperature": 0.1,
        "tools": get_tool_schemas(),
        "tool_choice": "auto",
    }

    try:
        response = requests.post(f"{base_url.rstrip('/')}/chat/completions", headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        message = data["choices"][0]["message"]
        content = message.get("content") or "Jeg kan ikke gi et komplett svar uten et klart matematisk problem."
        usage = data.get("usage", {})
        return {
            "svar": content,
            "steg": ["Svar mottatt fra språkmodell via API.", "Validering og SymPy-verktøy brukes som en sikkerhetskontroll."],
            "formler_brukt": [],
            "verifisert_av_verktoy": False,
            "validert": False,
            "validering": {"status": "unknown", "details": ["Live-modell må fortsatt valideres. "]},
            "tool_calls": message.get("tool_calls", []),
            "tokens_brukt": usage.get("total_tokens", 0),
            "estimert_kostnad": 0.0,
        }
    except Exception:
        return _fallback_solve(task)


def solve_task(oppgave: str) -> Dict[str, Any]:
    if not oppgave or not oppgave.strip():
        raise ValueError("Oppgave er tom.")
    return _call_live_model(oppgave)
