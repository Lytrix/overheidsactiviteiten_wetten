import os
import argparse
import requests
from os import errno


def create_dir_if_not_exists(directory):
    """
    Create directory if it does not yet exists.
    Args:
        Specify the name of directory, for example: `dir/anotherdir`
    Returns:
        Creates the directory if it does not exists, of return the error message.
    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def extract_pdf_tables(pdf_folder, output_folder, export_format):
    """
    Extract tables from multiple pdfs.
    Args:

    - pdf_folder: path of pdf files
    - export_format: JSON, TSV, CSV

    Result:

    - Exported tables in output folder
    """

    # Install jar file if it is not yet downloaded.
    if not os.path.isfile('tabula-1.0.2-jar-with-dependencies.jar'):
        url = 'https://github.com/tabulapdf/tabula-java/releases/download/v1.0.2/tabula-1.0.2-jar-with-dependencies.jar'
        response = requests.get(url)
        filename = url.split('/')[-1]
        open(filename, 'wb').write(response.content)

    export_format = export_format.upper()
    create_dir_if_not_exists(pdf_folder)
    create_dir_if_not_exists(output_folder)

    base_command = 'java -jar tabula-1.0.2-jar-with-dependencies.jar -p all -f {} -o {} {}'

    for filename in os.listdir(pdf_folder):
        pdf_path = os.path.join(pdf_folder, filename)
        output_path = os.path.join(output_folder, filename.lower().replace('.pdf', '.{}'.format(export_format.lower())))
        command = base_command.format(export_format, output_path, pdf_path)
        os.system(command)


def parser():
    """
    Parser function to run arguments from commandline and to add description to sphinx docs.
    To see possible styling options: https://pythonhosted.org/an_example_pypi_project/sphinx.html
    """
    description = """
    Extract all tables from a multipage pdf and export to JSON, CSV or TSV.

    Example command line:
        ``python extract_tables_from_pdfs.py pdf output json``

    Prequisits:
    It uses a java backend, which can be downloaded here:

        https://github.com/tabulapdf/tabula-java/releases

    To download JAVA, go here:

        https://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html#jdk-7u11-oth-JPR

    More information found here:

        https://dirkmjk.nl/en/2017/04/how-automate-extracting-tables-pdfs-using-tabula
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('pdf_folder',
                        type=str,
                        help='Specify folder where the pdfs are in')
    parser.add_argument('output_folder',
                        type=str,
                        help='Specify folder where the files are written to')
    parser.add_argument('export_format',
                        type=str,
                        help='Choose export format: JSON, CSV, TSV')

    return parser


def main():
    args = parser().parse_args()
    extract_pdf_tables(args.pdf_folder, args.output_folder, args.export_format)


if __name__ == '__main__':
    main()
