#! /usr/bin/python3
# Created by AG on 09-09-2025

import os
import sys
import click
from groq import Groq
from textwrap import dedent
from dotenv import load_dotenv
from utils import remove_docstring_sequences
from utils import insert_docstring_in_function
from utils import find_sequence_pairs, function_line
from utils import block_has_existing_docstring, strip_existing_docstring

load_dotenv()


def docnerd(code: str, model="llama-3.1-8b-instant") -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    SYSTEM = (
        "You write concise and precise google-styled python docstrings. "
        "Given a function or a code block, return ONLY the docstring content\
        (no triple quotes or fences)."
    )
    USER = f"Write a google-styled docstring for this function:\n\n```python\n{
        code}\n```"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system", "content": SYSTEM
            },
            {
                "role": "user", "content": USER
            }
        ],
        temperature=0.2,
        # reasoning_format="hidden"
    )

    docstring = response.choices[0].message.content.strip()
    docstring = docstring.strip("`")

    if docstring.startswith('"""') and docstring.endswith('"""'):
        docstring = docstring[3:-3].strip()

    if docstring.startswith("'''") and docstring.endswith("'''"):
        docstring = docstring[3:-3].strip()

    return docstring


def process_file(
    file_path: str,
    model: str = "llama-3.1-8b-instant",
    dry_run: bool = False,
    do_backup: bool = True,
    replace_existing_docstring: bool = False
):
    with open(file_path, "r", encoding="utf-8") as file:
        file_lines = file.readlines()

    changes = 0
    total_inserted = 0
    start_end_pairs = list(find_sequence_pairs(file_lines))
    if not start_end_pairs:
        click.echo("Docstring sequences not found!")
        return 0

    offset = 0
    for (start_sequence, end_sequence) in start_end_pairs:
        start_sequence += offset
        end_sequence += offset

        function_index = function_line(
            file_lines, start_sequence, end_sequence
        )
        if function_index is None:
            click.echo(f"No Function definition found between lines \
                       {start_sequence+1}–{end_sequence+1}.", err=True
                       )
            continue

        insert_at = function_index + 1
        if block_has_existing_docstring(file_lines, insert_at):
            if replace_existing_docstring:
                if strip_existing_docstring(file_lines, function_index):
                    # click.echo(f"Existing docstring removed at \
                    #            {function_index + 1}.")
                    offset -= 1
                #
                # else:
                #     click.echo(f"Couldn't strip existing docstring at \
                #                {function_index + 1}.", err=True)

            else:
                # click.echo(f"Function at line \
                #            {function_index + 1} already has a docstring.",
                #            err=True
                #            )
                continue

        code_snippet = dedent(
            "".join(file_lines[start_sequence + 1: end_sequence]).strip()
        )
        try:
            doc = docnerd(code_snippet, model=model)
        except Exception as e:
            click.echo(f"Error from Groq (lines {start_sequence + 1}–\
            {end_sequence + 1}): {e}", err=True)
            continue

        added = insert_docstring_in_function(file_lines, function_index, doc)
        total_inserted += added
        changes += 1
        offset += added

    if changes == 0:
        click.echo("Nothing to change.")
        return 0

    if dry_run:
        click.echo("Dry run complete, no file(s) written.")
        return changes

    if do_backup:
        with open(file_path, "r", encoding="utf-8") as original_file:
            original_contents = original_file.read()
        with open(file_path + ".bak", "w", encoding="utf-8") as backup_file:
            backup_file.write(original_contents)

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(file_lines)

    click.echo(f"Updated '{file_path}' with {changes} docstring(s). Inserted {total_inserted} line(s).")
    return changes


@click.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--model", default="llama-3.1-8b-instant", show_default=True, help="Choose the AI model to generate docstring.")
@click.option("--no-backup", is_flag=True, help="Choose whether a backup of the file will be generated or not.")
@click.option("--dry-run", is_flag=True, help="Preview original file without generating docstring.")
@click.option("--replace-existing-docstring", is_flag=True, help="Replace existing docstrings with AI generated ones.")
def main(
    file: str,
    model: str,
    no_backup: bool,
    dry_run: bool,
    replace_existing_docstring: bool
):
    if not os.getenv("GROQ_API_KEY"):
        click.echo(
            "GROQ_API_KEY is not set. Define it as an environment variable", err=True)
        sys.exit(1)

    process_file(
        file_path=file,
        model=model,
        dry_run=dry_run,
        do_backup=not no_backup,
        replace_existing_docstring=replace_existing_docstring
    )
    if not dry_run:
        remove_docstring_sequences(file)


if __name__ == "__main__":
    main()
