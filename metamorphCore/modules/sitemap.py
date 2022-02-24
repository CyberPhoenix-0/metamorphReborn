from urllib.parse import urljoin,urlparse
import requests
from sys import argv
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET

class mapping:
    def __init__(self, url=[],base_url=""):
        self.already_visited= []
        self.next_a_visiter =url
        self.final=[]
        self.base_url=base_url

    def get_all_links(self, url, html):
        all_links=[]
        parsed = BeautifulSoup(html, 'html.parser')
        for link in parsed.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/') :
                path = urljoin(url, path)
            all_links.append(path)
        return all_links

    def find_links(self, url):
        html = requests.get(url).text
        for url in self.get_all_links(url, html):
            if url not in self.already_visited and url not in self.next_a_visiter:
                if urlparse(url).netloc=='':
                    urltmp=urljoin(self.base_url,url)
                if urlparse(urltmp).netloc==urlparse(self.base_url).netloc:
                    self.next_a_visiter.append(url)
                    self.final.append(url)

    def main(self):
        while self.next_a_visiter!=[]:
            url = self.next_a_visiter.pop(0)
            print(f'[+] {url}')
            try:
                self.find_links(url)
            except:
                continue
            self.already_visited.append(url)

        return self.final

def generate_xml(url,resultat):
    root = ET.Element("sitemap")
    for i in range(len(resultat)):
        ET.SubElement(root, "url").text = url+resultat[i]
    tree = ET.ElementTree(root)
    filename=urlparse(url).netloc
    filename=filename.replace(".","_")
    filename=filename.replace("-","_")
    tree.write(filename+'.xml')
    print(f'[*] XML generated : {filename}.xml')

if __name__ == '__main__':
    """
    Input : argv[1]=URL a scanner
    Output : Fichier XML "url.xml" avec des "_" a la place des "." et des "-"
    Metamorph SiteMap Module
    V1.0
    Argument : xmlFile
    Desc : SiteMap Scanning tool, xmlFile in argument
    Syntaxe : module sitemap <xmlFile>
    """
    urls=argv[1]
    sitemap=mapping([urls],base_url=urls).main()
    sitemap.append("")
    print(sitemap)
    generate_xml(urls,sitemap)
