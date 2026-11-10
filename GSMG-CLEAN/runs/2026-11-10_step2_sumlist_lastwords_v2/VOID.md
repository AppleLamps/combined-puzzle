# Void run

This run does not count. Its planted control did not fire: the reader's count-from-0 and
count-from-1 labels were swapped, so the control, which addressed count-from-1, was read one
position off and came back as noise.

The real outputs are kept in `results.json` and `outputs.jsonl` (best score -5.16, below the
control median of -4.92). Both counting conventions were in the family, so the selections are
the same ones the corrected run makes, but they are not a recorded null, because a null counts
only when its control fires. The corrected rerun is `runs/2026-11-10_step2_sumlist_lastwords_v3`.
