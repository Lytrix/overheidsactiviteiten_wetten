#  Overheidsactiviteiten #

[Vereniging Nederlandse Gemeenten](https://www.vng.nl) Published a [list of government activities]()https://vng.nl/files/vng/brieven/2014/attachments/20140709_aanzet-voor-een-lijst-met-overheidsactiviteiten.pdf in 2014 related to their public rights and laws which allow them to use certain data.

This script extracts all tables from a multipage pdf and export to JSON, CSV or TSV and parses the table to a system readable json array.

## Usage

```
git clone https://github.com/Lytrix/overheidsactiviteiten_wetten
cd overheidsactiviteiten_wetten
python3 -m venv env
source venv/bin/activate
pip install requirements.txt
python parse_overheidsactiviteiten_pdf_tables.py
```
This will create a usable json file from the pdf tables.

## Prequisits
It uses a java program, which will be automatically downloaded if it is not present in the root directory. 
If it script fails to do this it can be downloaded here:

https://github.com/tabulapdf/tabula-java/releases

To download JAVA, go here:

https://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html#jdk-7u11-oth-JPR

More information found can be found here:

https://dirkmjk.nl/en/2017/04/how-automate-extracting-tables-pdfs-using-tabula
