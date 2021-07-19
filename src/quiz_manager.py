"""
    Quiz Manager is a script that helps with the convertion and generation of quizzes.
"""

import click

@click.group()
def cli():
    """
        Entrypoint of the application
    """

@cli.command()
@click.option('-i', '--input-file', 'input_file_path', required=True,
    help='Input file path')
@click.option('-o', '--output-file', 'output_file_path', required=True,
    help='Output file path')
@click.option('-if', '--input-format', type=click.Choice(['JSON', 'HR', 'MXML'],
    case_sensitive=False), help='The input format')
@click.option('-of', '--output-format', type=click.Choice(['JSON', 'HR', 'MXML'],
    case_sensitive=False), help='The output format')
def convert(input_file_path, output_file_path, input_format, output_format):
    """
        Converts files to different formats.
    """
    if input_format is None:
        if input_file_path.split('.')[-1].lower() in ['json', 'hr', 'mxml']:
            input_format = input_file_path.split('.')[-1].upper()
        else:
            raise click.UsageError('Input format can\'t be extracted from input'\
                ' file extention. Use --input-format to specify the input format.')

    if output_format is None:
        if output_file_path.split('.')[-1].lower() in ['json', 'hr', 'mxml']:
            output_format = output_file_path.split('.')[-1].upper()
        else:
            raise click.UsageError('Output format can\'t be extracted from output'\
                ' file extention. Use --output-format to specify the output format.')


    print(f"Converting from {input_format} to {output_format}")
    print(f"Paths:\n\tinput: {input_file_path}\n\toutput: {output_file_path}")

    with open(input_file_path, 'r', encoding="UTF-8") as input_file:
        input_content = input_file.read()

    # TODO: Add conversion here
    conversion = ''

    with open(output_file_path, 'w', encoding="UTF-8") as output_file:
        output_file.write(conversion)

if __name__ == '__main__':
    cli()