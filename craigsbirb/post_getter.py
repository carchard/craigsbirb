import os
import time
import json
import requests
import datetime
from bs4 import BeautifulSoup as bs
from constants import DEBUG_LEVEL
from constants import GETTER_OUTPUT_FILE
from constants import CL_DATE_FORMAT


class Post_Getter:
    def __init__(self, city='boston',
                 start_time=None,
                 save_fname=GETTER_OUTPUT_FILE,
                 save_type='w'):
        if start_time is None:
            self.last_update_time = datetime.datetime.now()
        else:
            self.last_update_time = start_time
        self.save_fname = save_fname
        self.base_url = "https://{}".format(city)
        self.base_url += ".craigslist.org/d/photo-video/search/pha"
        self.latest_content = ""
        self.save_type = save_type
        print("You made a post getter")

    def get_urls(self):
        data = requests.get(self.base_url)
        print("Got response status: {}".format(data.status_code))
        if data.status_code == 200:
            resp = data.text
        else:
            print("Status was not 200!")
            return []
        soup = bs(resp, 'html.parser')
        self.latest_content = soup.find_all('li', 'result-row')

        self.new_links = []
        for block in self.latest_content:
            d1 = block.find_all('a', 'result-title hdrlnk')[0]
            title = d1.string.strip()
            link = d1.attrs['href']

            d2 = block.p.find_all('span', 'result-meta')[0]
            try:
                price = d2.find_all('span',
                                    'result-price')[0].string.strip()
            except IndexError:
                price = "None Provided"
            dt = block.p.time.attrs['datetime']
            if DEBUG_LEVEL <= 2:
                print('\n\n' + "".join(['=']*40))
                print("Title: {}".format(title))
                print("Link: {}".format(link))
                print("Price: {}".format(price))
                print("Post Time: {}".format(dt))
                print()
            dt_formatted = datetime.datetime.strptime(dt,
                                             CL_DATE_FORMAT)
            if dt_formatted > self.last_update_time:
                post_dict = {'title': title,
                             'link': link,
                             'price': price,
                             'time': dt}
                self.new_links.append(post_dict)

        self.last_update_time = datetime.datetime.now()
        self.write_output_file()

    def write_output_file(self):
        if 'a' in self.save_type and os.path.isfile(self.save_fname):
            with open(self.save_fname, 'r') as f:
                self.new_links.extend(json.load(f))

        with open(self.save_fname, 'w') as f:
            json.dump(self.new_links, f, indent=4, sort_keys=True,
                      separators=(',', ':'))


if __name__ == "__main__":
    date_str = '2018-11-12 19:51'
    dt_object = datetime.datetime.strptime(date_str, CL_DATE_FORMAT)
    print(dt_object)
    pg = Post_Getter(start_time=dt_object)
    pg.get_urls()
