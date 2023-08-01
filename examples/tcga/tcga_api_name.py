import requests
import json
import numpy as np
import humanize
import csv
import glob
import os

# The base URL for the GDC API
base_url = "https://api.gdc.cancer.gov/"

# The endpoint for getting file data
endpoint = "files/"

def read_files_in_directory(directory_path):
    file_contents = {}

    # List all .txt files in the given directory
    txt_files = glob.glob(os.path.join(directory_path, '*.txt'))

    for file_path in txt_files:
        # Extract the file name without extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Read the content of the file and store it as a list of lines
        with open(file_path, 'r') as file:
            content = file.readlines()
            file_contents[file_name] = [x.split('\n')[0] for x in content]

    return file_contents

def find_duplicates(input_list):
    return [item for item in set(input_list) if input_list.count(item) > 1]


organs = read_files_in_directory('.')

for organ, file_names in organs.items():
    # Parameters for the API request
    params = {
        "filters": json.dumps({
            "op": "and",
            "content":[
                {
                "op": "in",
                "content":{
                    "field": "file_name",
                    "value": file_names
                    }
                },
                {
                "op": "in",
                "content":{
                    "field": "files.data_format",
                    "value": ["SVS"]
                    }
                }
            ]
        }),
        "fields": "file_name,cases.submitter_id,data_format,file_size,md5sum",
        "format": "JSON",
        "size": "10000"  # Adjust the size as needed to fetch more results
    }

    # Make the API request
    response = requests.get(base_url + endpoint, params=params)

    # Parse response
    response = response.json()['data']
    assert(response['pagination']['page'] == 1)  # If this is not one we did not get all results

    all_sizes = np.array([x['file_size'] for x in response['hits']]).sum()
    total_size = np.sum(all_sizes)
    print('{} total size of all {} retrieved files: {}'.format(organ, len(response['hits']), humanize.naturalsize(total_size)))

    # Extract relevant fields for the manifest file
    manifest_data = [{'id': result['id'], 'filename': result['file_name'], 'md5': result['md5sum'], 'size': result['file_size']} for result in response['hits']]

    missing_files = [x for x in file_names if x not in [x['filename'] for x in manifest_data]]
    if len(missing_files) > 0:
        print('\t Missing files: {}'.format(missing_files))

    duplicates = find_duplicates(file_names)
    if len(duplicates) > 0:
        print('\t Duplicates: {}'.format(duplicates))

    #######
    # Note BRCA has an invalid file: 11327473-2921-4916-a111-89d0eda6be8a !!!

    # Specify the file to write the manifest to
    with open(f'{organ}.tsv', 'w', newline='') as manifest_file:
        fieldnames = ['id', 'filename', 'md5', 'size']
        writer = csv.DictWriter(manifest_file, fieldnames=fieldnames, delimiter='\t')

        writer.writeheader()
        for row in manifest_data:
            writer.writerow(row)