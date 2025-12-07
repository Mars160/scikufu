"""Tests for scikufu.file.text module."""

import pytest


from scikufu.file.text import read, write, append


class TestTextRead:
    """Test cases for the read function in text module."""

    def test_read_simple_text_file(self, tmp_path):
        """Test reading a simple text file."""
        test_content = "Hello, World!"
        text_file = tmp_path / "simple.txt"

        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        result = read(text_file)
        assert result == test_content

    def test_read_multiline_text_file(self, tmp_path):
        """Test reading a multiline text file."""
        test_content = """Line 1
Line 2
Line 3
This is a longer line with some text.
The end."""

        text_file = tmp_path / "multiline.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        result = read(text_file)
        assert result == test_content

    def test_read_empty_text_file(self, tmp_path):
        """Test reading an empty text file."""
        text_file = tmp_path / "empty.txt"

        with open(text_file, "w", encoding="utf-8") as f:
            f.write("")

        result = read(text_file)
        assert result == ""

    def test_read_text_file_with_whitespace(self, tmp_path):
        """Test reading a text file with various whitespace characters."""
        test_content = "  \t\n  Text with spaces\n\tand tabs\n\nand newlines  \t\n"

        text_file = tmp_path / "whitespace.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        result = read(text_file)
        assert result == test_content

    def test_read_text_file_with_utf8_encoding(self, tmp_path):
        """Test reading a text file with UTF-8 encoding containing Unicode characters."""
        test_content = """中文内容
Hello 世界
Emoji: 🌍🚀💻
Special chars: áéíóú ñ ß
German: Müller
Russian: Привет мир
Arabic: مرحبا بالعالم"""

        text_file = tmp_path / "utf8.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        result = read(text_file, encoding="utf-8")
        assert result == test_content

    def test_read_text_file_with_different_encoding(self, tmp_path):
        """Test reading a text file with different encoding."""
        test_content = "Café résumé naïve"

        # Test with latin-1 encoding
        text_file = tmp_path / "latin1.txt"
        with open(text_file, "w", encoding="latin-1") as f:
            f.write(test_content)

        result = read(text_file, encoding="latin-1")
        assert result == test_content

    def test_read_text_file_with_ascii_encoding(self, tmp_path):
        """Test reading a text file with ASCII encoding."""
        test_content = "Simple ASCII text: Hello, World! 123"

        text_file = tmp_path / "ascii.txt"
        with open(text_file, "w", encoding="ascii") as f:
            f.write(test_content)

        result = read(text_file, encoding="ascii")
        assert result == test_content

    def test_read_text_file_path_as_string(self, tmp_path):
        """Test reading text file with path provided as string."""
        test_content = "Path as string test"
        text_file = tmp_path / "string_path.txt"

        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        # Use string path instead of Path object
        result = read(str(text_file))
        assert result == test_content

    def test_read_text_file_path_as_pathlike(self, tmp_path):
        """Test reading text file with path provided as PathLike object."""
        test_content = "PathLike object test"
        text_file = tmp_path / "pathlike.txt"

        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        # Use Path object
        result = read(text_file)
        assert result == test_content

    def test_read_text_file_not_found(self):
        """Test reading a text file that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            read("/path/that/does/not/exist.txt")

    def test_read_large_text_file(self, tmp_path):
        """Test reading a large text file."""
        # Create a large text content
        lines = [f"This is line {i} with some content." for i in range(1000)]
        test_content = "\n".join(lines)

        text_file = tmp_path / "large.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        result = read(text_file)
        assert result == test_content
        assert len(result.splitlines()) == 1000

    def test_read_text_file_with_special_characters(self, tmp_path):
        """Test reading text file with special characters."""
        test_content = """Special characters test:
!@#$%^&*()_+-=[]{}|;':",./<>?
Backslash: \\
Quotes: ' and "
Tab: \t
Newline: \n"""

        text_file = tmp_path / "special_chars.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        result = read(text_file)
        assert result == test_content

    def test_read_text_file_with_numbers(self, tmp_path):
        """Test reading text file containing numbers."""
        test_content = """Numbers test:
Integer: 42
Float: 3.14159
Scientific: 1.23e-4
Negative: -123
Mixed: 42 is the answer to life, universe and everything."""

        text_file = tmp_path / "numbers.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        result = read(text_file)
        assert result == test_content

    def test_read_text_file_with_mixed_line_endings(self, tmp_path):
        """Test reading text file with different line ending styles."""
        test_content_original = "Line 1\r\nLine 2\nLine 3\r\nLine 4\n"
        # Python's text mode normalizes line endings, so we expect \r\n to become \n
        test_content_expected = "Line 1\nLine 2\nLine 3\nLine 4\n"

        text_file = tmp_path / "line_endings.txt"
        with open(text_file, "wb") as f:
            f.write(test_content_original.encode("utf-8"))

        result = read(text_file)
        assert result == test_content_expected

    def test_read_text_file_default_encoding(self, tmp_path):
        """Test reading text file with default UTF-8 encoding."""
        test_content = "Default encoding test"
        text_file = tmp_path / "default_encoding.txt"

        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        # Don't specify encoding parameter
        result = read(text_file)
        assert result == test_content

    def test_read_text_file_with_emoji(self, tmp_path):
        """Test reading text file containing emoji."""
        test_content = "Emoji test: 😀😎🚀💻🌍⭐🎉"
        text_file = tmp_path / "emoji.txt"

        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        result = read(text_file)
        assert result == test_content

    def test_read_text_file_with_xml_content(self, tmp_path):
        """Test reading text file containing XML-like content."""
        test_content = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <item id="1">First item</item>
    <item id="2">Second item</item>
</root>"""

        text_file = tmp_path / "xml_content.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        result = read(text_file)
        assert result == test_content

    def test_read_text_file_with_json_content(self, tmp_path):
        """Test reading text file containing JSON content (as text)."""
        test_content = '{"name": "test", "value": 42, "active": true}'
        text_file = tmp_path / "json_as_text.txt"

        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        result = read(text_file)
        assert result == test_content
        # Verify it's returned as string, not parsed as JSON
        assert isinstance(result, str)

    def test_read_text_file_with_source_code(self, tmp_path):
        """Test reading text file containing source code."""
        test_content = """def hello_world():
    \"\"\"A simple function that prints hello world.\"\"\"
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()"""

        text_file = tmp_path / "source_code.py"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        result = read(text_file)
        assert result == test_content


class TestTextWrite:
    """Test cases for the write function in text module."""

    def test_write_simple_text(self, tmp_path):
        """Test writing simple text content to a file."""
        test_content = "Hello, World!"
        text_file = tmp_path / "write_simple.txt"

        write(text_file, test_content)

        result = read(text_file)
        assert result == test_content

    def test_write_empty_text(self, tmp_path):
        """Test writing empty text to a file."""
        test_content = ""
        text_file = tmp_path / "write_empty.txt"

        write(text_file, test_content)

        result = read(text_file)
        assert result == ""

    def test_write_multiline_text(self, tmp_path):
        """Test writing multiline text content."""
        test_content = """Line 1
Line 2
Line 3
This is a longer line."""
        text_file = tmp_path / "write_multiline.txt"

        write(text_file, test_content)

        result = read(text_file)
        assert result == test_content

    def test_write_with_unicode_content(self, tmp_path):
        """Test writing Unicode content."""
        test_content = """中文内容
Hello 世界
Emoji: 🌍🚀💻
Special chars: áéíóú ñ ß"""
        text_file = tmp_path / "write_unicode.txt"

        write(text_file, test_content)

        result = read(text_file)
        assert result == test_content

    def test_write_with_different_encoding(self, tmp_path):
        """Test writing text with different encoding."""
        test_content = "Café résumé naïve"
        text_file = tmp_path / "write_encoding.txt"

        write(text_file, test_content, encoding="latin-1")

        result = read(text_file, encoding="latin-1")
        assert result == test_content

    def test_write_overwrites_existing_file(self, tmp_path):
        """Test that write overwrites existing file content."""
        original_content = "Original content"
        new_content = "New content"
        text_file = tmp_path / "overwrite.txt"

        # Write original content
        write(text_file, original_content)
        result = read(text_file)
        assert result == original_content

        # Write new content (should overwrite)
        write(text_file, new_content)
        result = read(text_file)
        assert result == new_content

    def test_write_with_special_characters(self, tmp_path):
        """Test writing text with special characters."""
        test_content = """Special characters:
!@#$%^&*()_+-=[]{}|;':",./<>?
Backslash: \\
Quotes: ' and "
Tab: \t
Newline: \n"""
        text_file = tmp_path / "write_special.txt"

        write(text_file, test_content)

        result = read(text_file)
        assert result == test_content

    def test_write_with_numbers(self, tmp_path):
        """Test writing text containing numbers."""
        test_content = """Numbers test:
Integer: 42
Float: 3.14159
Scientific: 1.23e-4
Negative: -123"""
        text_file = tmp_path / "write_numbers.txt"

        write(text_file, test_content)

        result = read(text_file)
        assert result == test_content

    def test_write_large_text(self, tmp_path):
        """Test writing large text content."""
        lines = [f"This is line {i} with some content." for i in range(1000)]
        test_content = "\n".join(lines)
        text_file = tmp_path / "write_large.txt"

        write(text_file, test_content)

        result = read(text_file)
        assert result == test_content
        assert len(result.splitlines()) == 1000

    def test_write_path_as_string(self, tmp_path):
        """Test writing to file with path provided as string."""
        test_content = "Path as string test"
        text_file = tmp_path / "write_string.txt"

        write(str(text_file), test_content)

        result = read(text_file)
        assert result == test_content

    def test_write_with_emoji(self, tmp_path):
        """Test writing text containing emoji."""
        test_content = "Emoji test: 😀😎🚀💻🌍⭐🎉"
        text_file = tmp_path / "write_emoji.txt"

        write(text_file, test_content)

        result = read(text_file)
        assert result == test_content

    def test_write_xml_content(self, tmp_path):
        """Test writing XML-like content."""
        test_content = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <item id="1">First item</item>
    <item id="2">Second item</item>
</root>"""
        text_file = tmp_path / "write_xml.txt"

        write(text_file, test_content)

        result = read(text_file)
        assert result == test_content

    def test_write_json_content(self, tmp_path):
        """Test writing JSON content as text."""
        test_content = '{"name": "test", "value": 42, "active": true}'
        text_file = tmp_path / "write_json.txt"

        write(text_file, test_content)

        result = read(text_file)
        assert result == test_content
        assert isinstance(result, str)  # Should be string, not parsed JSON

    def test_write_source_code(self, tmp_path):
        """Test writing source code content."""
        test_content = """def hello_world():
    \"\"\"A simple function that prints hello world.\"\"\"
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()"""
        text_file = tmp_path / "write_code.py"

        write(text_file, test_content)

        result = read(text_file)
        assert result == test_content


class TestTextAppend:
    """Test cases for the append function in text module."""

    def test_append_to_existing_file(self, tmp_path):
        """Test appending to an existing text file."""
        original_content = "Original content"
        append_content = "Appended content"
        text_file = tmp_path / "append_existing.txt"

        # Write original content
        write(text_file, original_content)

        # Append new content
        append(text_file, append_content)

        result = read(text_file)
        assert result == original_content + append_content

    def test_append_to_empty_file(self, tmp_path):
        """Test appending to an empty file."""
        append_content = "First content"
        text_file = tmp_path / "append_empty.txt"

        # Create empty file
        write(text_file, "")

        # Append content
        append(text_file, append_content)

        result = read(text_file)
        assert result == append_content

    def test_append_to_nonexistent_file(self, tmp_path):
        """Test appending to a non-existent file."""
        append_content = "First content"
        text_file = tmp_path / "append_nonexistent.txt"

        # Append to non-existent file (should create it)
        append(text_file, append_content)

        result = read(text_file)
        assert result == append_content

    def test_append_empty_string(self, tmp_path):
        """Test appending empty string."""
        original_content = "Original content"
        text_file = tmp_path / "append_empty_string.txt"

        write(text_file, original_content)
        append(text_file, "")

        result = read(text_file)
        assert result == original_content

    def test_append_multiline_content(self, tmp_path):
        """Test appending multiline content."""
        original_content = "First line"
        append_content = "\nSecond line\nThird line"
        text_file = tmp_path / "append_multiline.txt"

        write(text_file, original_content)
        append(text_file, append_content)

        result = read(text_file)
        expected = original_content + append_content
        assert result == expected

    def test_append_with_unicode_content(self, tmp_path):
        """Test appending Unicode content."""
        original_content = "English content"
        append_content = "中文内容 🌍🚀"
        text_file = tmp_path / "append_unicode.txt"

        write(text_file, original_content)
        append(text_file, append_content)

        result = read(text_file)
        expected = original_content + append_content
        assert result == expected

    def test_append_with_different_encoding(self, tmp_path):
        """Test appending with different encoding."""
        original_content = "Hello"
        append_content = "Café résumé"
        text_file = tmp_path / "append_encoding.txt"

        write(text_file, original_content, encoding="latin-1")
        append(text_file, append_content, encoding="latin-1")

        result = read(text_file, encoding="latin-1")
        expected = original_content + append_content
        assert result == expected

    def test_append_multiple_times(self, tmp_path):
        """Test appending multiple times to the same file."""
        content1 = "First"
        content2 = "Second"
        content3 = "Third"
        text_file = tmp_path / "append_multiple.txt"

        write(text_file, content1)
        append(text_file, content2)
        append(text_file, content3)

        result = read(text_file)
        expected = content1 + content2 + content3
        assert result == expected

    def test_append_with_newlines(self, tmp_path):
        """Test appending content with newlines."""
        original_content = "Line 1\n"
        append_content = "Line 2\nLine 3\n"
        text_file = tmp_path / "append_newlines.txt"

        write(text_file, original_content)
        append(text_file, append_content)

        result = read(text_file)
        expected = original_content + append_content
        assert result == expected

    def test_append_with_spaces_and_tabs(self, tmp_path):
        """Test appending content with spaces and tabs."""
        original_content = "Start\t"
        append_content = "  Middle  \tEnd"
        text_file = tmp_path / "append_whitespace.txt"

        write(text_file, original_content)
        append(text_file, append_content)

        result = read(text_file)
        expected = original_content + append_content
        assert result == expected

    def test_append_special_characters(self, tmp_path):
        """Test appending special characters."""
        original_content = "Normal text"
        append_content = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        text_file = tmp_path / "append_special.txt"

        write(text_file, original_content)
        append(text_file, append_content)

        result = read(text_file)
        expected = original_content + append_content
        assert result == expected

    def test_append_with_emoji(self, tmp_path):
        """Test appending emoji content."""
        original_content = "Text: "
        append_content = "😀😎🚀💻🌍"
        text_file = tmp_path / "append_emoji.txt"

        write(text_file, original_content)
        append(text_file, append_content)

        result = read(text_file)
        expected = original_content + append_content
        assert result == expected

    def test_append_path_as_string(self, tmp_path):
        """Test appending to file with path as string."""
        original_content = "Original"
        append_content = "Appended"
        text_file = tmp_path / "append_string.txt"

        write(text_file, original_content)
        append(str(text_file), append_content)

        result = read(text_file)
        expected = original_content + append_content
        assert result == expected

    def test_append_large_content(self, tmp_path):
        """Test appending large content."""
        original_lines = [f"Original line {i}\n" for i in range(100)]
        append_lines = [f"Append line {i}\n" for i in range(100, 200)]

        original_content = "".join(original_lines)
        append_content = "".join(append_lines)
        text_file = tmp_path / "append_large.txt"

        write(text_file, original_content)
        append(text_file, append_content)

        result = read(text_file)
        expected = original_content + append_content
        assert result == expected
        assert len(result.splitlines()) == 200
