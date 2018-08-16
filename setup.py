from setuptools import setup

name = 'GeocodingTools'
version = '0.2.5'
url = 'https://github.com/ad2476/osm-python-tools'

with open('./GeocodingTools/__info__.py', 'w') as f:
    f.write('__name__ = \'%s\'\n' % name)
    f.write('__version__ = \'%s\'\n' % version)
    f.write('__url__ = \'%s\'\n' % url)

setup(
    name = name,
    packages = ['GeocodingTools', 'GeocodingTools.internal'],
    install_requires = [
        'beautifulsoup4',
        'datetime',
        'lxml',
        'matplotlib',
        'numpy',
        'pandas',
        'ujson',
        'xarray',
    ],
    version = version,
    author = 'Franz-Benjamin Mocnik',
    author_email = 'mail@mocnik-science.net',
    description = 'A library to access geocoding services such as OpenStreetMap or Geonames',
    license = 'GPL-3',
    url = url,
    download_url = '',
    keywords = ['OpenStreetMap', 'OSM', 'service', 'geonames', 'nominatim'],
    classifiers = [
        'Programming Language :: Python :: 3',
    ],
)
