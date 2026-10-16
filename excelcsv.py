"""Read-only UTF-8 CSV check for two numeric-text conversion risks.

This is not an Excel simulator, validator or formula-safety check.
Only ASCII digit strings with leading zeros or 16+ digits are flagged.
"""
import csv
import sys


def ascii_digits(text):
    return bool(text) and all('0' <= char <= '9' for char in text)


def is_leading_zero(text):
    return len(text) > 1 and ascii_digits(text) and text.startswith('0')


def is_long_number(text):
    return len(text) >= 16 and ascii_digits(text)


def scan_rows(rows):
    """Rows must be mappings of unique column names to string values."""
    hits = {}
    for row in rows:
        for name, value in row.items():
            text = value.strip()
            for rule, flagged in [('zero', is_leading_zero(text)),
                                  ('long', is_long_number(text))]:
                if flagged:
                    col = hits.setdefault(name, {'zero': 0, 'long': 0,
                                                 'zero_example': '', 'long_example': ''})
                    col[rule] += 1
                    if not col[rule + '_example']:
                        col[rule + '_example'] = text
    return hits


def main(argv):
    if len(argv) != 2 or argv[1] in ('-h', '--help'):
        print('Usage: python excelcsv.py FILE', file=sys.stderr)
        return 2
    path = argv[1]
    try:
        with open(path, 'r', newline='', encoding='utf-8-sig') as handle:
            reader = csv.reader(handle, strict=True)
            header = next(reader, None)
            if not header or any(not name.strip() for name in header):
                raise ValueError('missing or blank column name')
            if len(set(header)) != len(header):
                raise ValueError('duplicate column name')
            rows = []
            for number, fields in enumerate(reader, 1):
                if len(fields) != len(header):
                    raise ValueError('data record %d has %d fields; expected %d'
                                     % (number, len(fields), len(header)))
                rows.append(dict(zip(header, fields)))
    except OSError as error:
        print('Cannot read file: %s (%s)' % (path, error.strerror), file=sys.stderr)
        return 2
    except (csv.Error, UnicodeError, ValueError) as error:
        print('Could not check CSV: %s' % error, file=sys.stderr)
        return 1
    hits = scan_rows(rows)
    print('Two numeric-text risks to check before Excel import')
    print('File: ' + path)
    print('Data records checked: %d' % len(rows))
    print()
    if not hits:
        print('No ASCII digit strings with leading zeros or 16+ digits found.')
    for name, col in hits.items():
        print('Column: ' + name)
        if col['zero']:
            print('  %d leading-zero value(s), like %s'
                  % (col['zero'], col['zero_example']))
        if col['long']:
            print('  %d value(s) have 16+ digits, like %s'
                  % (col['long'], col['long_example']))
    print()
    print('These are risk flags, not predictions for your Excel settings.')
    print('Not checked: dates, scientific notation, formulas, encoding beyond UTF-8,')
    print('or every other automatic conversion. No-hit output is not a safety pass.')
    print('Only the CSV was read. Import identifiers as text if you must keep digits.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
