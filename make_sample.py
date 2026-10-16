"""Create a tiny fictional CSV beside this script. Never reuse a sample folder."""
from pathlib import Path
import stat

CSV = '''Order ID,Item,Phone,Reference,Total
00104,Tea,0555000001,1234567890123456,129.50
00215,Pen,0555000002,1234567890123457,64.00
00331,Book,0555000003,1234567890123458,250.75
00440,Cup,0555000004,1234567890123459,19.99
'''


def main():
    folder = Path(__file__).absolute().parent / 'sample'
    if '..' in folder.parts:
        raise OSError('Parent-traversal paths are unsupported.')
    for parent in reversed(folder.parents):
        info = parent.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise OSError('Linked/reparse-point parents are unsupported.')
    try:
        folder.mkdir()  # Refuses any existing file or folder, including links.
    except FileExistsError:
        raise SystemExit('Stopped: sample already exists. Nothing was replaced or deleted.')
    with (folder / 'orders.csv').open('x', encoding='utf-8', newline='') as handle:
        handle.write(CSV)
    print('Created sample/orders.csv with 4 fictional data records.')
    print('Existing files are never replaced. Run this setup only once in a new lesson folder.')


if __name__ == '__main__':
    main()
