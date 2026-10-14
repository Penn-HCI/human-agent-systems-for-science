# Project memory

This folder is an Obsidian vault holding the memory for a scientific investigation.

## De novo analysis
Please do not read the published HALIE paper or related blog posts or other public communications — the analysis in this repository is a reproduction of it from the ground up, and I want to avoid tainting with the past analysis results.

## General guidance to keep this usable
* Notes should be very readable. Prefer concision over verbosity. Save important results, consider putting details into supplemental investigation files rather than the main file
* Help the user attribute the findings quickly
	* For empirical findings, in a drop-down (closed by default), allow a user to look at particular excerpts of analysis scripts that produced a result, commands to re-run to replicate the result, and (optionally, much more rarely) bits of raw data that show it themselves
	* For sources, in a drop-down, include the original quote from the paper, a link to the paper, and if possible, a page number

## Folders
- `data/` — datasets. Don't modify.
- `sources/` — original papers and other source files.
- `investigations/` — one note per investigation (use `templates/investigation.md`).
- `related-work/` — one note per paper or source (use `templates/related-work.md`).
- `datasets/` — one note per dataset: files, structure, quirks.
- `concepts/` — one note per recurring idea or measure.
- `analysis/` — scripts that investigations ran. Link to them from the note.
- `transcripts/` — raw Claude Code session logs, saved with `tools/save_transcript.py`.
- `index.md` — a list of every note, with a one-line summary. Update it when you add a note.
- `log.md` — an append-only record of what was done (`## [date] type | title`).

## Affirmed passages
- `> [!affirmed]` callouts are findings a person has checked and stands behind.
- Treat them as established; build on them rather than re-deriving or contradicting them.
- If evidence contradicts one, say so in a new `> [!agent]` callout next to it. Don't edit it.
- Never create, edit, or remove an affirmed callout. Only people do that.

## Marking what you add
- Notes you create get `added_by: claude` in their frontmatter.
- When you add to a note someone else wrote, put your addition in a `> [!agent]` callout.

## Before starting a new investigation
- Read the affirmed callouts across `investigations/` and `related-work/` first.
- Record what you did (code, queries, steps) so the finding can be traced back.
