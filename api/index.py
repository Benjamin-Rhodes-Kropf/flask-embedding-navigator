from flask import Flask, render_template, request, jsonify
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
@app.route('/grid', methods=['GET','POST'])
def grid(): 
    print("request received")
    print(f"request method: {request.method}")

    # Example of retrieving a vector from form data; adjust based on your actual data source
    if request.method == 'POST':
        data = request.get_json()  # Get the JSON data sent with the POST request
        vector = data.get('vector')  # Retrieve the vector from the JSON data
        print(f"vector: {vector}")
        if vector:
            vector = list(map(float, vector))
    else:
     vector = torch.rand(768).tolist()

    # Query the index
    print("Querying the index...")
    response = index.query(
        vector=vector,
        top_k=9,
        include_values=True
    )

    for match in response["matches"]:
        print(match["id"])

    # get all links in response
    links = []
    vectors = []
    for match in response["matches"]:
        links.append(match["id"])
        vectors.append(match["values"])
    
    # Create a list of tuples where each tuple is (link, vector)
    items = list(zip(links, vectors))

    return render_template('grid.html', items=items)  # Pass the links to the template

if __name__ == '__main__':
    app.run(debug=True)
