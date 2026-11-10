import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from contextlib import redirect_stdout

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import fastcopy  # noqa: E402

real_copy2 = shutil.copy2


def copy2_failing_for_bad_file(src, dst, *args, **kwargs):
    if Path(src).name == 'bad.txt':
        raise OSError('simulated copy failure')
    return real_copy2(src, dst, *args, **kwargs)


class SummaryCountsRealCopiesTest(unittest.TestCase):
    def test_summary_reports_only_files_actually_copied(self):
        # The summary must count successful copies, not the number of files queued.
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / 'src'
            dst = Path(tmp) / 'dst'
            src.mkdir()
            (src / 'good.txt').write_text('ok')
            (src / 'bad.txt').write_text('fails')

            out = io.StringIO()
            with mock.patch.object(fastcopy.shutil, 'copy2', side_effect=copy2_failing_for_bad_file), \
                    redirect_stdout(out):
                fastcopy.FastCopy(str(src), str(dst), thread_num=1)

            self.assertIn('1/2 files copied successfully.', out.getvalue())


if __name__ == '__main__':
    unittest.main()
