import json
import unicodedata

from flask import Flask, request
from lxml import etree

from elastic_index import Index
from os import path
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

@app.route("/shoutout", methods=["GET"])
@app.route("/test", methods=["GET"])
def shoutout():
    name = request.args.get('name')
    return json.dumps(name); 
    # http://localhost:5050/test?name=maarten test met
    # http://localhost:5050/shoutout?name=hoi


@app.route("/scream/<name>/")
def scream(name):
    scream = "GRRRRR " + name.upper() + '!!!'
    return json.dumps(scream)


# testen met http://localhost:5050/detail?rec=19.cmdi # tijd mee verspeelt... ik dacht dat het 19 was

@app.route("/detail", methods=['GET'])
def get_detail():
    print('test')
    # exit(3)
    rec = request.args.get("rec")
    filename = "/data/records/" + rec
    if not path.exists(filename):
        return json.dumps('file does not exist')
        # todo moet de structuur meegeven 

    file = etree.parse(filename)
    # if not path.exists("guru99.txt"):
    #     return json.dumps('file does not exist')
    root = file.getroot()
    print(root)
    ns = {"cmd": "http://www.clarin.eu/cmd/","xml": "http://www.w3.org/XML/1998/namespace"}
    ttl = grab_value("./cmd:Components/cmd:Interview/cmd:Titel[@xml:lang='nl']", root, ns)
    ttl_en = grab_value("./cmd:Components/cmd:Interview/cmd:Titel[@xml:lang='en']", root, ns)
    titel = grab_value("./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Naam/cmd:titel", root, ns)
    voornaam = grab_value("./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Naam/cmd:voornaam", root, ns)
    achternaam = grab_value("./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Naam/cmd:achternaam", root, ns)
    tussenvoegsel = grab_value("./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Naam/cmd:tussenvoegsel", root, ns)
    loc = grab_list('locatie', "./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Carriere/cmd:Stationering/cmd:Locatie", root, ns)
    # statio_post = grab_list('locatie', "./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Carriere/cmd:Stationering/cmd:Post", root, ns)

    opnamedata = grab_list('opnamedatum', "./cmd:Components/cmd:Interview/cmd:Opname/cmd:Opnamedatum", root, ns)
    
    stationeringen = root.findall("./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Carriere/cmd:Stationering", ns) # zonder slash pakt hij de xml elementen met slash alles wat eronder hangt
    # stationeringen = grab_list("./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Carriere/cmd:Stationering", ns) # zonder slash pakt hij de xml elementen met slash alles wat eronder hangt
    interviewsessies = root.findall("./cmd:Components/cmd:Interview/cmd:Opname", ns)
    # print(type(stationeringen)
    print(interviewsessies)

    # loop through a list

    statio_list = []
    for item in stationeringen:
        # print('item:', item)
        statio = {}
        for el in item:    
            # iek = grab_value("./cmd:departement", item, ns)
            # iek = grab_value("./cmd:departement/cmd:Organisatie", item, ns)
            # print(el, type(el),  "-",el.tag, "-" ,el.text)           
            tag = etree.QName(el.tag).localname           
            # print('tag: ', tag, 'localname: ', tag.localname)
            if tag == 'Periode':
                statio[tag] = {'Van': '', 'Tot': ''}    
                van = grab_value("./cmd:Van", el ,ns)
                tot = grab_value("./cmd:Tot", el ,ns)
                statio[tag]['Van'] = van
                statio[tag]['Tot'] = tot         
            else:
                statio[tag] = el.text

        statio_list.append(statio)

    sessie_list = []
    for item in interviewsessies:
    # print('item:', item)
        sessie = {}
        for el in item:    
            tag = etree.QName(el.tag).localname           
            # print('tag: ', tag, 'localname: ', tag.localname)
            sectielist = []
            if tag == 'Inhoud':
                # sectie = grab_list("./cmd:Sectie", el, ns)
                secties = el.findall("./cmd:Sectie", ns)
                for it in secties:
                    sectie = {}
                    onderwerp = grab_value("./cmd:Onderwerp", it, ns)
                    tijdstip = grab_value("./cmd:Tijdstip", it, ns)
                    periode = grab_value("./cmd:Periode", it, ns)
                    sectie['onderwerp'] = onderwerp
                    sectie['tijdstip'] = tijdstip
                    sectie['periode'] = periode # TODO uitwerken
                    sectielist.append(sectie)
                  
                sessie[tag] = sectielist
            else:
                sessie[tag] = el.text
        sessie_list.append(sessie)

    # print(statio_list, sep="\n")

    # print('\n'.join(map(str, statio_list))) 

    # buffer = {name : unicodedata.normalize("NFKD", item.text).strip()}
    # if buffer not in ret_arr:
        # ret_arr.append(buffer)


    # print(opnamedata[0])
  
    # stationeringen = grab_list('stationering', "./cmd:Components/cmd:Interview/cmd:Geinterviewde/cmd:Carriere/cmd:Stationering", root, ns)


    # print('loc' ,loc)
    retStruc = {
                "_id": rec,
                "titel": ttl, 
                "titel_en": ttl_en,    
                "locaties": loc,
                "naam_titel": titel,
                "naam_voornaam": voornaam,
                "naam_achternaam": achternaam,
                "naam_tussenvoegsel": tussenvoegsel, 
                "opnamedata": opnamedata,
                "stationeringen" : statio_list,
                "interviewsessies" : sessie_list
    }

    return json.dumps(retStruc)



#Start main program

if __name__ == '__main__':
    app.run()

