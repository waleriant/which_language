import json
import requests
from bs4 import BeautifulSoup
from random import shuffle

def delete_txt_between(my_string_, str1, str2):
    pos1 = my_string_.find(str1)
    pos2 = my_string_.find(str2)
    
    while (pos1 > -1) and (pos2 > pos1):
        my_string_ = my_string_.replace(my_string_[pos1:pos2+1],"")
        pos1 = my_string_.find(str1)
        pos2 = my_string_.find(str2)
    return my_string_

# delete such substrings: "[xxx]", "<xxx>", "(xxx)", "\n"
# add "[...]" in the end
	
def format_text(my_string_):
    words_list = my_string_.split()
    my_string_ = ""
    for word in words_list:
        my_string_ += word
        my_string_ += " "
        if len(my_string_) > 200:
            break
    
    my_string_ = delete_txt_between(my_string_, "[", "]")
    my_string_ = delete_txt_between(my_string_, "<", ">")
    my_string_ = delete_txt_between(my_string_, "(", ")")
    my_string_.replace("\n", "")
    my_string_.replace("    ", " ")
    my_string_.replace("   ", " ")
    my_string_.replace("  ", " ")
        
    return my_string_ + " [...]"
    
# the str_ must include less than 30% of "1-9" and its length must be higher than 100

def test_str(my_string_):
    # counts the number of "1-9"
    nb_bad_char = 0
    for c in my_string_:
        if ord(c) > 49 and ord(c) < 57:
            nb_bad_char +=1 
    return nb_bad_char < 0.3 * len(my_string_) and len(my_string_) > 100
    
# extract the first paragraph of the page

def find_paragraph(url_):
    r = requests.get(url_)
    soup = BeautifulSoup(r.text, "html.parser")
    p = soup.find("p")
    if p is not None:
        my_string = format_text(p.text)
        if test_str(my_string):
            return my_string
    return ""
    
# return the two following variables:
# sentence = "Il-Monasteru ta' Maulbronn huwa eks abbazija tal-Ċisterċensi u eks stat ekkleżjastiku fl-Imperu Ruman Sagru li jinsab f'Maulbronn, Baden-Württemberg. Il-kumpless tal-monasteru, wieħed mill-iżjed ippr [...]"
# options = [{"language": "Maltese", "is_answer": True},
#            {"language": "English", "is_answer": False}, 
#            {"language": "Italian", "is_answer": False}, 
#            {"language": "Greek",   "is_answer": False}]

def extract_options_sentence(nb=4):
    with open("webscraping.json", "r", encoding = "utf-8") as f:
        my_list = json.loads(f.read())
    
    options = []

    # try to extract the answer, the url and the sentence
    sentence = ""
    shuffle(my_list)
    
    while sentence == "":
        # extract the answer ("Maltese")
        language = my_list[0]["language"]
    
        # extract the related url and sentence
        url = my_list[0]["url"]
        sentence = find_paragraph(url)

        # add the answer to options if a related sentence was found
        if sentence != "":
            options.append({"language": language, "is_answer": True})
        my_list.pop(0)
            

    # extract the (nb-1) other languages ("English", "Italian", "Greek")
    count = 1
    while count < nb:
        language = my_list[0]["language"] 
        options.append({"language": language, "is_answer": False})

        my_list.pop(0)
        count += 1

    return sentence, options