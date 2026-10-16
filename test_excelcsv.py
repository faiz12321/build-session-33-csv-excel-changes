"""Small fixture tests. All test-created files stay in a temporary folder."""
import contextlib
import hashlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import excelcsv

HERE = Path(__file__).resolve().parent


class Checks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_csv(self, data):
        path = self.folder / 'data.csv'
        path.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = excelcsv.main(['excelcsv.py', str(path)])
        return rc, out.getvalue(), err.getvalue()

    def test_leading_zero(self):
        self.assertTrue(excelcsv.is_leading_zero('007'))
        for text in ['0', '7', '01.2', '٠١', '']:
            self.assertFalse(excelcsv.is_leading_zero(text))

    def test_long_boundary(self):
        self.assertFalse(excelcsv.is_long_number('1' * 15))
        self.assertTrue(excelcsv.is_long_number('1' * 16))

    def test_both_risks_counted(self):
        col = excelcsv.scan_rows([{'Code': '0' * 16}])['Code']
        self.assertEqual((col['zero'], col['long']), (1, 1))

    def test_separate_examples(self):
        col = excelcsv.scan_rows([{'A': '007'}, {'A': '1' * 16}])['A']
        self.assertEqual(col['zero_example'], '007')
        self.assertEqual(col['long_example'], '1' * 16)

    def test_surrounding_spaces(self):
        rc, out, _ = self.run_csv('Code\n 007 \n')
        self.assertEqual(rc, 0)
        self.assertIn('1 leading-zero value(s)', out)

    def test_no_hits_are_not_safety_pass(self):
        rc, out, _ = self.run_csv('Value\n1E10\n03/04\n=1+1\n')
        self.assertEqual(rc, 0)
        self.assertIn('No ASCII digit strings', out)
        self.assertIn('No-hit output is not a safety pass.', out)
        self.assertNotIn('without changing values', out)

    def test_extra_fields_rejected(self):
        rc, _, err = self.run_csv('A,B\n001,x,extra\n')
        self.assertEqual(rc, 1)
        self.assertIn('has 3 fields; expected 2', err)

    def test_missing_fields_rejected(self):
        self.assertEqual(self.run_csv('A,B\n001\n')[0], 1)

    def test_duplicate_header_rejected(self):
        self.assertEqual(self.run_csv('A,A\n001,002\n')[0], 1)

    def test_blank_header_rejected(self):
        self.assertEqual(self.run_csv('A, \n001,x\n')[0], 1)

    def test_invalid_utf8_rejected(self):
        self.assertEqual(self.run_csv(b'A\n\xff\n')[0], 1)

    def test_bom_accepted(self):
        self.assertEqual(self.run_csv(b'\xef\xbb\xbfA\n001\n')[0], 0)

    def test_quoted_multiline(self):
        rc, out, _ = self.run_csv('A,B\n001,"two\nlines"\n')
        self.assertEqual(rc, 0)
        self.assertIn('Data records checked: 1', out)

    def test_unclosed_quote_rejected(self):
        self.assertEqual(self.run_csv('A\n"unclosed\n')[0], 1)

    def test_header_only(self):
        rc, out, _ = self.run_csv('A\n')
        self.assertEqual(rc, 0)
        self.assertIn('Data records checked: 0', out)

    def test_empty_file_rejected(self):
        self.assertEqual(self.run_csv('')[0], 1)

    def test_source_bytes_metadata_and_directory_unchanged(self):
        path = self.folder / 'data.csv'
        path.write_bytes(b'A\n007\n')
        before = (path.read_bytes(), path.stat().st_size, path.stat().st_mtime_ns,
                  sorted(p.name for p in self.folder.iterdir()))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(excelcsv.main(['excelcsv.py', str(path)]), 0)
        after = (path.read_bytes(), path.stat().st_size, path.stat().st_mtime_ns,
                 sorted(p.name for p in self.folder.iterdir()))
        self.assertEqual(before, after)

    def test_setup_refuses_existing_sample(self):
        shutil.copyfile(HERE / 'make_sample.py', self.folder / 'make_sample.py')
        cmd = [sys.executable, str(self.folder / 'make_sample.py')]
        first = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(first.returncode, 0)
        sentinel = self.folder / 'sample' / 'keep.txt'
        sentinel.write_text('keep me', encoding='utf-8')
        source = self.folder / 'sample' / 'orders.csv'
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        second = subprocess.run(cmd, capture_output=True, text=True)
        self.assertNotEqual(second.returncode, 0)
        self.assertEqual(sentinel.read_text(encoding='utf-8'), 'keep me')
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)

    def test_missing_file(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(excelcsv.main(['excelcsv.py', str(self.folder/'absent')]), 2)

    def test_usage(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(excelcsv.main(['excelcsv.py']), 2)


if __name__ == '__main__':
    unittest.main()
