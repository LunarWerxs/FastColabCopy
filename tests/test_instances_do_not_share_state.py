import io
import sys
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import fastcopy  # noqa: E402


class InstancesDoNotShareStateTest(unittest.TestCase):
    def test_two_instances_get_their_own_queue_and_lock(self):
        # Two runs in one process must not share the queue or lock they coordinate through.
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / 'src'
            src.mkdir()
            with redirect_stdout(io.StringIO()):
                first = fastcopy.FastCopy(str(src), str(Path(tmp) / 'dst1'))
                second = fastcopy.FastCopy(str(src), str(Path(tmp) / 'dst2'))

            self.assertIsNot(first.file_queue, second.file_queue)
            self.assertIsNot(first._lock, second._lock)


if __name__ == '__main__':
    unittest.main()
