import json
import PySimpleGUI as SG
import os


def get_import_template_fields(file_name="product-import-template.-fields.csv"):
    if file_name.count('.') < 1:
        file_name += '.csv'
    with open('product-import-template.-fields.csv', encoding='UTF-8') as file:
        return [name.strip() for name in file]


def get_csv_file_content(file_name: str) -> dict:
    if file_name.count('.') < 1:
        file_name += '.csv'

    headers = []
    products = []
    flag = True
    with open('NEW PRODUCTS IMPORT.csv', encoding='UTF-8') as file:
        for line in file:
            if flag:
                headers = line.strip().split(';')
                flag = False
                continue
            products.append(line.strip().split(';'))
    return {
        "headers": headers,
        "products": products
    }


def save_to_json(folder: str, file_name: str, save: str):
    if file_name.count('.') < 1:
        file_name += '.csv'

    import_feed = {
        'product': []
    }

    headers = get_csv_file_content(file_name)['headers']
    products = get_csv_file_content(file_name)['products']

    for i in range(len(products)):
        product = {}
        for j in range(len(headers)):
            product[headers[j]] = products[i][j]
        import_feed['product'].append(product)

    print(json.dumps(import_feed, indent=4, sort_keys=True))
    with open(f'{folder}/{save}.json', 'w', encoding="UTF-8") as outfile:
        json.dump(import_feed, outfile, indent=4, sort_keys=True)


if __name__ == '__main__':
    """
    print(get_import_template_fields(), end='\n\n')
    print(get_csv_file_content(), end='\n\n')
    save_to_json()
    """
    layout = [
        [
            [
                SG.Text("Chosen File: "),
                SG.In(size=(79, 1), enable_events=True, key="-FILE-"),
                SG.FileBrowse(),
            ],
            [
                SG.Text("Created File: "),
                SG.Input(size=(79, 1), enable_events=True, key="-SAVED-"),
                SG.Button("Submit name", enable_events=True, key="-SUBMITTED_SAVE-"),
            ],
            [
                SG.Text("Location to save JSON: "),
                SG.In(size=(70, 1), enable_events=True, key="-LOCATION-"),
                SG.FolderBrowse(),
                SG.Button("Submit (convert)", enable_events=True, key="-SUBMITTED-"),
            ],
            [
                SG.HSeparator(),
            ],
            [
                SG.Text("", key="-MSG-"),
            ],
        ]
    ]

    window = SG.Window(title="Excel (CSV) to *.json converter", layout=layout)

    is_file_set, is_save_set, is_location_set = False, False, False
    while True:
        event, values = window.read()
        if event == "Exit" or event == SG.WIN_CLOSED:
            break

        if event == "-FILE-":
            file = values["-FILE-"]
            is_file_set = True
            print(file)
        if event == "-LOCATION-":
            location = values["-LOCATION-"]
            is_location_set = True
            print(location)
        if event == "-SUBMITTED_SAVE-":
            saved = values["-SAVED-"]
            is_save_set = True
            print(saved)
        if event == "-SUBMITTED-" and is_file_set and is_save_set and is_location_set:
            print(get_import_template_fields(), end='\n\n')
            print(get_csv_file_content(file_name=values["-FILE-"]), end='\n\n')
            save_to_json(folder=values["-LOCATION-"], save=values["-SAVED-"], file_name=values["-FILE-"])
            window.Element("-MSG-").update("File is saved correctly.")

    window.close()
