# Check two numeric-text CSV risks

Save three source files in a NEW empty lesson folder.

    python make_sample.py
    python excelcsv.py sample/orders.csv
    python -m unittest -v

Two Windows and two Ubuntu full replays run exact visible source versions. Final 34 small fixture tests pass (Unix pipe skips on Windows); symlink creation can skip where unavailable. Displayed stdout is first Windows output, not normalized or mixed. Pair differences are unittest time.
Only link/error changes: refuse input/ancestor symbolic links/reparse points, hardlinks, special files and traversal before reading. Read/metadata errors exit 2; error text now preserves an explicit refusal reason. Setup refuses linked parents/traversal and existing sample paths, without reset/deletion.
Original strict UTF-8/BOM CSV parsing, unique/nonblank headers, row widths, ASCII digit patterns, stripped surrounding spaces, examples, counts and output remain unchanged. Only leading-zero and 16+ digit strings are flagged. No-hit output still does not certify Excel compatibility, formulas, dates, scientific notation or other conversions.
The checker has no write/move/delete/network code but reads all CSV rows into memory. No size/time/resource limit, atomic snapshot or hostile-race defense. Stop editors/sync. Output includes column names and example values which may be private. Small fictional fixtures are not proof on every filesystem. No Excel/desktop Windows/macOS recording. Recorder removes only its own temporary fixture folder. Decisions/feedback are teaching text, not recorded output.

MIT code. Python separately licensed/not included.

Reference: https://docs.python.org/3/library/os.html
Reference: https://support.microsoft.com/en-us/excel/keeping-leading-zeros-and-large-numbers

Windows paired run: https://github.com/faiz12321/lesson-lab/actions/runs/38977458108
Ubuntu paired run: https://github.com/faiz12321/lesson-lab/actions/runs/38977558188
