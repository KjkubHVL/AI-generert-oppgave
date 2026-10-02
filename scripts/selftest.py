#!/usr/bin/env python3
import argparse
from pathlib import Path

REQUIRED = [
    "README.md",
    "OPPGAVE.md",
    "SYSTEMBESKRIVELSE.md",
    "EVALUERING.md",
    ".env.example",
    "requirements.txt",
    "backend/__init__.py",
    "backend/formelsamling.py",
    "backend/tools.py",
    "backend/llm_client.py",
    "backend/validator.py",
    "backend/main.py",
    "frontend/index.html",
    "scripts/selftest.py",
]


def check_file(path: str) -> bool:
    return Path(path).exists()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    missing = [item for item in REQUIRED if not check_file(item)]
    if missing:
        print("SELFTEST: FAIL")
        for item in missing:
            print(f" - Missing: {item}")
        return 1

    try:
        import backend.main
        from fastapi.testclient import TestClient

        client = TestClient(backend.main.app)
        health = client.get("/health")
        if health.status_code != 200:
            raise RuntimeError(f"/health failed: {health.status_code}")

        solve = client.post("/solve", json={"oppgave": "Deriver f(x)=x^2+3*x+1"})
        if solve.status_code != 200:
            raise RuntimeError(f"/solve failed: {solve.status_code} {solve.text}")

        body = solve.json()
        if not isinstance(body.get("svar"), str):
            raise RuntimeError("Missing string svar")
        if not isinstance(body.get("steg"), list):
            raise RuntimeError("Missing list steg")
        if not isinstance(body.get("formler_brukt"), list):
            raise RuntimeError("Missing list formel_brukt")
        if not isinstance(body.get("validert"), bool):
            raise RuntimeError("Missing bool validert")

    except Exception as exc:
        print("SELFTEST: FAIL")
        print(f" - {exc}")
        return 1

    print("SELFTEST: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
