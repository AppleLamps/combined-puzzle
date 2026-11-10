# Void run

This run does not count. Its planted control did not fire: the control tried to spell a phrase
through the gap sums, but a stretch of one cell can only hold 1 to 9, so most letters were
unreachable and the control text came out as `iaieiheleitwiresiftheci`.

The real outputs it wrote are kept in `results.json` (best score -6.76, below the control
median of -6.73, no exact hit). They are not a recorded null, because a null counts only when
its control fires. The rerun with a constructible control is `runs/2026-11-10_step2_gap_sums_v2`.
