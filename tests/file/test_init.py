"""Tests for scikufu.file module (.__init__ file)."""

import os
import tempfile
import pytest

from scikufu.file import exists


class TestFileExists:
    """Test cases for the exists function in file module."""

    def test_exists_with_existing_file(self, tmp_path):
        """Test exists function with an existing file."""
        # Create a test file
        test_file = tmp_path / "test_file.txt"
        with open(test_file, "w") as f:
            f.write("test content")

        # Test that the file exists
        result = exists(test_file)
        assert result is True

    def test_exists_with_existing_file_as_string(self, tmp_path):
        """Test exists function with file path provided as string."""
        # Create a test file
        test_file = tmp_path / "test_file_string.txt"
        with open(test_file, "w") as f:
            f.write("test content")

        # Test that the file exists using string path
        result = exists(str(test_file))
        assert result is True

    def test_exists_with_existing_directory(self, tmp_path):
        """Test exists function with an existing directory."""
        # Create a test directory
        test_dir = tmp_path / "test_directory"
        test_dir.mkdir()

        # Test that the directory exists
        result = exists(test_dir)
        assert result is True

    def test_exists_with_nonexistent_file(self):
        """Test exists function with a non-existent file."""
        nonexistent_file = "/path/that/does/not/exist.txt"
        result = exists(nonexistent_file)
        assert result is False

    def test_exists_with_nonexistent_file_as_string(self):
        """Test exists function with non-existent file path as string."""
        nonexistent_file = "/tmp/this_file_does_not_exist_12345.txt"
        result = exists(nonexistent_file)
        assert result is False

    def test_exists_with_empty_string(self):
        """Test exists function with empty string path."""
        result = exists("")
        assert result is False

    def test_exists_with_relative_path_existing_file(self, tmp_path):
        """Test exists function with relative path to existing file."""
        # Create a test file
        test_file = tmp_path / "relative_test.txt"
        with open(test_file, "w") as f:
            f.write("test content")

        # Change to the temp directory and use relative path
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = exists("relative_test.txt")
            assert result is True
        finally:
            os.chdir(original_cwd)

    def test_exists_with_relative_path_nonexistent_file(self, tmp_path):
        """Test exists function with relative path to non-existent file."""
        # Change to the temp directory and use relative path
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = exists("nonexistent_relative.txt")
            assert result is False
        finally:
            os.chdir(original_cwd)

    def test_exists_with_special_characters_in_path(self, tmp_path):
        """Test exists function with special characters in file path."""
        # Create a file with special characters in name
        special_file = tmp_path / "test_file_特殊字符_@#$%^&().txt"
        with open(special_file, "w", encoding="utf-8") as f:
            f.write("special content")

        result = exists(special_file)
        assert result is True

    def test_exists_with_hidden_file(self, tmp_path):
        """Test exists function with hidden file."""
        # Create a hidden file
        hidden_file = tmp_path / ".hidden_file"
        with open(hidden_file, "w") as f:
            f.write("hidden content")

        result = exists(hidden_file)
        assert result is True

    def test_exists_with_unicode_filename(self, tmp_path):
        """Test exists function with Unicode filename."""
        # Create a file with Unicode name
        unicode_file = tmp_path / "测试文件.txt"
        with open(unicode_file, "w", encoding="utf-8") as f:
            f.write("unicode content")

        result = exists(unicode_file)
        assert result is True

    def test_exists_with_dot_in_current_directory(self, tmp_path):
        """Test exists function with current directory path '.'."""
        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = exists(".")
            assert result is True  # Current directory always exists
        finally:
            os.chdir(original_cwd)

    def test_exists_with_double_dot_parent_directory(self, tmp_path):
        """Test exists function with parent directory path '..'."""
        # Change to a subdirectory and test parent directory
        original_cwd = os.getcwd()
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        try:
            os.chdir(subdir)
            result = exists("..")
            assert result is True  # Parent directory exists
        finally:
            os.chdir(original_cwd)

    def test_exists_with_absolute_and_relative_paths(self, tmp_path):
        """Test exists function with absolute and relative paths for same file."""
        # Create a test file
        test_file = tmp_path / "path_test.txt"
        with open(test_file, "w") as f:
            f.write("test content")

        # Test with absolute path
        abs_result = exists(test_file)
        assert abs_result is True

        # Change to temp directory and test with relative path
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            rel_result = exists("path_test.txt")
            assert rel_result is True
        finally:
            os.chdir(original_cwd)

    def test_exists_with_tempfile(self):
        """Test exists function with a temporary file."""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name

        # File exists even after closing (delete=False)
        try:
            result = exists(temp_path)
            assert result is True
        finally:
            # Clean up
            os.unlink(temp_path)

    def test_exists_after_file_deletion(self, tmp_path):
        """Test exists function after file deletion."""
        # Create a test file
        test_file = tmp_path / "delete_me.txt"
        with open(test_file, "w") as f:
            f.write("content")

        # File should exist
        assert exists(test_file) is True

        # Delete the file
        test_file.unlink()

        # File should no longer exist
        assert exists(test_file) is False

    def test_exists_with_symlink(self, tmp_path):
        """Test exists function with symbolic link (if supported)."""
        # Create a target file
        target_file = tmp_path / "target.txt"
        with open(target_file, "w") as f:
            f.write("target content")

        # Create a symbolic link
        try:
            link_file = tmp_path / "link.txt"
            link_file.symlink_to(target_file)

            # Test that symlink exists
            result = exists(link_file)
            assert result is True
        except OSError:
            # Symlinks not supported on this platform, skip test
            pytest.skip("Symbolic links not supported on this platform")