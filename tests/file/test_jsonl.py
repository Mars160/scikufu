"""Tests for scikufu.file.jsonl module."""

import json
import pytest

from scikufu.file.jsonl import read, write, append


class TestJsonlRead:
    """Test cases for the read function in jsonl module."""

    def test_read_simple_jsonl_file(self, tmp_path):
        """Test reading a simple JSON Lines file."""
        test_data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"}
        ]
        jsonl_file = tmp_path / "simple.jsonl"

        # Write JSON Lines manually
        with open(jsonl_file, "w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        result = list(read(jsonl_file))
        assert result == test_data

    def test_read_empty_jsonl_file(self, tmp_path):
        """Test reading an empty JSON Lines file."""
        jsonl_file = tmp_path / "empty.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            f.write("")

        result = list(read(jsonl_file))
        assert result == []

    def test_read_jsonl_file_with_blank_lines(self, tmp_path):
        """Test reading JSON Lines file with blank lines."""
        test_data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
        jsonl_file = tmp_path / "with_blanks.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(test_data[0], ensure_ascii=False) + "\n")
            f.write("\n")  # Blank line
            f.write(json.dumps(test_data[1], ensure_ascii=False) + "\n")
            f.write("\n")  # Another blank line

        result = list(read(jsonl_file))
        assert result == test_data  # Blank lines should be ignored

    def test_read_jsonl_file_with_whitespace_lines(self, tmp_path):
        """Test reading JSON Lines file with whitespace-only lines."""
        test_data = [{"id": 1, "value": "test"}]
        jsonl_file = tmp_path / "whitespace.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(test_data[0], ensure_ascii=False) + "\n")
            f.write("   \n")  # Whitespace line
            f.write("\t\n")   # Tab line

        result = list(read(jsonl_file))
        assert result == test_data

    def test_read_jsonl_file_with_unicode_content(self, tmp_path):
        """Test reading JSON Lines file with Unicode content."""
        test_data = [
            {"chinese": "你好世界", "emoji": "🌍🚀"},
            {"german": "Müller", "special": "áéíóú"}
        ]
        jsonl_file = tmp_path / "unicode.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        result = list(read(jsonl_file))
        assert result == test_data

    def test_read_jsonl_file_with_different_encoding(self, tmp_path):
        """Test reading JSON Lines file with different encoding."""
        test_data = [{"message": "Café résumé"}]
        jsonl_file = tmp_path / "latin1.jsonl"

        with open(jsonl_file, "w", encoding="latin-1") as f:
            f.write(json.dumps(test_data[0]) + "\n")

        result = list(read(jsonl_file, encoding="latin-1"))
        assert result == test_data

    def test_read_jsonl_file_path_as_string(self, tmp_path):
        """Test reading JSON Lines file with path provided as string."""
        test_data = [{"test": "data"}]
        jsonl_file = tmp_path / "string_path.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(test_data[0], ensure_ascii=False) + "\n")

        result = list(read(str(jsonl_file)))
        assert result == test_data

    def test_read_jsonl_file_with_complex_nested_data(self, tmp_path):
        """Test reading JSON Lines file with complex nested data."""
        test_data = [
            {
                "user": {
                    "id": 1,
                    "name": "John",
                    "tags": ["admin", "user"]
                },
                "items": [
                    {"type": "book", "title": "Python 101"},
                    {"type": "course", "title": "Data Science"}
                ]
            }
        ]
        jsonl_file = tmp_path / "complex.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        result = list(read(jsonl_file))
        assert result == test_data

    def test_read_jsonl_file_with_special_values(self, tmp_path):
        """Test reading JSON Lines file with special JSON values."""
        test_data = [
            {"null_value": None, "boolean": True},
            {"number": 42.5, "empty": {}},
            {"array": [1, None, True, "test"]}
        ]
        jsonl_file = tmp_path / "special_values.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        result = list(read(jsonl_file))
        assert result == test_data

    def test_read_jsonl_file_with_trailing_newline(self, tmp_path):
        """Test reading JSON Lines file with trailing newline."""
        test_data = [{"id": 1}, {"id": 2}]
        jsonl_file = tmp_path / "trailing.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item) + "\n")
            f.write("\n")  # Extra trailing newline

        result = list(read(jsonl_file))
        assert result == test_data

    def test_read_jsonl_file_without_trailing_newline(self, tmp_path):
        """Test reading JSON Lines file without trailing newline."""
        test_data = [{"id": 1}, {"id": 2}]
        jsonl_file = tmp_path / "no_trailing.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(test_data[0], ensure_ascii=False) + "\n")
            f.write(json.dumps(test_data[1], ensure_ascii=False))  # No trailing newline

        result = list(read(jsonl_file))
        assert result == test_data

    def test_read_single_line_jsonl_file(self, tmp_path):
        """Test reading JSON Lines file with single line."""
        test_data = [{"single": "record"}]
        jsonl_file = tmp_path / "single.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(test_data[0], ensure_ascii=False) + "\n")

        result = list(read(jsonl_file))
        assert result == test_data

    def test_read_jsonl_file_not_found(self):
        """Test reading a JSON Lines file that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            list(read("/path/that/does/not/exist.jsonl"))

    def test_read_invalid_jsonl_file(self, tmp_path):
        """Test reading an invalid JSON Lines file."""
        jsonl_file = tmp_path / "invalid.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            f.write('{"valid": "json"}\n')
            f.write('{"invalid": json line}\n')  # Invalid JSON

        with pytest.raises(json.JSONDecodeError):
            list(read(jsonl_file))

    def test_read_large_jsonl_file(self, tmp_path):
        """Test reading a large JSON Lines file."""
        test_data = [{"id": i, "data": f"item_{i}"} for i in range(1000)]
        jsonl_file = tmp_path / "large.jsonl"

        with open(jsonl_file, "w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        result = list(read(jsonl_file))
        assert result == test_data
        assert len(result) == 1000


class TestJsonlWrite:
    """Test cases for the write function in jsonl module."""

    def test_write_simple_jsonl_file(self, tmp_path):
        """Test writing a simple JSON Lines file."""
        test_data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"}
        ]
        jsonl_file = tmp_path / "write_simple.jsonl"

        write(jsonl_file, test_data)

        # Verify file was written correctly
        result = list(read(jsonl_file))
        assert result == test_data

    def test_write_empty_list(self, tmp_path):
        """Test writing an empty list to JSON Lines file."""
        test_data = []
        jsonl_file = tmp_path / "write_empty.jsonl"

        write(jsonl_file, test_data)

        result = list(read(jsonl_file))
        assert result == []

    def test_write_single_item(self, tmp_path):
        """Test writing a single item to JSON Lines file."""
        test_data = [{"single": "item"}]
        jsonl_file = tmp_path / "write_single.jsonl"

        write(jsonl_file, test_data)

        result = list(read(jsonl_file))
        assert result == test_data

    def test_write_complex_data(self, tmp_path):
        """Test writing complex nested data to JSON Lines file."""
        test_data = [
            {
                "user": {"id": 1, "profile": {"name": "John", "age": 30}},
                "orders": [{"id": "A1", "amount": 99.99}, {"id": "A2", "amount": 49.99}]
            }
        ]
        jsonl_file = tmp_path / "write_complex.jsonl"

        write(jsonl_file, test_data)

        result = list(read(jsonl_file))
        assert result == test_data

    def test_write_with_unicode_content(self, tmp_path):
        """Test writing Unicode content to JSON Lines file."""
        test_data = [
            {"chinese": "你好世界", "emoji": "🌍🚀"},
            {"german": "Müller", "special": "áéíóú"}
        ]
        jsonl_file = tmp_path / "write_unicode.jsonl"

        write(jsonl_file, test_data)

        result = list(read(jsonl_file))
        assert result == test_data

    def test_write_with_different_encoding(self, tmp_path):
        """Test writing JSON Lines file with different encoding."""
        test_data = [{"message": "Café résumé"}]
        jsonl_file = tmp_path / "write_encoding.jsonl"

        write(jsonl_file, test_data, encoding="latin-1")

        result = list(read(jsonl_file, encoding="latin-1"))
        assert result == test_data

    def test_write_overwrites_existing_file(self, tmp_path):
        """Test that write overwrites existing file."""
        original_data = [{"id": 1, "name": "Original"}]
        new_data = [{"id": 2, "name": "New"}]
        jsonl_file = tmp_path / "overwrite.jsonl"

        # Write original data
        write(jsonl_file, original_data)
        result = list(read(jsonl_file))
        assert result == original_data

        # Write new data (should overwrite)
        write(jsonl_file, new_data)
        result = list(read(jsonl_file))
        assert result == new_data

    def test_write_with_special_values(self, tmp_path):
        """Test writing special JSON values."""
        test_data = [
            {"null_value": None, "boolean_true": True, "boolean_false": False},
            {"integer": 42, "float": 3.14159, "empty_array": [], "empty_object": {}}
        ]
        jsonl_file = tmp_path / "write_special.jsonl"

        write(jsonl_file, test_data)

        result = list(read(jsonl_file))
        assert result == test_data

    def test_write_large_dataset(self, tmp_path):
        """Test writing a large dataset to JSON Lines file."""
        test_data = [{"id": i, "data": f"item_{i}"} for i in range(1000)]
        jsonl_file = tmp_path / "write_large.jsonl"

        write(jsonl_file, test_data)

        result = list(read(jsonl_file))
        assert result == test_data
        assert len(result) == 1000

    def test_write_path_as_string(self, tmp_path):
        """Test writing JSON Lines file with path as string."""
        test_data = [{"test": "data"}]
        jsonl_file = tmp_path / "write_string.jsonl"

        write(str(jsonl_file), test_data)

        result = list(read(jsonl_file))
        assert result == test_data


class TestJsonlAppend:
    """Test cases for the append function in jsonl module."""

    def test_append_to_existing_file(self, tmp_path):
        """Test appending to an existing JSON Lines file."""
        original_data = [{"id": 1, "name": "Alice"}]
        append_data = [{"id": 2, "name": "Bob"}, {"id": 3, "name": "Charlie"}]
        jsonl_file = tmp_path / "append_existing.jsonl"

        # Write original data
        write(jsonl_file, original_data)

        # Append new data
        append(jsonl_file, append_data)

        # Verify combined data
        result = list(read(jsonl_file))
        expected = original_data + append_data
        assert result == expected

    def test_append_to_empty_file(self, tmp_path):
        """Test appending to an empty JSON Lines file."""
        append_data = [{"id": 1, "name": "Alice"}]
        jsonl_file = tmp_path / "append_empty.jsonl"

        # Create empty file
        write(jsonl_file, [])

        # Append data
        append(jsonl_file, append_data)

        result = list(read(jsonl_file))
        assert result == append_data

    def test_append_to_nonexistent_file(self, tmp_path):
        """Test appending to a non-existent JSON Lines file."""
        append_data = [{"id": 1, "name": "Alice"}]
        jsonl_file = tmp_path / "append_nonexistent.jsonl"

        # Append to non-existent file (should create it)
        append(jsonl_file, append_data)

        result = list(read(jsonl_file))
        assert result == append_data

    def test_append_empty_list(self, tmp_path):
        """Test appending empty list to JSON Lines file."""
        original_data = [{"id": 1, "name": "Alice"}]
        jsonl_file = tmp_path / "append_empty_list.jsonl"

        # Write original data
        write(jsonl_file, original_data)

        # Append empty list
        append(jsonl_file, [])

        # Verify data unchanged
        result = list(read(jsonl_file))
        assert result == original_data

    def test_append_single_item(self, tmp_path):
        """Test appending single item to JSON Lines file."""
        original_data = [{"id": 1, "name": "Alice"}]
        append_data = [{"id": 2, "name": "Bob"}]
        jsonl_file = tmp_path / "append_single.jsonl"

        write(jsonl_file, original_data)
        append(jsonl_file, append_data)

        result = list(read(jsonl_file))
        expected = original_data + append_data
        assert result == expected

    def test_append_with_unicode_content(self, tmp_path):
        """Test appending Unicode content to JSON Lines file."""
        original_data = [{"chinese": "你好"}]
        append_data = [{"emoji": "🌍🚀", "german": "Müller"}]
        jsonl_file = tmp_path / "append_unicode.jsonl"

        write(jsonl_file, original_data)
        append(jsonl_file, append_data)

        result = list(read(jsonl_file))
        expected = original_data + append_data
        assert result == expected

    def test_append_with_different_encoding(self, tmp_path):
        """Test appending with different encoding."""
        original_data = [{"message": "Hello"}]
        append_data = [{"message": "Café"}]
        jsonl_file = tmp_path / "append_encoding.jsonl"

        write(jsonl_file, original_data, encoding="latin-1")
        append(jsonl_file, append_data, encoding="latin-1")

        result = list(read(jsonl_file, encoding="latin-1"))
        expected = original_data + append_data
        assert result == expected

    def test_append_multiple_times(self, tmp_path):
        """Test appending multiple times to the same file."""
        data1 = [{"id": 1}]
        data2 = [{"id": 2}]
        data3 = [{"id": 3}]
        jsonl_file = tmp_path / "append_multiple.jsonl"

        write(jsonl_file, data1)
        append(jsonl_file, data2)
        append(jsonl_file, data3)

        result = list(read(jsonl_file))
        expected = data1 + data2 + data3
        assert result == expected

    def test_append_complex_data(self, tmp_path):
        """Test appending complex nested data."""
        original_data = [{"user": {"id": 1, "name": "Alice"}}]
        append_data = [{"order": {"id": "A1", "items": [{"name": "Book", "price": 19.99}]}}]
        jsonl_file = tmp_path / "append_complex.jsonl"

        write(jsonl_file, original_data)
        append(jsonl_file, append_data)

        result = list(read(jsonl_file))
        expected = original_data + append_data
        assert result == expected

    def test_append_path_as_string(self, tmp_path):
        """Test appending to JSON Lines file with path as string."""
        original_data = [{"id": 1}]
        append_data = [{"id": 2}]
        jsonl_file = tmp_path / "append_string.jsonl"

        write(jsonl_file, original_data)
        append(str(jsonl_file), append_data)

        result = list(read(jsonl_file))
        expected = original_data + append_data
        assert result == expected

    def test_append_large_dataset(self, tmp_path):
        """Test appending a large dataset."""
        original_data = [{"id": i} for i in range(500)]
        append_data = [{"id": i} for i in range(500, 1000)]
        jsonl_file = tmp_path / "append_large.jsonl"

        write(jsonl_file, original_data)
        append(jsonl_file, append_data)

        result = list(read(jsonl_file))
        expected = original_data + append_data
        assert result == expected
        assert len(result) == 1000

    def test_append_single_dict(self, tmp_path):
        """Test appending a single dictionary to JSON Lines file."""
        original_data = [{"id": 1, "name": "Alice"}]
        single_dict = {"id": 2, "name": "Bob"}
        jsonl_file = tmp_path / "append_single_dict.jsonl"

        write(jsonl_file, original_data)
        append(jsonl_file, single_dict)  # Append single dict, not list

        result = list(read(jsonl_file))
        expected = original_data + [single_dict]
        assert result == expected

    def test_append_single_dict_to_empty_file(self, tmp_path):
        """Test appending a single dictionary to an empty JSON Lines file."""
        single_dict = {"id": 1, "message": "Hello"}
        jsonl_file = tmp_path / "append_single_empty.jsonl"

        # Create empty file
        write(jsonl_file, [])

        # Append single dict
        append(jsonl_file, single_dict)

        result = list(read(jsonl_file))
        assert result == [single_dict]

    def test_append_single_dict_to_nonexistent_file(self, tmp_path):
        """Test appending a single dictionary to a non-existent JSON Lines file."""
        single_dict = {"id": 1, "data": "test"}
        jsonl_file = tmp_path / "append_single_nonexistent.jsonl"

        # Append single dict to non-existent file (should create it)
        append(jsonl_file, single_dict)

        result = list(read(jsonl_file))
        assert result == [single_dict]

    def test_append_single_dict_with_unicode(self, tmp_path):
        """Test appending a single dictionary with Unicode content."""
        original_data = [{"chinese": "你好"}]
        single_dict = {"emoji": "🌍🚀", "german": "Müller"}
        jsonl_file = tmp_path / "append_single_unicode.jsonl"

        write(jsonl_file, original_data)
        append(jsonl_file, single_dict)

        result = list(read(jsonl_file))
        expected = original_data + [single_dict]
        assert result == expected