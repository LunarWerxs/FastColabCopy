import io
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock
from contextlib import redirect_stdout

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import fastcopy  # noqa: E402


class CopyWorkerSurvivesUnlinkFailureTest(unittest.TestCase):
    def test_run_finishes_when_unlink_of_existing_destination_raises(self):
        # With --replace, an unlink that raises must not kill the worker thread: the run must still finish.
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / 'src'
            dst = Path(tmp) / 'dst'
            src.mkdir()
            dst.mkdir()
            (src / 'a.txt').write_text('new')
            (dst / 'a.txt').write_text('old')

            def run():
                with redirect_stdout(io.StringIO()):
                    fastcopy.FastCopy(str(src), str(dst), replace=True, thread_num=1)

            with mock.patch.object(Path, 'unlink', side_effect=PermissionError('locked')):
                runner = threading.Thread(target=run, daemon=True)
                runner.start()
                runner.join(timeout=5)
                finished = not runner.is_alive()

            self.assertTrue(finished, 'FastCopy hung: queue.join() never returned after an unlink failure')


if __name__ == '__main__':
    unittest.main()
