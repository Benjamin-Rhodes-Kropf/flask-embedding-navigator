from flask import Flask, render_template, request, jsonify
from pinecone import Pinecone
import pinecone
import random
from algoliasearch.search_client import SearchClient
# !pip install --upgrade 'algoliasearch>=3.0,<4.0'
# pip install algoliasearch

app = Flask(__name__)

pc = pinecone.Pinecone(api_key="b76cad94-53ae-4524-9156-b3450a92ce4a", environment="gcp-starter")
index = pc.Index("dresses")

def nineNearestNeighbors(vector):
    response = index.query(
                vector=vector,
                top_k=9,
                include_values=True
            )
    things = [{'link': match["id"], 'vector': match["values"]} for match in response["matches"]]
    items = things[1:5] + [things[0]] + things[5:]
    return jsonify(items)


@app.route('/search', methods=['POST'])
def algoliaSearch():
    client = SearchClient.create('BV318UGLE0', '5079b75c76a6ce41a2da8e354d39e3ec')
    algoliaIndex = client.init_index('productData')
    data = request.get_json()
    searchTerm = data.get('query')
    initial = algoliaIndex.search(searchTerm)
    this = None
    try:
        this=initial['hits'][:9]
        things = [{'link': dress["image"], 'vector': index.query(id=dress["image"], top_k=5, include_values=True)['matches'][0]['values']} for dress in this]
        items = things[1:5] + [things[0]] + things[5:]
    except:
        this=algoliaIndex.search("")['hits'][:9]
        things = [{'link': dress["image"], 'vector': index.query(id=dress["image"], top_k=5, include_values=True)['matches'][0]['values']} for dress in this]
        items = things[1:5] + [things[0]] + things[5:]
    if(len(items)<9):
            return nineNearestNeighbors(items[0]["vector"])

    return items

@app.route('/', methods=['GET', 'POST'])
def grid():
    if request.method == 'POST':
        data = request.get_json()
        vector = data.get('vector')
        if vector:
            vector = list(map(float, vector))
            return nineNearestNeighbors(vector)
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
