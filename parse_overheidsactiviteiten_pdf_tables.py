# coding: utf8
import json
import re
import urllib.parse
from extract_tables_from_pdfs import extract_pdf_tables


def split_to_keys(elements):
    wetten = []
    wet = {}
    for words in elements:
        """
        Create Artikel elements
        """
        if words[:3] == 'Art':
            wet = {"Artikel": words.split(' ', 1)[1]}
        elif words.lower().find('wet') != -1:
            wet["Wet"] = words
            wet["url"] = "https://wetten.overheid.nl/{}".format(urllib.parse.quote(words))
            wetten.append(wet)
            wet = {}
        else:
            wetten.append(words)
    return wetten


def split_on_caps(string):
    """
    Split single string to elements in an array
    """
    regex = re.findall(r'[A-Z]+[^A-Z\(\)\-]*', string)
    elements = []
    for words in regex:
        words = words.strip()
        elements.append(words)
    elements = split_to_keys(elements)
    return elements


def remove_newline(string):
    string = " ".join(string.splitlines())
    return string


def cleanup_json(json_file):
    """
    Cleanup exported json from pdf
    """
    overheidstaken = []
    data = None
    json_dict = json.load(json_file)
    totaldata = [item['data'] for item in json_dict]
    for dataset in totaldata:
        if data:
            data = data + dataset
        else:
            data = dataset
    for index, item in enumerate(data):
        for subitem in item:
            if subitem['text'] == 'Activiteiten':
                del data[index]
                break
    for item in data:
        if len(item) > 3:
            for subitem in item:
                if subitem['left'] < 70 and subitem['text'] != '':
                    hoofdactiviteit = remove_newline(subitem['text'])
            if item[1]['text'] == '':  # ignore empty row
                continue
            else:
                activiteiten = split_on_caps(remove_newline(item[1]['text']))
                for activiteit in activiteiten:
                    activiteit = {"Hoofdactiviteit": hoofdactiviteit,
                                  "Activiteit": activiteit}
                    if len(item) > 2 and item[3]['text'] != '':
                        if item[3]['text'] == 'Idem':
                            activiteit["Wettelijke grondslag"] = overheidstaken[-1]["Wettelijke grondslag"]
                        else:
                            wettelijke_grondslag = remove_newline(item[3]['text'])
                            wettelijke_grondslag = split_on_caps(wettelijke_grondslag)
                            activiteit["Wettelijke grondslag"] = wettelijke_grondslag
                    else:
                        activiteit["Wettelijke grondslag"] = [{"Artikel": None, "Wet": 'Geen'}]
                    overheidstaken.append(activiteit)
    print(overheidstaken)
    overheidstaken = {"overheidstaken": overheidstaken, 
                      "metadata": {"bron": "https://vng.nl/files/vng/brieven/2014/attachments/20140709_aanzet-voor-een-lijst-met-overheidsactiviteiten.pdf"}}
    return overheidstaken


def main():
    extract_pdf_tables('pdf','output','json')
    with open('output/20140709_aanzet-voor-een-lijst-met-overheidsactiviteiten.json', 'r') as json_str:
        overheidstaken = cleanup_json(json_str)
    with open('overheidsactiviteiten_publiekrechtelijke_bevoegdheden_20140709.json', 'w') as outfile:
        json.dump(overheidstaken, outfile, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
