from flask import Flask, request
import json
from elastic_index import Index


app = Flask(__name__)

config = {
    "url" : "localhost",
    "port" : "9200",
    "doc_type" : "manuscript"
}

index = Index(config)


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Content-type'] = 'application/json'
    return response

@app.route("/")
def hello_world():
    retStruc = {"app": "Diplo service", "version": "0.1"}
    return json.dumps(retStruc)

@app.route("/facet", methods=['GET'])
def get_facet():
    facet = request.args.get("name")
    amount = request.args.get("amount")
    ret_struc = index.get_facet(facet + ".keyword", amount)
    return json.dumps(ret_struc)

# @app.route("/nested_facet", methods=['GET'])
# def get_nested_facet():
#     facet = request.args.get("name")
#     amount = request.args.get("amount")
#     path = request.args.get("path")
#     ret_struc = index.get_nested_facet(path, facet + ".keyword", amount)
#     return json.dumps(ret_struc)

@app.route("/filter-facet", methods=['GET'])
def get_filter_facet():
    facet = request.args.get("name")
    amount = request.args.get("amount")
    facet_filter = request.args.get("filter")
    ret_struc = index.get_filter_facet(facet + ".keyword", amount, facet_filter)
    return json.dumps(ret_struc)

@app.route("/browse", methods=['POST'])
def browse():
    struc = request.get_json()
    ret_struc = index.browse(struc["page"], struc["page_length"], struc["sortorder"] + ".keyword", struc["searchvalues"])
    return json.dumps(ret_struc)

@app.route("/item", methods=['GET'])
def manuscript():
    id = request.args.get('id')
    manuscript = index.item(id)
    return json.dumps(manuscript)

@app.route("/get_collection", methods=["POST"])
def get_collection():
    data = request.get_json()
    collection_items = index.get_collection_items(data["collection"])
    return json.dumps(collection_items);





#Start main program

if __name__ == '__main__':
    app.run()

