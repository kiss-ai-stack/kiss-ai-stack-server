import atexit
import os
import shutil
import tempfile
from functools import lru_cache


@lru_cache(maxsize=1)
def temp_file_manager():
    """
    Cached singleton factory function for Stacks server.
    """
    return TemporaryFileManager()



class TemporaryFileManager:
    """
    Manages temporary files and directories with guaranteed cleanup
    """

    def __init__(self):
        self._temp_dirs = set()
        atexit.register(self.cleanup_all)

    def create_temp_dir(self) -> str:
        """
        Create a temporary directory and track it for cleanup

        :return: Path to the temporary directory
        """
        temp_dir = tempfile.mkdtemp()
        self._temp_dirs.add(temp_dir)
        return temp_dir

    def cleanup_dir(self, dir_path: str):
        """
        Remove a specific temporary directory

        :param dir_path: Path to the temporary directory
        """
        try:
            if dir_path in self._temp_dirs and os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                self._temp_dirs.discard(dir_path)
        except Exception as e:
            print(f"Error cleaning up temp directory {dir_path}: {e}")

    def cleanup_all(self):
        """
        Remove all tracked temporary directories
        """
        for temp_dir in list(self._temp_dirs):
            self.cleanup_dir(temp_dir)

    def safe_file_path(self, temp_dir: str, filename: str) -> str:
        """
        Generate a safe file path within the temporary directory

        :param temp_dir: Base temporary directory
        :param filename: Original filename
        :return: Safe file path
        """
        safe_filename = os.path.basename(filename)
        return os.path.join(temp_dir, safe_filename)
