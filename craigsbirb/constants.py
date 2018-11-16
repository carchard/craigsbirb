import os

DATA_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(DATA_PATH, 'tmp')

if not os.path.isdir('tmp'):
    os.mkdir(DATA_PATH)

DEBUG_LEVEL = 3

valid_cities = ['boston', 'philadelphia']

non_numeric_cols = ['title', 'link']

GETTER_OUTPUT_FILE = os.path.join(DATA_PATH, 'getter.json')
EXTRACTOR_OUTPUT_FILE = os.path.join(DATA_PATH, 'extractor.json')
CLASSIFIER_OUTPUT_FILE = os.path.join(DATA_PATH, 'classifier.json')

CL_DATE_FORMAT = '%Y-%m-%d %H:%M'

PRICE_DEFAULT = 1500  # a large value but not an outlier

KEYWORDS = ["nikon",
            "24mm",
            "f1.2",
            "f/1.2",
            "f1.4",
            "f/1.4",
            "canon",
            "85mm",
            "ef-m",
            "eos-m",
            "carbon",
            "fx",
            "full",
            'm3',
            'lens',
            '2.8',
            'f2.8',
            'f/2.8',
            '50mm',
            '5D',
            'D850',
            'D610',
            '6D'
            ]

BADWORDS = ["tamron",
            "f3.5",
            "wanted",
            "vintage",
            "antique",
            "wtb",
            'tripod',
            'film'
            ]
