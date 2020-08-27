# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
	}

urls = [
"https://www.icc-cricket.com/mens-schedule/list",
"https://www.icc-cricket.com/womens-schedule/list"
]

result_file_name = "Schedule List.csv"
column_names = ["Type", "Match Type", "Name", "Home Team Name", "Away Team Name", "Start Date & Time", "End Date & Time", "Venue", "City", "Crawl URL"]
pd.DataFrame(columns=column_names).to_csv(result_file_name, sep="\t", index=False, encoding="utf-8")

for url in urls:
	request_object = requests.get(url, headers=headers)
	html_content = request_object.text
	print(request_object.status_code, "->", url)
	soup_object = BeautifulSoup(html_content, "lxml")
	type_ = soup_object.select_one('h1.page-title').text
	if("women" in type_.lower()):
		type_ = "Women's"
	else:
		type_ = "Men's"
	for element in soup_object.select('[class="js-matchlist"] > .match-block'):
		data_dict = dict()
		data_dict["Type"] = type_
		data_dict["Crawl URL"] = url
		data_dict["Match Type"] = element.select_one('[class="match-block__type"]').text
		data_dict["Start Date & Time"] = element.select_one('[data-startdate]')["data-startdate"]
		data_dict["End Date & Time"] = element.select_one('[data-enddate]')["data-enddate"]
		if("away" in element.select_one('.match-block__team:first-child')):
			data_dict["Away Team Name"] = element.select_one('.match-block__team:first-child').text
			data_dict["Home Team Name"] = element.select_one('.match-block__team:nth-child(3)').text
		else:
			data_dict["Home Team Name"] = element.select_one('.match-block__team:first-child').text
			data_dict["Away Team Name"] = element.select_one('.match-block__team:nth-child(3)').text
		temp_data = element.select_one('.match-block__summary').text.split("|")
		data_dict["Name"] = temp_data[0].split(",")[-1]
		data_dict["Venue"], data_dict["City"] = temp_data[-1].split(",")
		for key in data_dict.keys():
			data_dict[key] = re.sub(r"\s+", " ", data_dict[key])
			data_dict[key] = data_dict[key].strip()
		pd.DataFrame([data_dict], columns=column_names).to_csv(result_file_name, sep="\t", index=False, header=False, encoding="utf-8", mode="a")