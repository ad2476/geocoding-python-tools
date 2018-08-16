import urllib.parse

from GeocodingTools.internal.cacheObject import CacheObject

class Geonames(CacheObject):
    def __init__(self, username, endpoint='http://api.geonames.org/search', **kwargs):
        super().__init__('geonames', endpoint, **kwargs)
        self._user = username

    def _queryString(self, query, **kwargs):
        params = kwargs.get("params", {})
        return (query, query, params)

    def _queryRequest(self, endpoint, queryString, params=None):
        if not params:
            params = {}
        queryParams = {'type':'json', 'q':queryString, 'username':self._user, **params}
        queryParams = urllib.parse.urlencode(queryParams, safe='')
        return "{}?{}".format(endpoint, queryParams)

    def _rawToResult(self, data, queryString):
        return GeonameResult(data['geonames'], queryString)

class GeonameResult:
    def __init__(self, json, queryString):
        self._json = json
        self._queryString = queryString

    def toJSON(self):
        return self._json

    def queryString(self):
        return self._queryString

    def areaId(self):
        for d in self._json:
            if 'geonameId' in d:
                return d['geonameId']
        return None
