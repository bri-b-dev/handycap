# PLAN.md - Refactor + Enhancements

Umsetzungsplan für die Anforderungen aus `ENHANCEMENT.md`. Reihenfolge: erst Sicherheitsnetz und Refactor, dann Features.

## Entscheidungen

- WHS-Regel "beste N der **letzten 20**" wird korrigiert (bisher: alle Runden). Gespeicherte Handicaps ändern sich ggf. beim nächsten Recalc, ein Hinweis wird angezeigt.
- Fremdberechnung (eingegebener HCPI != gespeicherter HCPI): nur Score Differential, kein Speichern, keine Projektion.
- Zwischenspeichern der Rechner-Eingaben: `sessionStorage` genügt.
- Vorlagen: Tee ist Freitext. Damen/Herren = getrennte Vorlagen (z. B. "rot, Damen").
- Migration: manuelle Runden (`courseName` = `"CR/Slope"`) werden zu `courseRating`/`slope` migriert. Der PDF-Import speichert künftig `holes`, `courseRating`, `slope`, `tee`, `par`; bereits importierte Runden werden beim erneuten Import angereichert (statt als Duplikat übersprungen). `holes` unbekannt = leer.
- 9-Loch-Runden liegen bereits als 18-Loch-Differential vor (Expected-Score-Methode bzw. SD aus PDF). Das Highlighting kombiniert nichts.

## Phase 0: Sicherheitsnetz (`b/0-tests`)

1. Vitest einrichten (`npm run test`).
2. Tests für `computeBaseHandicap` / `applyCap` (0, 1, 3, 4, 6, 19, 20, 21 Runden; 26,5-Regel; Soft/Hard Cap).
3. `AGENTS.md` korrigieren (Anpassungstabelle, 9-Loch-Beschreibung).

## Phase 1: Domänenschicht

4. `utils/handicap.ts`: `calculateHistory(rounds)` (letzte 20, Cap, `counting`-Flag pro Runde) und `projectHandicap(rounds, newRound)`.
5. Composable `useResults()` (`load`, `add`, `remove`, `recalc`) ersetzt die drei Kopien der Logik.
6. Views umstellen (Verhalten unverändert, außer Korrektur aus 4).
7. Recalc beim Start + Hinweis, falls sich Handicaps durch die Korrektur ändern.

## Phase 2: Datenmodell (Dexie v5, bestehende Versionen unverändert)

8. `Result`: optionale Felder `holes`, `courseRating`, `slope`, `pcc`, `tee`, `par`.
9. Tabelle `courseTemplates` (`++id, name`): Name, Tee, Löcher, CR, Slope, optional Par.
10. Upgrade-Migration für manuelle Runden; Import speichert neue Felder und reichert vorhandene Runden an.
11. Test: Bearbeiten/Löschen einer Vorlage ändert bestehende Runden nicht (Werte werden kopiert).

## Phase 3: Features (je Branch/PR)

12. **Highlighting** in der Ergebnistabelle: `counting` aus 4, Icon + Fettdruck + Legende (ohne Farbe erkennbar).
13. **Zwischenspeichern**: `useCalculatorDraft` (Modul-Store + `sessionStorage`), leeren bei Speichern/Reset.
14. **Fremdberechnung**: nur SD anzeigen, kein Speichern; `inconsistentIndex`-Fehler entfällt.
15. **Vorlagen**: Verwaltung unter Einstellungen, Auswahl im Rechner, "Als Vorlage speichern"; Texte in `de.ts` + `en.ts`.

## Tests als Akzeptanz

Kriterien aus `ENHANCEMENT.md` werden, wo möglich, zu Tests (`fake-indexeddb` für Persistenz).
