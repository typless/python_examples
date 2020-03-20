import os

import requests

# ### API KEY ####
# Get api key at https://developers.typless.com -> Settings tab in side navigation
# ### API KEY ####
API_KEY = os.getenv('API_KEY')
DOCUMENT_TYPE_NAME = 'new-simple-invoice'


if API_KEY is None:
    raise Exception('YOU MUST SET API KEY TO ENVIRONMENT!')


# ######## Create document type #########
json_data = {
    "name": DOCUMENT_TYPE_NAME,
    "lang": "eng",
    "fields": [
        {"name": "supplier", "type": "AUTHOR"},
        {"name": "invoice_number", "type": "STRING"},
        {"name": "issue_date", "type": "DATE"},
        {"name": "total_amount", "type": "NUMBER"}
    ]
}
response = requests.post(
    "https://developers.typless.com/api/document-types/",
    json=json_data,
    headers={"Authorization": f"Token {API_KEY}"}
)
print(response.json())

# ######## Extract data first time  ########
file_name = 'invoice.pdf'
with open(file_name, 'rb') as invoice_file:
    file_bytes = invoice_file.read()
    files = {

        "file": (file_name, file_bytes,),
    }
    request_data = {
        "document_type_name": DOCUMENT_TYPE_NAME,
        "customer": 'myself'
    }
    response = requests.post(
        "https://developers.typless.com/api/document-types/extract-data/",
        files=files,
        data=request_data,
        headers={'Authorization': f'Token {API_KEY}'}
    )
    document_object_id = response.json()['object_id']
    print(response.json())

# ####### Train Typless AI #########
request_data = {
    "document_type_name": DOCUMENT_TYPE_NAME,
    "customer": 'myself',
    "learning_fields": [
        '{"name": "supplier", "value": "ScaleGrid"}',
        '{"name": "invoice_number", "value": "20190700006606"}',
        '{"name": "issue_date", "value": "2019-08-13"}',
        '{"name": "total_amount", "value": "15.84"}',
    ],
}
response = requests.post(
    "https://developers.typless.com/api/document-types/learn/",
    data=request_data,
    files={"document_object_id": (None, document_object_id)},
    headers={'Authorization': f'Token {API_KEY}'}
)
print(response.json())

# ######## Extract data second time  ########
file_name = 'invoice.pdf'
with open(file_name, 'rb') as invoice_file:
    file_bytes = invoice_file.read()
    files = {

        "file": (file_name, file_bytes,),
    }
    request_data = {
        "document_type_name": DOCUMENT_TYPE_NAME,
        "customer": 'myself'
    }
    response = requests.post(
        "https://developers.typless.com/api/document-types/extract-data/",
        files=files,
        data=request_data,
        headers={'Authorization': f'Token {API_KEY}'}
    )

    fields = response.json()['extracted_fields']
    supplier = [field for field in fields if field['name'] == 'supplier'][0]['values'][0]['value']
    invoice_number = [field for field in fields if field['name'] == 'invoice_number'][0]['values'][0]['value']
    issue_date = [field for field in fields if field['name'] == 'issue_date'][0]['values'][0]['value']
    total_amount = [field for field in fields if field['name'] == 'total_amount'][0]['values'][0]['value']

    print(f'Supplier: {supplier}')
    print(f'Invoice number: {invoice_number}')
    print(f'Issue date: {issue_date}')
    print(f'Total amount: {total_amount}')
