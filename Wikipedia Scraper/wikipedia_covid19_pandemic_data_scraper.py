# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
	}

result_file_name = "COVID-19_pandemic_data.csv"
column_names = ["Location", "Cases", "Deaths", "Recoveries", "Detail Page URL", "Location Flag URL"]
pd.DataFrame(columns=column_names).to_csv(result_file_name, sep="\t", index=False, encoding="utf-8")

url = "https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data"
request_object = requests.get(url, headers=headers)
html_content = request_object.text
print(request_object.status_code, "->", url)
soup_object = BeautifulSoup(html_content, "lxml")
for element in soup_object.select('[id="covid19-container"] table tbody tr'):
    if(element.select_one('th > a')):
        data_dict = dict()
        data_dict["Location"] = element.select_one('th > a').text
        data_dict["Cases"] = element.select_one('td:nth-child(3)').text
        data_dict["Deaths"] = element.select_one('td:nth-child(4)').text
        data_dict["Recoveries"] = element.select_one('td:nth-child(5)').text
        data_dict["Detail Page URL"] = "https://en.wikipedia.org" + element.select_one('th > a')["href"]
        data_dict["Location Flag URL"] = "https:" + element.select_one('th img')["src"]
        for key in data_dict.keys():
            data_dict[key] = re.sub(r"\s+", " ", data_dict[key])
            data_dict[key] = data_dict[key].strip()
        pd.DataFrame([data_dict], columns=column_names).to_csv(result_file_name, sep="\t", index=False, header=False, encoding="utf-8", mode="a")
