# Before Excel import: flag leading zeros and long digit strings

AI Tools That Work, build session 33. Python 3 standard library, Windows and Ubuntu.

`excelcsv.py FILE` reads a UTF-8 comma-separated CSV and flags two narrow patterns after trimming surrounding whitespace: ASCII digit strings with a leading zero and ASCII digit strings with 16 or more digits. Both can be counted on one value. It also rejects inconsistent field counts, blank/duplicate headers, invalid UTF-8 and parser errors. Quoted multiline records work.

This is not an Excel simulator, full CSV validator or formula-security scanner. No-hit output is not a safety pass. Dates, scientific notation, formulas and other conversions are not checked. Excel's import method, version and automatic-conversion settings affect what happens. Preserve an original and verify imported identifiers as text.

## Practice

Use a new empty lesson folder. Read `make_sample.py`, then run `python make_sample.py`. It creates `sample/orders.csv` with fictional data and refuses an existing sample path. It never deletes or replaces an existing sample folder. Do not remove existing data to force it to run.

Run `python excelcsv.py sample/orders.csv`. It reads the selected CSV only, but prints example values, so do not share private output. The tool loads the file in memory; use small files.

Run `python -m unittest -v`. All 20 tests use temporary folders. They check malformed records, UTF-8, quoted multiline data, risk boundaries and examples, no-hit limits, unchanged source bytes/metadata/directory and setup collision refusal. They do not certify every possible file.

If your platform uses `python3` rather than `python`, substitute that command throughout.

## Recording

The repaired sources ran twice on GitHub-hosted Windows and twice on Ubuntu on 16 October 2026. All four runs passed 20 tests. Transcripts are included. Per-platform runs differ only in test duration; Windows and Ubuntu also use different Python versions and unittest name rendering. Lesson displays use the first Windows recording, not a mixed transcript. This is not a recording of Excel.

Excel source: https://support.microsoft.com/en-us/excel/keeping-leading-zeros-and-large-numbers

MIT license for teaching code. No warranty. No private data, credentials or analytics included.
