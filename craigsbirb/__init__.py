import datetime
from post_getter import Post_Getter
from feature_extractor import Feature_Extractor
from post_classifier import Post_Classifier
from email_notifier import Email_Notifier

from constants import CL_DATE_FORMAT

def run_service(update_interval_min=60):
    date_str = '2018-11-13 16:51'
    dt_object = datetime.datetime.strptime(date_str, CL_DATE_FORMAT)
    pg = Post_Getter(start_time=dt_object)
    pg.get_urls()

    fe = Feature_Extractor()
    fe.process_new_posts()


if __name__ == "__main__":
    run_service()
