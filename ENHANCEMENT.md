## Temporarily save input

If parts of a round are provided in calculator-view and navigation changes, this input should be saved temporarily

**Acceptance criteria:**
* [ ] Inputs survive navigating Calculator → History → Calculator
* [ ] After saving or resetting, the inputs are empty again

## Restrict proxy calculations to score-differential only

When calculating on behalf of another player (calculator-hcpi != statistic-hcpi) - only score-differential should be calculated (no handicap-history, so handicap-calculation possible)...

**Acceptance criteria:**
* [ ] If the entered HCPI differs from the stored one, only the score differential is shown
* [ ] No projected handicap and no "save" action in that case

## Save course templates (prefill course rating and slope)

**Description:**
When entering a round, course rating and slope currently have to be typed in every time. I'd like to save course templates and select them when creating a round.

**Requirements:**
* A template contains: course name, tee (e.g. blue/yellow/red), number of holes (9/18), course rating, slope, optionally par
* Create, edit and delete templates
* When creating a new round, selecting a template prefills the fields (still manually overridable)
* Optional: "Save as template" from the values entered for a round
* Persisted locally (same mechanism as rounds)

**Acceptance criteria:**
* [ ] A template "Course X / Blue / 9 holes" can be saved and survives a restart
* [ ] Selecting it prefills course rating and slope correctly
* [ ] Editing or deleting a template does not change existing rounds

## Highlight rounds counted towards the handicap in the results overview

**Description:**
The results overview doesn't show which rounds actually count towards the current handicap. These should be visually highlighted.

**Requirements:**
* Rounds used in the calculation are highlighted (e.g. badge, bold text or background colour, ideally with a legend)
* Highlighting follows exactly the handicap calculation logic (under WHS: best 8 of the last 20 score differentials)
* Highlighting updates automatically when rounds are added, changed or deleted

**9-hole rounds:** Resolved - they are already stored as an 18-hole-equivalent differential (expected-score method / SD from the PDF), so they count like any other round; nothing is combined.

**Acceptance criteria:**
* [ ] Exactly the rounds used by the calculation are highlighted
* [ ] With fewer than 20 rounds, the WHS rule for the number of counting rounds applies
* [ ] The highlight is recognisable without colour (e.g. icon/text)