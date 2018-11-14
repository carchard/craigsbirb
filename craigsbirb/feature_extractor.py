from bs4 import BeautifulSoup as bs
import requests
import os
import json
import numpy as np
import pandas as pd
import tqdm
from constants import KEYWORDS
from constants import GETTER_OUTPUT_FILE
from constants import EXTRACTOR_OUTPUT_FILE

class Feature_Extractor():
    def __init__(self):
        self.getter_dict = {}
        print("You made a feature extractor!")

    def process_new_posts(self):
        if os.path.isfile(GETTER_OUTPUT_FILE):
            with open(GETTER_OUTPUT_FILE, 'r') as f:
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

        # preprocessing
        html_data = requests.get(getter_dict['link'])
        if html_data.status_code == 200:
            html_data = html_data.text
        else:
            html_data = ''
        html_data = bs(html_data, 'html.parser')
        user_text = html_data.find('section',
                                   {'id': 'postingbody'}).getText()
        getter_dict['price'] = getter_dict['price'].replace('$', '')
        print("{}: ${}".format(getter_dict['title'],
                               getter_dict['price']))
        try:
            features_dict['price'] = float(getter_dict['price'])
        except ValueError:
            features_dict['price'] = np.NaN

        features_dict['title'] = getter_dict['title']
        features_dict['num_keywords_in_title'] = 0
        features_dict['num_keywords_in_text'] = 0

        for word in features_dict['title'].split(' '):
            if word.lower() in KEYWORDS:
                features_dict['num_keywords_in_title'] += 1

        for keyword in KEYWORDS:
            if keyword in user_text.lower().split(' '):
                features_dict['num_keywords_in_text'] += 1
                features_dict[keyword] = 1
            else:
                features_dict[keyword] = 0

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
    fe.process_new_posts()
