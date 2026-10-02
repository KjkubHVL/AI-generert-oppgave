"""FastAPI-app for MatteHjelpen."""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.llm_client import solve_task
from backend.validator import validate_solution

app = FastAPI(title="MatteHjelpen", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


@app.get("/")
def read_root():
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "MatteHjelpen backend kjører."}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/config")
def config():
    return {
        "model": os.getenv("MODEL_NAME", "ukjent"),
        "api_base": os.getenv("API_BASE_URL", "ukjent"),
        "use_live_model": os.getenv("USE_LIVE_MODEL", "false").lower() == "true",
    }


@app.post("/solve")
def solve_endpoint(payload: dict):
    try:
        oppgave = payload.get("oppgave", "")
        if not isinstance(oppgave, str):
            raise ValueError("Feltet 'oppgave' må være tekst.")
        if not oppgave.strip():
            raise ValueError("Oppgave er tom.")

        result = solve_task(oppgave)
        validation = validate_solution(oppgave, result.get("svar", ""))
        result["validert"] = validation.get("validert", False)
        result["validering"] = validation
        result.setdefault("tokens_brukt", 0)
        result.setdefault("estimert_kostnad", 0.0)
        result.setdefault("formler_brukt", [])
        result.setdefault("steg", [])
        result.setdefault("verifisert_av_verktoy", bool(result.get("tool_calls")))
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Uventet feil: {exc}") from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
