# MatteHjelpen – systembeskrivelse

## Mål

Lag en webapp i Python som løser førsteårsoppgaver i matte: derivasjon, integrasjon, lineær algebra, differensiallikninger og komplekse tall.

## Arkitektur

- Backend: FastAPI
- Frontend: enkel HTML/JS
- LLM: OpenAI-kompatibel API via `.env`
- Beregninger: SymPy i `backend/tools.py`
- Validering: `backend/validator.py`
- Formelsamling: `backend/formelsamling.py`

## Prinsipp

- Modellen er en forklarende lærer.
- Verktøyet er det som faktisk regner.
- All beregning skal skje i SymPy.
- Bevis og begrepsoppgaver skal håndteres ærlig med tydelig flagg om at de ikke er verifisert av verktøy.

## Endepunkt

`POST /solve` tar inn JSON:

```json
{ "oppgave": "Deriver f(x)=x^2+3x+1" }
```

## Responsformat

```json
{
  "svar": "...",
  "steg": ["..."],
  "formler_brukt": [{"id": "D1", "navn": "Potensregel", "referanse": "Edwards & Penney"}],
  "verifisert_av_verktoy": true,
  "validert": true,
  "validering": {"status": "ok", "details": ["..."]},
  "tokens_brukt": 0,
  "estimert_kostnad": 0.0
}
```
