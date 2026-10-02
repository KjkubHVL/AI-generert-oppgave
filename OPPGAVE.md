# Innleveringsoppgave: MatteHjelpen

## Oppgave

Bygg en webapp for førsteårs matteoppgaver. Appen skal:

1. Ta imot en matteoppgave som tekst.
2. Kalle en språkmodell via API.
3. Bruke SymPy for all symbolsk og numerisk beregning.
4. Gi stegvis løsning med forklaring.
5. Knytte hvert steg til en formel-ID fra formelsamlingen.
6. Validere svaret numerisk og vise dette i frontend.
7. Returnere strukturert JSON fra backend.

## Omfang

- derivasjon
- integrasjon
- lineær algebra
- differentiallikninger
- komplekse tall

## Krav

- Ingen hardkodede API-nøkler.
- Alt som faktisk regnes må gjøres i SymPy-verktøyet.
- Bevisoppgaver skal merkes som “ikke verifisert av verktøy”.
- Frontend skal vise løsningen på en tydelig måte.
