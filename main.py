from fastapi import FastAPI
from utils.functions import create_campaign
app = FastAPI()

@app.get('/')
def response():
    return 'Connected successfully'

@app.post('/data')
def receive_file(file):
    create_campaign(file)
    return 'File has been received.'