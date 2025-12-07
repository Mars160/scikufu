"""Tests for scikufu.file.json module."""

import json
import pytest

from scikufu.file.json import read, write, append


class TestJsonRead:
    """Test cases for the read function in json module."""

    def test_read_simple_json_file(self, tmp_path):
        """Test reading a simple JSON file."""
        # Create a simple JSON file
        test_data = {"name": "test", "value": 42, "active": True}
        json_file = tmp_path / "test.json"

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        # Test reading the JSON file
        result = read(json_file)
        assert result == test_data

    def test_read_nested_json_file(self, tmp_path):
        """Test reading a nested JSON file."""
        test_data = {
            "user": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "preferences": {"theme": "dark", "notifications": True},
            },
            "items": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}],
            "metadata": {"created": "2023-01-01T00:00:00Z", "version": 1.0},
        }

        json_file = tmp_path / "nested.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        result = read(json_file)
        assert result == test_data

    def test_read_json_file_with_arrays(self, tmp_path):
        """Test reading a JSON file containing arrays."""
        test_data = {
            "numbers": [1, 2, 3, 4, 5],
            "strings": ["apple", "banana", "cherry"],
            "mixed": [1, "two", 3.0, True, None],
            "nested_arrays": [[1, 2], [3, 4], [5, 6]],
        }

        json_file = tmp_path / "arrays.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        result = read(json_file)
        assert result == test_data

    def test_read_json_file_with_special_values(self, tmp_path):
        """Test reading a JSON file with special values."""
        test_data = {
            "null_value": None,
            "boolean_true": True,
            "boolean_false": False,
            "integer": 42,
            "float": 3.14159,
            "empty_string": "",
            "empty_object": {},
            "empty_array": [],
        }

        json_file = tmp_path / "special.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        result = read(json_file)
        assert result == test_data

    def test_read_json_with_utf8_encoding(self, tmp_path):
        """Test reading a JSON file with UTF-8 encoding."""
        test_data = {
            "chinese": "你好世界",
            "emoji": "🌍🚀",
            "special_chars": "áéíóú",
            "german": "Müller",
        }

        json_file = tmp_path / "utf8.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False)

        result = read(json_file, encoding="utf-8")
        assert result == test_data

    def test_read_json_with_different_encoding(self, tmp_path):
        """Test reading a JSON file with different encoding."""
        test_data = {"message": "Hello World"}

        json_file = tmp_path / "latin1.json"
        with open(json_file, "w", encoding="latin-1") as f:
            json.dump(test_data, f)

        result = read(json_file, encoding="latin-1")
        assert result == test_data

    def test_read_json_file_path_as_string(self, tmp_path):
        """Test reading JSON file with path provided as string."""
        test_data = {"test": "data"}
        json_file = tmp_path / "string_path.json"

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        # Use string path instead of Path object
        result = read(str(json_file))
        assert result == test_data

    def test_read_json_file_path_as_pathlike(self, tmp_path):
        """Test reading JSON file with path provided as PathLike object."""
        test_data = {"test": "data"}
        json_file = tmp_path / "pathlike.json"

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        # Use Path object
        result = read(json_file)
        assert result == test_data

    def test_read_empty_json_file(self, tmp_path):
        """Test reading an empty JSON file."""
        json_file = tmp_path / "empty.json"

        # Create an empty JSON object file
        with open(json_file, "w", encoding="utf-8") as f:
            f.write("{}")

        result = read(json_file)
        assert result == {}

    def test_read_json_file_not_found(self):
        """Test reading a JSON file that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            read("/path/that/does/not/exist.json")

    def test_read_invalid_json_file(self, tmp_path):
        """Test reading an invalid JSON file."""
        json_file = tmp_path / "invalid.json"

        # Write invalid JSON content
        with open(json_file, "w", encoding="utf-8") as f:
            f.write('{"invalid": json content}')

        with pytest.raises(json.JSONDecodeError):
            read(json_file)

    def test_read_json_with_whitespace(self, tmp_path):
        """Test reading JSON file with various whitespace formatting."""
        test_data = {"key": "value", "array": [1, 2, 3]}

        json_file = tmp_path / "whitespace.json"
        with open(json_file, "w", encoding="utf-8") as f:
            # Write JSON with custom formatting
            f.write(
                '{\n    "key": "value",\n    "array": [\n        1,\n        2,\n        3\n    ]\n}'
            )

        result = read(json_file)
        assert result == test_data

    def test_read_json_with_comments_removed(self, tmp_path):
        """Test reading a JSON file (comments are not valid in standard JSON)."""
        test_data = {"name": "test", "value": 42}

        json_file = tmp_path / "no_comments.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        result = read(json_file)
        assert result == test_data

    def test_read_large_json_file(self, tmp_path):
        """Test reading a large JSON file."""
        # Create a large JSON object
        test_data = {
            "large_array": list(range(1000)),
            "nested_data": {f"key_{i}": f"value_{i}" for i in range(100)},
        }

        json_file = tmp_path / "large.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        result = read(json_file)
        assert result == test_data
        assert len(result["large_array"]) == 1000
        assert len(result["nested_data"]) == 100

    def test_read_json_file_with_unicode_escape_sequences(self, tmp_path):
        """Test reading JSON file with Unicode escape sequences."""
        json_file = tmp_path / "unicode_escape.json"

        # Write JSON with Unicode escape sequences manually
        with open(json_file, "w", encoding="utf-8") as f:
            f.write('{"unicode": "\\u4f60\\u597d", "emoji": "\\ud83c\\udf0d"}')

        result = read(json_file)
        assert result["unicode"] == "你好"
        assert result["emoji"] == "🌍"


class TestJsonWrite:
    """Test cases for the write function in json module."""

    def test_write_simple_json(self, tmp_path):
        """Test writing a simple JSON object."""
        test_data = {"name": "test", "value": 42, "active": True}
        json_file = tmp_path / "write_simple.json"

        write(json_file, test_data)

        result = read(json_file)
        assert result == test_data

    def test_write_empty_object(self, tmp_path):
        """Test writing an empty JSON object."""
        test_data = {}
        json_file = tmp_path / "write_empty.json"

        write(json_file, test_data)

        result = read(json_file)
        assert result == {}

    def test_write_nested_json(self, tmp_path):
        """Test writing a nested JSON object."""
        test_data = {
            "user": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "preferences": {"theme": "dark", "notifications": True},
            },
            "items": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}],
            "metadata": {"created": "2023-01-01T00:00:00Z", "version": 1.0},
        }

        json_file = tmp_path / "write_nested.json"
        write(json_file, test_data)

        result = read(json_file)
        assert result == test_data

    def test_write_with_arrays(self, tmp_path):
        """Test writing JSON object with arrays."""
        test_data = {
            "numbers": [1, 2, 3, 4, 5],
            "strings": ["apple", "banana", "cherry"],
            "mixed": [1, "two", 3.0, True, None],
            "nested_arrays": [[1, 2], [3, 4], [5, 6]],
        }

        json_file = tmp_path / "write_arrays.json"
        write(json_file, test_data)

        result = read(json_file)
        assert result == test_data

    def test_write_with_special_values(self, tmp_path):
        """Test writing JSON object with special values."""
        test_data = {
            "null_value": None,
            "boolean_true": True,
            "boolean_false": False,
            "integer": 42,
            "float": 3.14159,
            "empty_string": "",
            "empty_object": {},
            "empty_array": [],
        }

        json_file = tmp_path / "write_special.json"
        write(json_file, test_data)

        result = read(json_file)
        assert result == test_data

    def test_write_with_unicode_content(self, tmp_path):
        """Test writing JSON object with Unicode content."""
        test_data = {
            "chinese": "你好世界",
            "emoji": "🌍🚀",
            "special_chars": "áéíóú",
            "german": "Müller",
        }

        json_file = tmp_path / "write_unicode.json"
        write(json_file, test_data)

        result = read(json_file)
        assert result == test_data

    def test_write_with_different_encoding(self, tmp_path):
        """Test writing JSON object with different encoding."""
        test_data = {"message": "Hello World"}

        json_file = tmp_path / "write_encoding.json"
        write(json_file, test_data, encoding="latin-1")

        result = read(json_file, encoding="latin-1")
        assert result == test_data

    def test_write_with_custom_indent(self, tmp_path):
        """Test writing JSON object with custom indentation."""
        test_data = {"key": "value", "array": [1, 2, 3]}
        json_file = tmp_path / "write_indent.json"

        write(json_file, test_data, indent=2)

        # Read the raw file content to check indentation
        with open(json_file, "r", encoding="utf-8") as f:
            content = f.read()

        result = read(json_file)
        assert result == test_data
        # Check that indentation is applied (content contains spaces)
        assert "  " in content  # Should contain 2-space indentation

    def test_write_overwrites_existing_file(self, tmp_path):
        """Test that write overwrites existing file."""
        original_data = {"id": 1, "name": "Original"}
        new_data = {"id": 2, "name": "New"}
        json_file = tmp_path / "write_overwrite.json"

        # Write original data
        write(json_file, original_data)
        result = read(json_file)
        assert result == original_data

        # Write new data (should overwrite)
        write(json_file, new_data)
        result = read(json_file)
        assert result == new_data

    def test_write_large_json(self, tmp_path):
        """Test writing a large JSON object."""
        test_data = {
            "large_array": list(range(1000)),
            "nested_data": {f"key_{i}": f"value_{i}" for i in range(100)},
        }

        json_file = tmp_path / "write_large.json"
        write(json_file, test_data)

        result = read(json_file)
        assert result == test_data
        assert len(result["large_array"]) == 1000
        assert len(result["nested_data"]) == 100

    def test_write_path_as_string(self, tmp_path):
        """Test writing JSON object with path as string."""
        test_data = {"test": "data"}
        json_file = tmp_path / "write_string.json"

        write(str(json_file), test_data)

        result = read(json_file)
        assert result == test_data

    def test_write_unicode_escape_sequences_handled(self, tmp_path):
        """Test that Unicode characters are properly handled (not escaped)."""
        test_data = {"chinese": "你好", "emoji": "🌍"}
        json_file = tmp_path / "write_unicode_no_escape.json"

        write(json_file, test_data)

        # Read raw content to ensure Unicode is not escaped
        with open(json_file, "r", encoding="utf-8") as f:
            content = f.read()

        result = read(json_file)
        assert result == test_data
        # Unicode characters should be present in the file, not escape sequences
        assert "你好" in content
        assert "🌍" in content


class TestJsonAppend:
    """Test cases for the append function in json module."""

    def test_append_to_existing_file(self, tmp_path):
        """Test appending to an existing JSON file."""
        original_data = {"id": 1, "name": "Alice", "active": True}
        append_data = {"age": 30, "city": "New York"}
        json_file = tmp_path / "append_existing.json"

        # Write original data
        write(json_file, original_data)

        # Append new data
        append(json_file, append_data)

        # Verify merged data
        result = read(json_file)
        expected = {**original_data, **append_data}
        assert result == expected

    def test_append_to_empty_file(self, tmp_path):
        """Test appending to an empty JSON file."""
        append_data = {"id": 1, "name": "Alice"}
        json_file = tmp_path / "append_empty.json"

        # Create empty JSON file
        write(json_file, {})

        # Append data
        append(json_file, append_data)

        result = read(json_file)
        assert result == append_data

    def test_append_to_nonexistent_file(self, tmp_path):
        """Test appending to a non-existent JSON file."""
        append_data = {"id": 1, "name": "Alice"}
        json_file = tmp_path / "append_nonexistent.json"

        # Append to non-existent file (should create it)
        with pytest.raises(FileNotFoundError):
            append(json_file, append_data)

    def test_append_overwrites_existing_keys(self, tmp_path):
        """Test that append overwrites existing keys."""
        original_data = {"id": 1, "name": "Alice", "active": True}
        append_data = {"name": "Bob", "age": 30}  # name key exists in original
        json_file = tmp_path / "append_overwrite.json"

        write(json_file, original_data)
        append(json_file, append_data)

        result = read(json_file)
        expected = {"id": 1, "name": "Bob", "active": True, "age": 30}
        assert result == expected

    def test_append_empty_dict(self, tmp_path):
        """Test appending empty dictionary."""
        original_data = {"id": 1, "name": "Alice"}
        json_file = tmp_path / "append_empty_dict.json"

        write(json_file, original_data)
        append(json_file, {})

        result = read(json_file)
        assert result == original_data

    def test_append_with_nested_data(self, tmp_path):
        """Test appending nested data structures."""
        original_data = {"user": {"id": 1, "name": "Alice"}}
        append_data = {
            "preferences": {"theme": "dark", "notifications": True},
            "user": {"age": 30}  # This should replace the entire user object
        }
        json_file = tmp_path / "append_nested.json"

        write(json_file, original_data)
        append(json_file, append_data)

        result = read(json_file)
        expected = {
            "user": {"age": 30},
            "preferences": {"theme": "dark", "notifications": True}
        }
        assert result == expected

    def test_append_with_unicode_content(self, tmp_path):
        """Test appending Unicode content."""
        original_data = {"english": "Hello"}
        append_data = {"chinese": "你好", "emoji": "🌍"}
        json_file = tmp_path / "append_unicode.json"

        write(json_file, original_data)
        append(json_file, append_data)

        result = read(json_file)
        expected = {**original_data, **append_data}
        assert result == expected

    def test_append_with_different_encoding(self, tmp_path):
        """Test appending with different encoding."""
        original_data = {"message": "Hello"}
        append_data = {"french": "Café"}
        json_file = tmp_path / "append_encoding.json"

        write(json_file, original_data, encoding="latin-1")
        append(json_file, append_data, encoding="latin-1")

        result = read(json_file, encoding="latin-1")
        expected = {**original_data, **append_data}
        assert result == expected

    def test_append_multiple_times(self, tmp_path):
        """Test appending multiple times to the same file."""
        data1 = {"id": 1, "name": "Alice"}
        data2 = {"age": 30, "city": "New York"}
        data3 = {"active": True, "role": "admin"}
        json_file = tmp_path / "append_multiple.json"

        write(json_file, data1)
        append(json_file, data2)
        append(json_file, data3)

        result = read(json_file)
        expected = {**data1, **data2, **data3}
        assert result == expected

    def test_append_with_special_values(self, tmp_path):
        """Test appending special JSON values."""
        original_data = {"name": "test"}
        append_data = {
            "null_value": None,
            "boolean_true": True,
            "boolean_false": False,
            "number": 42.5,
            "empty_array": [],
            "empty_object": {}
        }
        json_file = tmp_path / "append_special.json"

        write(json_file, original_data)
        append(json_file, append_data)

        result = read(json_file)
        expected = {**original_data, **append_data}
        assert result == expected

    def test_append_with_arrays(self, tmp_path):
        """Test appending arrays to JSON file."""
        original_data = {"id": 1}
        append_data = {
            "numbers": [1, 2, 3],
            "strings": ["apple", "banana"],
            "mixed": [1, "two", 3.0, True, None]
        }
        json_file = tmp_path / "append_arrays.json"

        write(json_file, original_data)
        append(json_file, append_data)

        result = read(json_file)
        expected = {**original_data, **append_data}
        assert result == expected

    def test_append_path_as_string(self, tmp_path):
        """Test appending to JSON file with path as string."""
        original_data = {"id": 1}
        append_data = {"name": "Alice"}
        json_file = tmp_path / "append_string.json"

        write(json_file, original_data)
        append(str(json_file), append_data)

        result = read(json_file)
        expected = {**original_data, **append_data}
        assert result == expected

    def test_append_with_custom_indent(self, tmp_path):
        """Test appending with custom indentation."""
        original_data = {"id": 1, "name": "Alice"}
        append_data = {"age": 30, "city": "New York"}
        json_file = tmp_path / "append_indent.json"

        write(json_file, original_data, indent=2)
        append(json_file, append_data, indent=2)

        result = read(json_file)
        expected = {**original_data, **append_data}
        assert result == expected

        # Check that file is properly formatted with indentation
        with open(json_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "  " in content  # Should contain 2-space indentation

    def test_append_large_data(self, tmp_path):
        """Test appending large data structures."""
        original_data = {"original": list(range(500))}
        append_data = {"append": {f"key_{i}": f"value_{i}" for i in range(500)}}
        json_file = tmp_path / "append_large.json"

        write(json_file, original_data)
        append(json_file, append_data)

        result = read(json_file)
        expected = {**original_data, **append_data}
        assert result == expected
        assert len(result["original"]) == 500
        assert len(result["append"]) == 500
