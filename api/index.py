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
    print(f"request form: {request.form}")
    print(f"request vector: {request.form.get('vector')}")
    print(f"request args: {request.args}")

    # Example of retrieving a vector from form data; adjust based on your actual data source
    if request.method == 'POST':
        # Example of retrieving a vector from form data; adjust based on your actual data source
        input_vector = request.form.get('vector')
        if input_vector:
            # Assuming input_vector is a string of comma-separated numbers
            vector = list(map(float, input_vector.split(',')))
        else:
            vector = torch.rand(768).tolist()
    else:
        # For GET requests or if no vector is provided
        vector = torch.rand(768).tolist()

    response = index.query(
        vector=vector,
        top_k=9,
        include_values=True
    )

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
