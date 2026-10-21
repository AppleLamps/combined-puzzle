# Experiments log (repo vs handoff prose)

| Experiment | Handoff §9 / §8 | Repo |
|------------|-----------------|------|
| faed letter **deletion** (not zeroing) | Handoff §9 “deletion has not been tried” (community notes); **repo footnote** in `uploads/GSMG-handoff.md` §9 | **Tried:** mask6 six positions all 2⁶ subsets (`07-deletion-sweep.md`); filler deletion depths 1–4+ (`08`–`12`); door-index G7 (`16-round8`). Not exhaustive on full faed/dbbi. |
| dbbi **200k shuffle** null | §6.3 / §8.1 letter-shuffle evidence | **Not reproduced.** `round2_battery.py` runs a **simplified** random B/Y string null vs `BBBBYBBBYYBBBBYBBYYBFYY` (`ledger/15-team-audit.md` C2). |
| mask6 **zero** | §6.3 search pins | `step3_mask.py`, documented |

When citing handoff §9, treat deletion as **partially tried** in this repo.

`uploads/GSMG-handoff.md` is kept byte-identical to the second build (sha256 `442d502f…f6d7f6`). An earlier commit edited its §9 line in place to point here; that edit was reverted so the source pack matches its published hash. This table is the repo's note on §9.
