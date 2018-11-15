from bs4 import BeautifulSoup as bs
import requests
import os
import json
import numpy as np
import pandas as pd
import tqdm
from constants import KEYWORDS
from constants import BADWORDS
from constants import GETTER_OUTPUT_FILE
from constants import EXTRACTOR_OUTPUT_FILE

class Feature_Extractor():
    def __init__(self):
        self.getter_dict = {}
        print("You made a feature extractor!")

    def process_posts(self, json_fname=GETTER_OUTPUT_FILE):
        if os.path.isfile(json_fname):
            with open(json_fname, 'r') as f:
                getter_list = json.load(f)

        self.frame_proto = []
        for getter_dict in tqdm.tqdm(getter_list):
            self.frame_proto.append(self.process_features(getter_dict))

        df = pd.DataFrame(self.frame_proto)
        return df

    def process_features(self, getter_dict):
        """
        Parses the key features from the provided craigslist html string
        :param getter_list:
        :return: pandas dataframe
        """
        features_dict = {}
        lowercases = 'abcdefghijklmnopqrstuvwxyz'
        title_letters = [l for l in list(getter_dict['title']) if
                                         l.lower() in lowercases]
        title_uppers = [l for l in title_letters if l.isupper()]
        # preprocessing
        html_data = requests.get(getter_dict['link'])
        if html_data.status_code == 200:
            html_data = html_data.text
        else:
            html_data = ''
        html_data = bs(html_data, 'html.parser')
        user_text = html_data.find('section',
                                   {'id': 'postingbody'}).getText()
        text_letters = [l for l in list(user_text) if
                                         l.lower() in lowercases]
        text_uppers = [l for l in text_letters if l.isupper()]
        getter_dict['price'] = getter_dict['price'].replace('$', '')
        try:
            features_dict['price'] = float(getter_dict['price'])
        except ValueError:
            features_dict['price'] = 9999

        if 'score' in getter_dict:
            features_dict['score'] = getter_dict['score']

        features_dict['title'] = getter_dict['title']
        features_dict['num_keywords_in_title'] = 0
        features_dict['num_keywords_in_text'] = 0
        features_dict['num_badwords_in_text'] = 0
        features_dict['num_badwords_in_title'] = 0
        features_dict['text_fraction_caps'] = (len(text_uppers)
                                              /float(len(text_letters)))
        features_dict['title_fraction_caps'] = (len(title_uppers)
                                              /float(len(title_letters)))

        for word in features_dict['title'].split(' '):
            if word.lower() in KEYWORDS:
                features_dict['num_keywords_in_title'] += 1
            if word.lower() in BADWORDS:
                features_dict['num_badwords_in_title'] += 1

        for keyword in KEYWORDS:
            if keyword in user_text.lower().split(' '):
                features_dict['num_keywords_in_text'] += 1
                #features_dict[keyword] = 1
            #else:
                #features_dict[keyword] = 0

        for keyword in BADWORDS:
            if keyword in user_text.lower().split(' '):
                features_dict['num_badwords_in_text'] += 1

        features_dict['num_images'] = len(html_data.find_all('img'))
        return features_dict


if __name__ == "__main__":
    link = "https://boston.craigslist.org/gbs/pho/d/sony-a7-iii-full-frame/6748437097.html"
    data = requests.get(link)
    status = data.status_code
    print("Status: {}".format(data.status_code))
    if status == 200:
        html_str = data.text
    else:
        print("bad response status")
        html_str = ''

    fe = Feature_Extractor()
    df = fe.process_posts()
