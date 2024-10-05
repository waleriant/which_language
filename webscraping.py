import json

def extract_webscraping_data(my_list):
    code_list = []
    url_list = []
    for element in language_list:
        code_list.append(element["code"])
        url_list.append(element["url"])
    return (code_list, url_list)
	
with open("webscraping.json", "r", encoding = "utf-8") as f:
    my_list = json.loads(f.read())

code_list, url_list = extract_webscraping_data(my_list)