#!/bin/bash
# job NAME A B ORDERS MASK   (mid = thispassword always; 4 parts in parallel)
cd "$(dirname "$0")"; mkdir -p runs
CONS="-c terminal terminal.bin -c short short.bin -c cosmic cosmic.bin"
job() {
  name=$1 A=$2 B=$3 ord=$4 mask=$5
  # planted control through the same path: row 1 of A, last row of B
  a=$(head -1 $A); b=$(tail -1 $B)
  if [ $((ord & 2)) -ne 0 ]; then cand="${b}${a}thispassword"; else cand="${a}${b}thispassword"; fi
  if [ $((mask & 8)) -ne 0 ]; then f=8; elif [ $((mask & 4)) -ne 0 ]; then f=4; elif [ $((mask & 2)) -ne 0 ]; then f=2; else f=1; fi
  python3 plant.py runs/$name.ctl.bin "$cand" $f md5 >/dev/null
  head -1 $A > runs/$name.ctlA
  n=$(./h3 -c ctl runs/$name.ctl.bin -f $mask --cross runs/$name.ctlA $B --mid thispassword --order $ord 2>/dev/null | grep -c '^FLAG	ctl.*pad10')
  echo "CONTROL $name form$f fired=$n" | tee -a runs/controls.log
  [ "$n" -ge 1 ] || { echo "CONTROL FAILED $name"; exit 1; }
  for p in 0 1 2 3; do
    ./h3 $CONS -f $mask --cross $A $B --mid thispassword --order $ord --part $p 4 > runs/$name.p$p.flags 2> runs/$name.p$p.err &
  done
  wait
  echo "DONE $name $(date -u +%H:%M:%S)" | tee -a runs/progress.log
}
job_base() {
  name=$1; shift
  cat "$@" | ./h3 $CONS -f 15 > runs/$name.p0.flags 2> runs/$name.p0.err
  echo "DONE $name $(date -u +%H:%M:%S)" | tee -a runs/progress.log
}
echo "START $(date -u +%H:%M:%S)" >> runs/progress.log
job_base base_all msl_all.txt msl_rgb.txt n2_cands.txt msl_rem.txt msl_adj.txt msl_walk.txt cards.txt lw_core.txt lw_loc.txt lw_words.txt lw_adj.txt lw_walk.txt subs.txt
job core_all   msl_all.txt  lw_core.txt  3 12
job core_rem   msl_rem.txt  lw_core.txt  3 15
job core_n2    n2_cands.txt lw_core.txt  3 15
job core_rgb   msl_rgb.txt  lw_core.txt  3 15
job core_cards cards.txt    lw_core.txt  3 15
job walk_lw    msl_walk.txt lw_walk.txt  3 15
job walk_words msl_walk.txt lw_words.txt 3 15
job new_loc_ab msl_new.txt  lw_loc.txt   1 14
job new_loc_ba msl_new.txt  lw_loc.txt   2 15
job all_words_ab msl_all.txt lw_words.txt 1 14
job all_words_ba msl_all.txt lw_words.txt 2 15
job rgb_words_ab msl_rgb.txt lw_words.txt 1 14
job rgb_words_ba msl_rgb.txt lw_words.txt 2 15
job adj_adj    msl_adj.txt  lw_adj.txt   3 15
echo "ALLDONE $(date -u +%H:%M:%S)" >> runs/progress.log
