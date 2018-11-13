import os

DATA_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(DATA_PATH, 'tmp')

if not os.path.isdir('tmp'):
    os.mkdir(DATA_PATH)

DEBUG_LEVEL = 1

valid_cities = ['boston', 'philadelphia']

GETTER_OUTPUT_FILE = os.path.join(DATA_PATH, 'getter.json')

CL_DATE_FORMAT = '%Y-%m-%d %H:%M'
