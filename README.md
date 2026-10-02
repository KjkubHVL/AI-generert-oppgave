# MatteHjelpen

Dette repoet inneholder en Python/FastAPI-app som løser førsteårs matteoppgaver med en kombinasjon av språkmodell og SymPy-verktøy.

## Kjør lokalt

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn backend.main:app --reload
```

Åpne `http://localhost:8000` i nettleseren.

## Prinsipp

- Modellen kan forklare og foreslå metode.
- SymPy gjør all reell symbolsk og numerisk beregning.
- Validering skjer i backend før responsen returneres.

## FastAPI-endepunkt

- `POST /solve` med JSON: `{ "oppgave": "Deriver f(x)=x^2+3x+1" }`

## Selftest

```bash
python scripts/selftest.py --strict
```
