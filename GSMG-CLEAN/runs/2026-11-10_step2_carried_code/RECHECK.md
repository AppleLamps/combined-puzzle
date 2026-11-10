# Recheck against the restored plaintext files

`results.json` was produced while three files in `data/` still had their CRLF line ends converted
to LF (see 16 section 9). The registry this run compares against draws four of its 269 strings from
those files: the Phase 2 clear text, the Phase 3 riddles, and two Phase 3.2 passages cut by byte offset.

After the files were restored, the measurement on the real ordinary cells was repeated with the
sealed script version (`method.script_sha256` in `PREREG.json`):

| | damaged copies | restored files |
|---|---|---|
| registry | 269 strings, 24,897 characters | 269 strings, 24,903 characters |
| longest exact run, 83 and 84 cells | 7 digits (`5375523`, sha256 of the Phase 3 answer in decimal, a=0) | the same |
| longest relabelled window, 83 and 84 cells | 10 cells (the URL as a decimal number) | the same |

The outcome is unchanged: null, far below the acceptance rule (12 digits or 20 cells).

The 200-shuffle controls were not repeated on the restored files. They depend on the registry only
through those six added characters, and the real values sit below the control maxima recorded in
`results.json` (8 to 10 digits, 13 to 14 cells) either way.
