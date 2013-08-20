import csv
import sys

sys.path.append('src')

import urllib

__author__ = 'marknuttallsmith'

import unittest

import FundaScraper
from os import listdir
from os.path import isfile, join


class TestFundaHtmlParse(unittest.TestCase):
    test_dir = "/Users/marknuttallsmith/Projects/FundaScraper/html/"

    def setUp(self):
        self.seq = range(10)

    def read_test_file(self, htmlfile):
        return urllib.urlopen("file://" + self.test_dir + htmlfile)

    def test_html_parse(self):
        onlyfiles = [f for f in listdir(self.test_dir) if isfile(join(self.test_dir, f))]

        all_specs = list()
        for htmlfile in onlyfiles:
            specs = FundaScraper.parse_html(self.read_test_file(htmlfile))
            all_specs.append(specs)

        keys = FundaScraper.get_all_keys(all_specs)

        with open("data/20130815.csv",'wb') as fou:
            dw = csv.DictWriter(fou, dialect=csv.excel, fieldnames=keys)
            dw.writeheader()
            for specs in all_specs:
                dw.writerow({k:v.encode('utf8') for k,v in specs.items()})

            # "appartement-47391471-brederodestraat-31-hs.html"
            # "appartement-48412111-bosboom-toussaintstraat-68-hs.html"
            # "appartement-48522644-bosboom-toussaintstraat-56-iii.html"
            # "appartement-48529378-brederodestraat-30-ii.html"
            # "appartement-48552952-eerste-helmersstraat-154-hs.html"
            # "appartement-48632485-alberdingk-thijmstraat-5-ii.html"
            # "appartement-48675249-jan-pieter-heijestraat-147-i.html"
            # "appartement-48690938-wilhelminastraat-12-iii.html"
            # "appartement-48700504-gerard-brandtstraat-4-d.html"
            # "appartement-48737268-derde-helmersstraat-47-b-hs.html"
            # "appartement-48787516-eerste-helmersstraat-113-ii.html"
            # "appartement-48788997-bosboom-toussaintstraat-56-ii.html"
            # "appartement-48792733-eerste-helmersstraat-149-ii.html"
            # "appartement-48798345-eerste-helmersstraat-235-iii.html"


if __name__ == '__main__':
    unittest.main()
