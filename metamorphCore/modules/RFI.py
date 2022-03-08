from urllib.parse import urlparse
from requests import get
from sys import argv
import xml.etree.cElementTree as ET

def check_rfi(url):
    if "=" in url:
        fichier="https://www.google.com"
        url=url.replace("=",f'={fichier}#')
        req=get(url)
        if req.status_code==200 and "google" in req.text:
            return True
    return False
def load_xml(file):
    loaded=[]
    root = ET.parse(file).getroot()
    for i in root.findall('url'):
        loaded.append(i.text)
    return loaded
def generate_xml(vuln_rfi,no_rfi):
    root = ET.Element("root")
    for i in vuln_rfi:
        if no_rfi==False:
            ET.SubElement(root, "RFI").text = i
        else:
            ET.SubElement(root, "RFI").text = "No RFI"
            break
    ET.SubElement(root,"Payload").text="https://www.epita.fr/"
    ET.SubElement(root,"Number").text=str(len(vuln_rfi))
    tree = ET.ElementTree(root)
    print(vuln_rfi)
    filename=urlparse(vuln_rfi[0]).netloc.replace(".","_")
    filename=filename.replace("-","_")
    tree.write("RFI_"+filename+".xml")
    print('[*] XML Generated : rfi_'+filename+".xml")


if __name__=='__main__':
    """
    Metamorph LFI Vulnerabilities Detection

    Argument : argv[1] : Le fichier xml généré par sitemap.py
    Desc : Find RFI vulnerabilities in urls in URL.xml 
    Syntaxe : module rfi <url.xml>
    Info: XML generated will contains all urls vulnerable in <url>, payloads used in <payload> and the number of RFI found in <Number>
    """
    all_url=load_xml(argv[1])
    vuln_rfi=[]
    for i in all_url:
        if check_rfi(i)==True:
            vuln_rfi.append(i)
    print(f'[+] {len(vuln_rfi)} RFI found ')
    no_rfi=False
    if len(vuln_rfi)==0:
        vuln_rfi.append(all_url[0])
        no_rfi=True
    generate_xml(vuln_rfi,no_rfi)
       