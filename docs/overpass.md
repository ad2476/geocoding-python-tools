[back to readme](../../../)

# Overpass API

## Performing queries

OSM data can be accessed using the [http://wiki.openstreetmap.org/wiki/Overpass_API](Overpass API). While the Overpass API is powerful, it cannot automatically reverse geocode place names. We thus use Nominatim again to query the area id of, for example, NYC:
```python
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
nyc = nominatim.query('NYC')
```
Overpass queries are simple enough to be written by hand, but we will demonstrate how to use the `overpassQueryBuilder`:
```python
from OSMPythonTools.overpass import overpassQueryBuilder
query = overpassQueryBuilder(area=nyc.getAreaId(), elementType='node', selector='"highway"="bus_stop"', out='body')
```
The variable `query` is just a string containing the query:
```
'area(3600175905)->.searchArea;node(area.searchArea);node._["highway"="bus_stop"]; out body;'
```
We can now query an Overpass endpoint:
```python
from OSMPythonTools.overpass import Overpass
overpass = Overpass()
busStops = overpass.query(query)
```
Please observe that the constructor of the class `Overpass` again accepts the parameters `endpoint`, `cacheDir`, and `waitBetweenQueries`.
To query historical data, we can easily add a date:
```python
overpass.query(query, date='2014-01-01T00:00:00Z')
```
Also a timeout can be set:
```python
overpass.query(query, timeout=25)
```

## Accessing the result of a query

The result of the overpass query is an object containing several functions to easily access the data. All elements returned by the query can be accessed:
```python
busStops.elements()
# [<OSMPythonTools.element.Element object at 0x10963c9b0>, <OSMPythonTools.element.Element object at 0x10963c8d0>, ...
```
Each element is of the type [OSMPythonTools.element.**Element**](element.md), and easy methods to access its properties exist.

Also only elements of a certain type can be accessed:
```python
busStops.nodes()
busStops.ways()
busStops.relations()
busStops.areas()
```
In our case, the query only contains nodes because we explicitly queried only for nodes.

In many cases, the number of elements shall be counted. This can easily be achieved using the corresponding functions:
```python
busStops.countElements()
# 542
busStops.countNodes()
# 542
busStops.countWays()
# 0
busStops.countRelations()
# 0
busStops.countAreas()
# 0
```
Overpass queries contain information about the verbosity of the result. If the verbosity is `body`, like in our example, all important information about the bus stops is returned. If `count` is used instead, only the number of elements is returned. The function `busStops.elements()` will return a list of elements in the first case, and `None` in the second case. The function `busStops.countElements()` will return the number of elements in both cases.

Not only the data itself but also meta data about the query can be accessed. We can, for example, test whether the query was valid:
```python
busStops.isValid()
# True
```
Also the raw data can be accessed:
```python
busStops.toJSON()
```
Also other meta data provided by the overpass endpoint can be accessed:
```python
busStops.version()
busStops.generator()
busStops.timestamp_osm_base()
busStops.timestamp_area_base()
busStops.copyright()
busStops.remark()
```