from sys import argv 
from os import popen 
import xml.etree.cElementTree as ET
from urllib.parse import urlparse

def generate_xml(output,url):
    output_list=output.split('\n')
    output_list=[i for i in output_list if i!='' and i[0]!='%' and i[-1]!="-"]
    root = ET.Element("whois")
    for i in output_list:
        splitted=i.split(':')
        ET.SubElement(root, splitted[0]).text = splitted[1]
    tree = ET.ElementTree(root)
    url=url.replace(".","_")
    url=url.replace("-","_")
    tree.write(f'whois_{url}.xml')
    print(f'[*] XML generated whois_{url}.xml')

def main():
    url=urlparse(argv[1]).netloc
    url=url.split('www.')
    if len(url)!=1:
        url=url[1]
    else:
        url=url[0]
    output=popen(f"whois {url} | tr -d ' '").read()
    generate_xml(output,url)
if __name__=="__main__":
    """
    Input : url en argv[1] de la forme http(s)://(www.)site.com => ()=optionnel
    Output : fichier xml "whois_url.xml" avec des "_" a la place des "." et des "-"
    """
    main()

