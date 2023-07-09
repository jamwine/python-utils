import json


def save_output_in_json(output_file_path, data, data_description = ''):
    try:
        with open(output_file_path, 'w') as json_file:
            if data_description != '':
                json.dump({data_description: data}, json_file)
            else:
                json.dump({'data': data}, json_file)
        print(f"JSON file '{output_file_path}' saved successfully!\n")
    except Exception as exc:
        print(f"!! Failed to save JSON file '{output_file_path}'. !!\n", exc)