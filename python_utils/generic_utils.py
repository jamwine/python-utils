import json


def save_output_in_json(output_file_path, data, data_description = ''):
    try:
        with open(output_file_path, 'w', encoding='utf8') as json_file:
            if data_description != '':
                json.dump({data_description: data}, json_file, ensure_ascii=False)
            else:
                json.dump({'data': data}, json_file)
        print(f"JSON file '{output_file_path}' saved successfully!\n")
    except Exception as exc:
        print(f"!! Failed to save JSON file '{output_file_path}'. !!\n", exc)


def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print(f"JSON file '{file_path}' loaded successfully!\n")
            return data
    except Exception as exc:
        print(f"!! Failed to load JSON file '{file_path}'. !!\n", exc)
    