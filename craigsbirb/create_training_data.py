import json
import os
import tqdm
import webbrowser
import datetime
from post_getter import Post_Getter
from constants import CL_DATE_FORMAT

file_dir = os.path.dirname(os.path.realpath(__file__))
training_dir = os.path.join(file_dir, 'training_data')
if not os.path.isdir(training_dir):
    os.mkdir(training_dir)

training_set = os.path.join(training_dir, 'training.json')
new_post_set = os.path.join(training_dir, 'new_posts.json')


if __name__ == "__main__":
    date_str = '2018-11-10 16:51'
    dt_object = datetime.datetime.strptime(date_str, CL_DATE_FORMAT)
    pg = Post_Getter(start_time=dt_object, save_fname=new_post_set)
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
        webbrowser.open(url, new=0)
        usr_input = input('Post Quality? [1]\n>>')
        if usr_input:
            good = int(usr_input)
        else:
            good = 1
        training_dict[url] = good

    with open(training_set, 'w') as f:
        json.dump(training_dict, f, indent=4, separators=(',', ':'))
