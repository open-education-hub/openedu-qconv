"""
    Quiz Manager is a script that helps with the convertion and generation of quizzes.
"""

import re
import sys
import json
import glob
import click
from parsers import mxml
from parsers import md


@click.group()
def cli():
    """
    Entrypoint of the application
    """


@cli.command()
@click.option(
    "-i", "--input-file", "input_file_path", required=False, help="Input file path"
)
@click.option(
    "-d", "--input-path", "input_dir_path", required=False, help="Input directory (read all `.input_format` files from the input path)"
)
@click.option(
    "-o", "--output-file", "output_file_path", required=False, help="Output file path"
)
@click.option(
    "-od", "--output-path", "output_dir_path", required=False, help="Output directory (write questions in `Question_Title.output_format` files)"
)
@click.option(
    "-if",
    "--input-format",
    type=click.Choice(["JSON", "XML", "MD"], case_sensitive=False),
    help="The input format",
)
@click.option(
    "-of",
    "--output-format",
    type=click.Choice(["JSON", "XML", "MD"], case_sensitive=False),
    help="The output format",
)
@click.option(
    "-c",
    "--category",
    required=False,
    help="Category specifier for XML quizzes",
)
def convert(input_file_path, input_dir_path, output_file_path, output_dir_path, input_format, output_format, category=None):
    """
    Converts files to different formats.
    """
    if input_file_path is None and input_dir_path is None:
        raise click.UsageError(
            "One of --input-path or --input-file must be set."
        )

    if output_dir_path is None and output_file_path is None:
        raise click.UsageError(
            "One of --output-path or --output-file must be set."
        )

    if input_format is None:
        if input_file_path is None:
            raise click.UsageError(
                "--input-format must be specified if using --input-path"
            )

        if input_file_path.split(".")[-1].lower() in ["json", "xml", "md"]:
            input_format = input_file_path.split(".")[-1].upper()
        else:
            raise click.UsageError(
                "Input format can't be extracted from input"
                " file extention. Use --input-format to specify the input format."
            )

    if output_format is None:
        if output_file_path is None:
            raise click.UsageError(
                "--output-format must be specified if using --output-path"
            )

        if output_file_path.split(".")[-1].lower() in ["json", "xml", "md"]:
            output_format = output_file_path.split(".")[-1].upper()
        else:
            raise click.UsageError(
                "Output format can't be extracted from output"
                " file extention. Use --output-format to specify the output format."
            )

    print(f"Converting from {input_format} to {output_format}")
    print(f"Paths:\n\tinput: {input_file_path}\n\toutput: {output_file_path}")

    input_content = ""

    if input_file_path is not None:
        with open(input_file_path, "r", encoding="UTF-8") as input_file:
            input_content = input_file.read().rstrip('\n')

    if input_dir_path is not None:
        read_files = glob.glob(input_dir_path + "/*.md")
        for f in read_files:
            with open(f, "rb") as infile:
                input_content += infile.read().decode("utf-8")
            input_content += "\n\n"

    input_content = input_content.rstrip("\n")

    conversion = ""
    if input_format == "JSON":
        if output_format == "XML":
            conversion = mxml.quiz_json_to_mxml(json.loads(input_content), category)
        elif output_format == "MD":
            conversion = md.quiz_json_to_md(json.loads(input_content))
    elif input_format == "XML":
        if output_format == "JSON":
            conversion = mxml.quiz_mxml_to_json(input_content)
        elif output_format == "MD":
            conversion = md.quiz_json_to_md(json.loads(mxml.quiz_mxml_to_json(input_content)))
    elif input_format == "MD":
        if output_format == "JSON":
            conversion = md.quiz_md_to_json(input_content)
        if output_format == "XML":
            conversion = mxml.quiz_json_to_mxml(json.loads(md.quiz_md_to_json(input_content)))

    if output_dir_path is None:
        with open(output_file_path, "w", encoding="UTF-8") as output_file:
            output_file.write(''.join(conversion))
    else:
        if output_format == "MD":
            for q in conversion:
                q_name = re.sub('[`().,;:?"/]', '', q.partition('\n')[0][2:])
                q_name = re.sub(' ', '_', q_name)
                with open(output_dir_path + "/" + q_name + ".md", "w", encoding="UTF-8") as output_file:
                    output_file.write(q.strip("\n"))


if __name__ == "__main__":
    cli()
