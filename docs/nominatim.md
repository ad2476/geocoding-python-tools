[back to readme](../../../)

# Nominatim

## Reverse geocoding

OSM data contains numerous place names. Nominatim is a reverse geocoder which is able to identify geometries in OSM data corresponding to a given string. If you are, for example, interested in the German town Heidelberg, you can query:
```python
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
heidelberg = nominatim.query('Heidelberg')
```
The result of this query is an object which contains a number of functions to access the data. Most important, the area id can be accessed:
```python
heidelberg.areaId()
# 3600285864
```
This raw data provided by Nominatim potentially contains more than one geometry. The function `areaId` only returns the area id of the first geometry. The (complete) raw data of the answer by Nominatim can be accessed:
```python
heidelberg.toJSON()
# [{'place_id': '580259', 'licence': 'Data © OpenStreetMap ...
```

If you want to know the geometry as [well-known text](https://en.wikipedia.org/wiki/Well-known_text), you have to provide an corresponding parameter for the request, because this will inform the Nominatim webservie to provide the geometry in the result:
```python
heidelberg = nominatim.query('Heidelberg', wkt=True)
heidelberg.wkt()
# 'POINT(8.694724 49.4093582)'
```
Additional parameters can be sent with the query request by providing a `params` dictionary to `nominatim.query`.

## Parameters

As a default, `OSMPythonTools.Nominatim` uses the endpoint `https://nominatim.openstreetmap.org/search`. If another one should be used, for example, a local one, corresponding data can be provided:
```python
nominatim = Nominatim(endpoint='https://nominatim.openstreetmap.org/search')
```
The data is automatically cached into a the directory `./cache`. If another directory shall be used, the directory name can be provided:
```python
nominatim = Nominatim(cacheDir='cache')
```
In case of numerous requests, one may want to delay the requests. The fetching process can, for example, be instructed to wait 2 seconds between the queries sent to Nominatim:
```python
nominatim = Nominatim(waitBetweenQueries=2)
```
Also combinations of `endpoint`, `cacheDir`, and `waitBetweenQueries` can be used.
