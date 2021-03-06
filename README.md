# GeocodingTools

Incorporates Franz-Benjamin Mocnik's [OSMPythonTools](https://github.com/mocnik-science/osm-python-tools) library into a more general library for geocoding using supported gazetteer services.
Currently supported are: OpenStreetMap [Nominatim](http://nominatim.openstreetmap.org), [Geonames](http://www.geonames.org/). Endpoint implementations rely on the internal `CacheObject` to comply
with API rate limits and obligations of clients to cache requests.

## Installation

To install `GeocodingTools`, you will need Python 3 and `pip` ([How to install pip](https://pip.pypa.io/en/stable/installing/)).
```bash
pip3 install git+https://github.com/ad2476/geocoding-python-tools
```

## OSMPythonTools

The sub-package `OSMPythonTools` provides easy access to [OpenStreetMap (OSM)](http://www.openstreetmap.org) related services, among them an [Overpass endpoint](https://wiki.openstreetmap.org/wiki/Overpass_API), [Nominatim](http://nominatim.openstreetmap.org), and the [OSM API](https://wiki.openstreetmap.org/wiki/API).

### Example 1

*Which object does the way with the id `5887599` represent?*

We can use the OSM API to answer this question:
```python
from OSMPythonTools.api import Api
api = Api()
way = api.query('way/5887599')
```
The resulting object contains information about the way, which can easily be accessed:
```python
way.tag('building')
# 'castle'
way.tag('architect')
# 'Johann Lucas von Hildebrandt'
way.tag('website')
# 'http://www.belvedere.at'
```

### Example 2

*What is the English name of the church called "Stephansdom", what address does it have, and which of which denomination is the church?*

We use the Overpass API to query the corresponding data:
```python
from OSMPythonTools.overpass import Overpass
overpass = Overpass()
result = overpass.query('way["name"="Stephansdom"]; out body;')
```
This time, the result is a number of objects, which can be accessed by `result.elements()`. We just pick the first one: 
```python
stephansdom = result.elements()[0]
```
Information about the church can now easily be accessed:
```python
stephansdom.tag('name:en')
# "Saint Stephen's Cathedral"
'%s %s, %s %s' % (stephansdom.tag('addr:street'), stephansdom.tag('addr:housenumber'), stephansdom.tag('addr:postcode'), stephansdom.tag('addr:city'))
# 'Stephansplatz 3, 1010 Wien'
stephansdom.tag('building')
# 'cathedral'
stephansdom.tag('denomination')
# 'catholic'
```

### Example 3

*How many trees are in the OSM data of Vienna? And how many trees have there been in 2013?*

This time, we have to first resolve the name "Vienna" to an area id:
```python
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
areaId = nominatim.query('Vienna, Austria').areaId()
```
This area id can now be used to build the corresponding query:
```python
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
overpass = Overpass()
query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
result = overpass.query(query)
result.countElements()
# 137830
```
There are 134520 trees in the current OSM data of Vienna. How many have there been in 2013?
```python
result = overpass.query(query, date='2013-01-01T00:00:00Z', timeout=60)
result.countElements()
# 127689
```

### Example 4

*How did the number of trees in Berlin, Paris, and Vienna change over time?*

Before we can answer the question, we have to import some modules:
```python
from collections import OrderedDict
from OSMPythonTools.data import Data, dictRangeYears, ALL
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
```
The question has two "dimensions": the dimension of time, and the dimension of different cities:
```python
dimensions = OrderedDict([
    ('year', dictRangeYears(2013, 2017.5, 1)),
    ('city', OrderedDict({
        'berlin': 'Berlin, Germany',
        'paris': 'Paris, France',
        'vienna': 'Vienna, Austria',
    })),
])
```
We have to define how we fetch the data. We again use Nominatim and the Overpass API to query the data (it can take some time to perform this query the first time!):
```python
overpass = Overpass()
def fetch(year, city):
    areaId = nominatim.query(city).areaId()
    query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
    return overpass.query(query, date=year, timeout=60).countElements()
data = Data(fetch, dimensions)
```
We can now easily generate a plot from the result:
```python
data.plot(city=ALL, filename='example4.png')
```

![data.plot(city=ALL, filename='example4.png')](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/example4.png)

Alternatively, we can generate a table from the result
```python
data.select(city=ALL).getCSV()
# year,berlin,paris,vienna
# 2013.0,10180,1936,127689
# 2014.0,17971,26905,128905
# 2015.0,28277,90599,130278
# 2016.0,86769,103172,132293
# 2017.0,108432,103246,134616
```

More examples can be found inside the documentation of the modules.

### OSMPythonTools Usage

The following modules are available (please click on their names to access further documentation):

* [OSMPythonTools.**Api**](docs/api.md) - Access to the official OSM API
* [OSMPythonTools.**Data**](docs/data.md) - Collecting, mining, and drawing data from OSM; to be used in combination with the other modules
* [OSMPythonTools.**Element**](docs/element.md) - Elements are returned by other services, like the OSM API or the Overpass API
* [OSMPythonTools.**Nominatim**](docs/nominatim.md) - Access to Nominatim, a reverse geocoder
* [OSMPythonTools.**Overpass**](docs/overpass.md) - Access to the Overpass API

## GeonamesTools

Documentation is WIP.

## Author

This library heavily relies on the original OSMPythonTools written by Franz-Benjamin Mocnik, <mail@mocnik-science.net>.
See the commit log for a record of changes.

(c) by Franz-Benjamin Mocnik, 2017-2018.
(c) by Arun Drelich, 2018.

The code is licensed under the [GPL-3](https://github.com/ad2476/geocoding-python-tools/blob/master/LICENSE.md).
