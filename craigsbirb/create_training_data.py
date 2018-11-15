import json
import os
import tqdm
import datetime
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from post_getter import Post_Getter
from constants import CL_DATE_FORMAT

file_dir = os.path.dirname(os.path.realpath(__file__))
training_dir = os.path.join(file_dir, 'training_data')
if not os.path.isdir(training_dir):
    os.mkdir(training_dir)

training_set = os.path.join(training_dir, 'training.json')
new_post_set = os.path.join(training_dir, 'new_posts.json')


if __name__ == "__main__":
    if os.path.isfile(new_post_set):
        os.remove(new_post_set)
    dr = webdriver.Chrome()
    dr.get('http://boston.craigslist.com/')
    date_str = '2018-11-10 16:51'
    dt_object = datetime.datetime.strptime(date_str, CL_DATE_FORMAT)

    cities = ['boston', 'philadelphia', 'longisland', 'newyork',
              'newhaven', 'hartford']
    for city in cities:
        pg = Post_Getter(start_time=dt_object, save_fname=new_post_set,
                         city=city, save_type='a')
        pg.get_urls()

    if os.path.isfile(training_set):
        with open(training_set, 'r') as f:
            training_dict = json.load(f)
    else:
        training_dict = {}

    with open(new_post_set, 'r') as f:
        posts_list = json.load(f)

    for data in tqdm.tqdm(posts_list):
        url = data['link']

        # skip links we've already rated
        if url in training_dict:
            continue

        # rate new links
        # open tab
        dr.find_element_by_tag_name('body').send_keys(
            Keys.COMMAND + 't')
        # You can use (Keys.CONTROL + 't') on other OSs

        # Load a page
        dr.get(url)

        # Make the assessment...
        usr_input = input('Post Quality? [1]\n>>')
        if usr_input:
            good = int(usr_input)
        else:
            good = 1
        training_dict[url] = good

        # close the tab
        # (Keys.CONTROL + 'w') on other OSs.
        dr.find_element_by_tag_name('body').send_keys(
            Keys.COMMAND + 'w')

    for idx in range(len(posts_list)):
        posts_list[idx]['score'] = training_dict[posts_list[idx][
            'link']]

    with open('updated_posts.json', 'w') as f:
        json.dump(posts_list, f, indent=4, separators=(',', ':'))

    with open(training_set, 'w') as f:
        json.dump(training_dict, f, indent=4, separators=(',', ':'))
