import requests
from sys import argv
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
from urllib.parse import urljoin

#input :Fichier XML de sortie du sitemap


def get_all_forms(url):
    req=requests.get(url).content
    html = BeautifulSoup(req, "html.parser")
    return html.find_all("form")

def get_form_details(form):
    form_details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    input_list = []
    for input_box in form.find_all("input"):
        input_type = input_box.attrs.get("type", "text")
        input_name = input_box.attrs.get("name")
        input_list.append({"type": input_type, "name": input_name})
    form_details["action"] = action
    form_details["method"] = method
    form_details["inputs"] = input_list
    return form_details

def submit_form(form_details, url, payload):
    url_complete = urljoin(url, form_details["action"])
    input_list = form_details["inputs"]
    data = {}
    for input in input_list:
        if input["type"]=="text" or input["type"]=="search":
            input["value"]=payload
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value
    if form_details["method"] == "post":
        return requests.post(url_complete, data=data)
    else:
        return requests.get(url_complete, params=data)

def scan(url):
    forms = get_all_forms(url)
    vuln=[]
    payload ='"><sCRipt>alert("testing")</scrIpT>--'
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, payload).content.decode()
        if payload in content:
            for i in range(len(form_details["inputs"])-1):
                if payload in form_details["inputs"][i]["value"]:
                    vuln.append(form_details["inputs"][i]["name"])
    return vuln

def generate_xml(resultats,payload,vuln_compteur):
    root = ET.Element("root")
    doc=ET.SubElement(root,"XSS")
    for i in resultats.items():
        for j in i[1]:
            ET.SubElement(doc, "XSS",name=j).text = i[0]
    ET.SubElement(root,"Payload").text=payload
    ET.SubElement(root,"Number").text=str(vuln_compteur)
    tree = ET.ElementTree(root)
    filename=url.split('.xml')[0]
    tree.write("XSS_"+filename+".xml")
    print('[*] XML Generated : XSS_'+filename+".xml")

def load_xml(file):
    loaded=[]
    root = ET.parse(file).getroot()
    for i in root.findall('url'):
        loaded.append(i.text)
    return loaded

if __name__=="__main__":
    """
    Input : En argv[1] : Le fichier xml généré par sitemap.py
    Output : Fichier xml "XSS_url.xml" avec des "_" a la place des "." et des "-"
    Metamorph XSS Module
    V1.0
    Argument : xmlFile
    Desc : XSS Scanning tool, xmlFile in argument
    Syntaxe : module xss <xmlFile>


    """
    load_xml(argv[1])
    url=argv[1]
    vuln_compteur=0
    vulnerable_url={}
    for i in load_xml(argv[1]):
        scan_result=scan(i)
        vuln_compteur+=len(scan_result)
        if scan_result!=[]:
            vulnerable_url[i]=scan_result
    print(f'[*] {vuln_compteur} XSS found')
    generate_xml(vulnerable_url,'"><script>alert("testing")</script>--',vuln_compteur)
            




