from flask import Flask, request
import json
from elastic_index import Index
from lxml import etree
import unicodedata



app = Flask(__name__)

config = {
    "url" : "localhost",
    "port" : "9200",
    "doc_type" : "manuscript"
}

index = Index(config)

def grab_value(path, root, ns):
    content = root.findall(path, ns)
    if content and content[0].text is not None:
        return unicodedata.normalize("NFKD", content[0].text).strip()
    else:
        return ""

def grab_list(name, path, root, ns):
    ret_arr = []
    content = root.findall(path, ns)
    for item in content:
        buffer = {name : unicodedata.normalize("NFKD", item.text).strip()}
        if buffer not in ret_arr:
            ret_arr.append(buffer)
    return ret_arr


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

@app.route("/detail", methods=['GET'])
def get_detail():
    print('test')
    rec = request.args.get("rec")
    file = etree.parse("/data/records/"+rec)
    root = file.getroot()
    ns = {"cmd": "http://www.clarin.eu/cmd/","xml": "http://www.w3.org/XML/1998/namespace"}
    ttl = grab_value("./cmd:Components/cmd:Interview/cmd:Titel[@xml:lang='nl']", root, ns)
    titel = grab_value("./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Naam/cmd:titel", root, ns)
    voornaam = grab_value("./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Naam/cmd:voornaam", root, ns)
    achternaam = grab_value("./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Naam/cmd:achternaam", root, ns)
    tussenvoegsel = grab_value("./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Naam/cmd:tussenvoegsel", root, ns)

    loc = grab_list('locatie', "./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Carriere/cmd:Stationering/cmd:Locatie", root, ns)
    opnamedata = grab_list('opnamedatum', "./cmd:Components/cmd:Interview/cmd:Opname/cmd:Opnamedatum", root, ns)
    # print('loc' ,loc)
    retStruc = {"_id": rec,"titel": ttl, "locaties": loc, "naam_titel": titel, "naam_voornaam": voornaam, "naam_achternaam": achternaam, "naam_tussenvoegsel": tussenvoegsel, "opnamedata": opnamedata}
    return json.dumps(retStruc)



#Start main program

if __name__ == '__main__':
    app.run()

