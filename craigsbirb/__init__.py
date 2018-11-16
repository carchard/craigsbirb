import datetime
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from post_getter import Post_Getter
from feature_extractor import Feature_Extractor
from post_classifier import Post_Classifier
from email_notifier import Email_Notifier
import pandas as pd
from constants import CL_DATE_FORMAT
from constants import GETTER_OUTPUT_FILE
import tqdm
import os

def run_service(update_interval_min=60):
    date_str = '2018-11-13 16:51'
    dt_object = datetime.datetime.strptime(date_str, CL_DATE_FORMAT)
    clf = Post_Classifier(use_previous=False)
    cities = ['columbia', 'toronto']#, 'harrisonburg', 'richmond']
    if os.path.isfile(GETTER_OUTPUT_FILE):
        os.remove(GETTER_OUTPUT_FILE)
    for city in cities:
        print("getting links from {}".format(city))
        pg = Post_Getter(start_time=dt_object,
                         city=city, save_type='a')
        pg.get_urls()

    fe = Feature_Extractor()
    df = fe.process_posts()

    posts_list = clf.predict_good_links(df)

    dr = webdriver.Chrome()
    dr.get('http://boston.craigslist.com/')

    for url in tqdm.tqdm(posts_list):
        # open tab
        dr.find_element_by_tag_name('body').send_keys(
            Keys.COMMAND + 't')
        # You can use (Keys.CONTROL + 't') on other OSs

        # Load a page
        dr.get(url)

        # Make the assessment...
        usr_input = input('Press any key to advance to next post')

        # close the tab
        # (Keys.CONTROL + 'w') on other OSs.
        dr.find_element_by_tag_name('body').send_keys(
            Keys.COMMAND + 'w')


if __name__ == "__main__":
    run_service()
