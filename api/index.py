from flask import Flask, render_template, request, jsonify
from pinecone import Pinecone, ServerlessSpec, PodSpec
import pinecone
import torch

app = Flask(__name__)

pc = pinecone.Pinecone(api_key="b76cad94-53ae-4524-9156-b3450a92ce4a", environment="gcp-starter")
index = pc.Index("dresses")

# old home route
# @app.route('/')
# def home():
#     return 'Hello, World!'

@app.route('/', methods=['GET', 'POST'])
def grid():
    if request.method == 'POST':
        data = request.get_json()
        vector = data.get('vector')
        if vector:
            vector = list(map(float, vector))
            response = index.query(
                vector=vector,
                top_k=9,
                include_values=True
            )
            # Prepare the data to send back to the client
            items = [{'link': match["id"], 'vector': match["values"]} for match in response["matches"]]
            return jsonify(items)
        else:
            return jsonify({'error': 'No vector provided'}), 400
    else:
        vector = torch.rand(768).tolist()
        response = index.query(
            vector=vector,
            top_k=9,
            include_values=True
        )
        links = [match["id"] for match in response["matches"]]
        vectors = [match["values"] for match in response["matches"]]
        items = list(zip(links, vectors))
        return render_template('grid.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
