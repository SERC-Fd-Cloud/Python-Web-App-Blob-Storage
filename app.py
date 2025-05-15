from flask import Flask, request
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)
blob_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING', '')
if blob_connection_string:
    container_name = 'uploads'
    blob_service = BlobServiceClient.from_connection_string(blob_connection_string)
    container_client = blob_service.get_container_client(container_name)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        container_client.upload_blob(name=f.filename, data=f, overwrite=True)
        return 'File uploaded successfully!'
    
    if blob_connection_string:
        return '''
        <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit">
        </form>
        '''
    else:
        return 'Azure Storage connection string not set. Please set the AZURE_STORAGE_CONNECTION_STRING environment variable.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
