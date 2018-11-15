from setuptools import setup

setup(name='craigsbirb',
      version='0.1',
      description='package to send summaries of CL posts that might '
                  'be of interest to the user',
      url='https://github.com/carchard/craigsbirb',
      author='c. archard',
      author_email='carchard0@gmail.com',
      license='GPL3',
      packages=['craigsbirb'],
      install_requires=[
          'bs4',
          'pandas',
          'selenium'
      ],
      zip_safe=False)
