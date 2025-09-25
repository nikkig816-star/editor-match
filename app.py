from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/search-scholars", methods=["GET"])
def search_scholars():
    query = request.args.get("query")
    limit = request.args.get("limit", 5)

    if not query:
        return jsonify({"error": "Missing query"}), 400

    params = {
        "query": query,
        "limit": limit,
        "fields": "name,affiliations,hIndex,citationCount,paperCount,url"
    }

    r = requests.get("https://api.semanticscholar.org/graph/v1/author/search", params=params)
    results = r.json().get("data", [])
    out = []

    for item in results:
        out.append({
            "name": item.get("name"),
            "affiliations": item.get("affiliations"),
            "hIndex": item.get("hIndex"),
            "citationCount": item.get("citationCount"),
            "paperCount": item.get("paperCount"),
            "profileUrl": item.get("url")
        })

    return jsonify(out)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
