#! /usr/bin/python3
# Created by AG on 09-09-2025

import re
import click

START_SEQUENCE = re.compile(r"^\s*#\s*DOCSTRING\s*START\s*$", re.IGNORECASE)
END_SEQUENCE = re.compile(r"^\s*#\s*DOCSTRING\s*END\s*$", re.IGNORECASE)
FUNCTION_SEQUENCE = re.compile(r"^\s*(async\s+def|def)\s+\w+\s*\(.*\)\s*:\s*$")
PYTHON_DOCSTRING_SEQUENCE = re.compile(r'^\s*(?P<q>["\']{3})')


def find_sequence_pairs(file_lines: str):
    current_line: int = 0
    while current_line < len(file_lines):
        if START_SEQUENCE.match(file_lines[current_line]):
            end_sequence_line: int = current_line + 1
            while end_sequence_line < len(file_lines) and not \
                    END_SEQUENCE.match(file_lines[end_sequence_line]):
                end_sequence_line += 1
            if end_sequence_line >= len(file_lines):
                click.echo(
                    "START sequence has no matching END sequence!", err=True)
                break
            yield (current_line, end_sequence_line)
            current_line = end_sequence_line + 1
        else:
            current_line += 1


def function_line(
    file_lines: str,
    start_line: int,
    end_line: int
) -> None | int:
    for index in range(start_line, end_line + 1):
        if FUNCTION_SEQUENCE.match(file_lines[index]):
            return index
    return None


def block_has_existing_docstring(
    file_lines: str,
    insert_at: int
) -> bool:
    while insert_at < len(file_lines) and \
            (file_lines[insert_at].strip() == "" or
             file_lines[insert_at].lstrip().startswith("#")):
        insert_at += 1

    if insert_at < len(file_lines) and \
            PYTHON_DOCSTRING_SEQUENCE.match(file_lines[insert_at].lstrip()):
        return True

    return False


def make_indent_after_function(file_lines: str, function_line: int) -> int:
    function_indent = len(
        file_lines[function_line]) - len(file_lines[function_line].lstrip(" "))
    current_line = function_line + 1
    while current_line < len(file_lines) and \
            file_lines[current_line].strip() == "":
        current_line += 1

    if current_line < len(file_lines):
        indent = len(file_lines[current_line]) - \
            len(file_lines[current_line].lstrip(" "))
        if indent > function_indent:
            return indent
    return function_indent + 4


def insert_docstring_in_function(
    file_lines: str,
    function_index: int,
    docstring: str
) -> int:
    indent_space = make_indent_after_function(
        file_lines=file_lines,
        function_line=function_index
    )
    indent = " " * indent_space
    code_block: list = [
        f"{indent}\"\"\"\n",
        * [
            (indent + line + ("\n" if not line.endswith("\n") else ""))
            for line in docstring.splitlines()
        ],
        "\n" if not docstring.endswith("\n") else "",
        f"{indent}\"\"\"\n",
    ]

    file_lines[function_index + 1: function_index + 1] = code_block
    return len(code_block)
