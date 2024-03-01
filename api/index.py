from flask import Flask, render_template
from pinecone import Pinecone, ServerlessSpec, PodSpec
import pinecone
import torch

app = Flask(__name__)

pc = pinecone.Pinecone(api_key="b76cad94-53ae-4524-9156-b3450a92ce4a", environment="gcp-starter")
index = pc.Index("dresses")

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

# New route for the grid
@app.route('/grid')
def grid():
    return render_template('grid.html')  # This will render the grid.html template

if __name__ == '__main__':
    app.run(debug=True)
