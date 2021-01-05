try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': "PW's RPG Game",
    'author': 'Paul-Willem Janse van Rensburg',
    'url': 'no_url_yet',
    'download_url': 'no download url yet',
    'author_email': 'paulwillemjvr@gmail.com',
    'version': '0.1',
    'install_requires': [''],
    'packages': ['pwrpg'],
    'scripts': [],
    'name': 'pwrpg'
}

setup(**config)