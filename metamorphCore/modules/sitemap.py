import sys
from urllib.parse import urljoin, urlparse
import requests
from sys import argv
import termcolor
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET




alreadyVisited = []
nextToVisit = None
baseUrl = None
final = []


def __init__(self, url=None, base_url=""):
    if url is None:
        url = []
    nextToVisit = url
    baseUrl = base_url

def get_all_links(url, html):
    all_links = []
    parsed = BeautifulSoup(html, 'html.parser')
    for link in parsed.find_all('a'):
        path = link.get('href')
        if path and path.startswith('/'):
            path = urljoin(url, path)
        all_links.append(path)
    return all_links

def find_links(url):
    html = requests.get(url).text
    linksInPage = get_all_links(url, html)
    for url in linksInPage:
        if url not in alreadyVisited and url not in nextToVisit:
            if urlparse(url).netloc == '':
                urltmp = urljoin(baseUrl, url)
                if urlparse(urltmp).netloc == urlparse(baseUrl).netloc:
                    nextToVisit.append(url)
                    final.append(url)

def main():
    while nextToVisit:
        url = nextToVisit.pop(0)
        print(f'[+] {url}')
        find_links(url)
        try:
            find_links(url)
        except requests.exceptions.MissingSchema as missingSchemaerror:
            print(missingSchemaerror)
            continue
        except Exception as err:
            print(termcolor.colored("[X]Error : An error occured in sitemap module !\n" + str(err)))
        alreadyVisited.append(url)
    return final


def generate_xml(url, resultat):
    root = ET.Element("sitemap")
    for i in range(len(resultat)):
        ET.SubElement(root, "url").text = url + resultat[i]
    tree = ET.ElementTree(root)
    filename = urlparse(url).netloc
    filename = filename.replace(".", "_")
    filename = filename.replace("-", "_")
    tree.write(filename + '.xml')
    print(f'[*] XML generated : {filename}.xml')


if __name__ == '__main__':
    """
    Input : argv[1]=URL a scanner; mode de scan, 0: scan surface, 1: scan profondeur
    Output : Fichier XML "url.xml" avec des "_" a la place des "." et des "-"
    Metamorph SiteMap Module
    V2.0
    Argument : url, mode
    Desc : SiteMap Scanning tool, xmlFile in argument
    Syntaxe : module sitemap <url>
    """
    try:
        urls = argv[1]
        try:
            mode = int(argv[2])
            if mode == 1:
                nextToVisit = [urls]
                baseUrl = urls
                sitemap = main()
                print(sitemap)
                generate_xml(urls, sitemap)
        except IndexError:
            print(termcolor.colored("[X]Error : Missing mode argument ! Must be a value between 0 and 1.", 'red'))
        res = None
    except KeyboardInterrupt:
        print(termcolor.colored("[X]Error : Scan stopped while running !", 'red'))
        sys.exit(0)
    except Exception as error:
        print(error)
        sys.exit(-1)
