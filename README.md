# Venstre Norddjurs – opdateret 15. november 2026

Åbn `index.html` på telefon/PC for en statisk demonstration.

**Indhold:** kort forside, 8 kommunalbestyrelsesmedlemmer med portrætlinks og V-logoer, bestyrelsesplads, møder og udvalg, nyheder og forfatterindlæg.

**Din Avis:** Daglig søgning via GitHub Actions (`.github/workflows/opdater-nyheder.yml`) efter offentlig tilgængelige artikellinks. Forudsætter publicering af ALLE filer på GitHub Pages, Actions-rettighed til at skrive til repository og aktivering af workflow. Søgeresultater er ikke komplette og angives som omtale, **ikke** forfatterskab. Redaktionelt bekræftede indlæg kan indsættes i `data/articles.json` med `author` og `authorshipVerified: true`. For at de også vises ved lokal åbning, skal de indlejrede `EMBEDDED` data i `index.html` vedligeholdes. Ingen avisartiklers fulde tekst kopieres.

**Billeder:** Politikerportrætter forsøges hentet fra Norddjurs Kommunes officielle billedserver. Ved manglende netforbindelse eller fejl vises Venstre-markering i stedet.

**Bemærk:** Dette er en opdateret fil til gennemgang, ikke en live-ændring på en eksisterende GitHub-side.


Version 2.3 (17-11-2026): Kort Venstre-banner uden landsmødefotos, mobilnavigation med større trykflader, nyhedsfiltre og forbedret artikelvisning under politikere. Din Avis-indhentning kræver GitHub Actions og afhænger af offentlig indeksering; automatisk fundne artikler er ikke verificerede forfatterindlæg.
