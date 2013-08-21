# coding=utf-8
import csv
from datetime import date
import re
import sys
import logging
import urllib
import mechanize
import urlparse

import Stadsdeel
from bs4 import BeautifulSoup
import time

MAIN_URL = 'http://www.funda.nl/koop/amsterdam/jordaan'
test_dir = "/Users/marknuttallsmith/Projects/FundaScraper/data/"

# To make sure you're seeing all debug output:
logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


def scrape_links(br, ):
    print br.geturl()
    links = list()
    for link in br.links(url_regex='/koop/amsterdam/'):
        if link.text == '[IMG]':
            links.append(urlparse.urljoin(link.base_url, link.url + "kenmerken"))
    return links


def get_html(link):
    response = urllib.urlopen(link)
    if "404" not in response.url and "500" not in response.url:
        return response.read()
    print "... failed"
    return None


def parse_html(html):
    soup = BeautifulSoup(html)
    specs = {}
    header = soup.find_all("div", class_="prop-hdr")[0]
    specs["Address"] = header.h1.get_text()
    specs["Postcode"] = header.p.get_text().replace("    Tophuis", "")
    specs["Areacode"] = specs["Postcode"].split(" ")[0]
    nav = soup.find_all("p", class_="path-nav")[0]
    specs["Area"] = nav.get_text(strip=True).split(">")[-1]

    specs["Stadsdeel"] = Stadsdeel.stadsdeel[specs["Area"]]
    for table in soup.find_all("table", class_="specs-cats"):
        for tr in table.find_all('tr'):
            if tr.th is not None and tr.td is not None and tr.td.get_text(strip=True):
                key = tr.th.get_text(strip=True)

                text = tr.td.get_text("|", strip=True)

                text = text.replace(u"\u00B2", u'')  # replace squares
                text = text.replace(u"\u00B3", u'')  # replace cubes
                text = re.sub("\W+m$", "", text)  # replace metres
                text = text.replace(u"\u20AC", u'').strip()  # replace euros

                if key == 'Vraagprijs':
                    if "v.o.n." in text:
                        text = text.replace(" v.o.n.", "")
                        specs["Cost"] = "v.o.n."
                    elif "k.k." in text:
                        text = text.replace(" k.k.", "")
                        specs["Cost"] = "k.k."
                    text = text.replace(".", "")

                specs[key] = text
    return specs


def get_all_keys(all_specs):
    keys = set()
    for specs in all_specs:
        keys.update(specs.keys())
    return sorted(list(keys))


def write_test_file(link, html):
    with open("data/" + link.split('/')[-2] + ".html", "w") as text_file:
        text_file.write(html.read())
        # parse_html(html)


def main():
    br = mechanize.Browser()
    # time.sleep(1)

    br.open(MAIN_URL)
    # while True:
    #     try:
    #         break
    #     except urllib2.URLError as e:
    #         if not e.contains('54'):
    #             raise

    links = list()
    volgende = True
    while volgende is True:
        try:
            links.extend(scrape_links(br))
            br.follow_link(text_regex="^Volgende", nr=0)
            # time.sleep(1)
        except mechanize.LinkNotFoundError:
            volgende = False

    datestr = date.today().isoformat()

    with open("data/" + datestr + "-links.txt", 'wb') as fou:
        fou.write("\n".join(links))

    all_specs = list()
    for link in links:
        time.sleep(1)
        print link
        html = get_html(link)
        if html is not None:
            specs = parse_html(html)
            specs["Link"] = '=HYPERLINK("' + link + '")'
            all_specs.append(specs)

    keys = get_all_keys(all_specs)
    suffix = MAIN_URL.split('/')[-1]

    f = open("data/" + datestr + '-' + suffix + ".csv", 'wb')

    # w = UnicodeDictWriter(f, sorted(keys))
    # w.writeheader()
    # w.writerows(all_specs)
    # f.close()

    with open("data/" + datestr + '-' + suffix + ".csv", 'wb') as fou:
        fou.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        dw = csv.DictWriter(fou, fieldnames=keys)
        dw.writeheader()
        for specs in all_specs:
            dw.writerow({k: v.encode('utf8') for k, v in specs.items()})
            # dw.writerow(specs)


if __name__ == "__main__":
    main()