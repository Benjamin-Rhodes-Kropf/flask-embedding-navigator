from flask import Flask, render_template, request, jsonify
from pinecone import Pinecone
import pinecone
import random

app = Flask(__name__)

pc = pinecone.Pinecone(api_key="b76cad94-53ae-4524-9156-b3450a92ce4a", environment="gcp-starter")
index = pc.Index("dresses")

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
            items = [{'link': match["id"], 'vector': match["values"]} for match in response["matches"]]
            return jsonify(items)
        else:
            return jsonify({'error': 'No vector provided'}), 400
    else:
        vector = [random.random() for _ in range(768)]  # Modified line here
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
