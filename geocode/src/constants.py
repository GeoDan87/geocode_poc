from pyproj.crs import CRS
'''
State of New York Geocoding Service (https://gisservices.its.ny.gov/arcgis/rest/services/Locators/Street_and_Address_Composite/GeocodeServer)
Endpoints formatted as METHODS: URL
GET/POST: https://gisservices.its.ny.gov/arcgis/rest/services/Locators/Street_and_Address_Composite/GeocodeServer/findAddressCandidates
GET/POST https://gisservices.its.ny.gov/arcgis/rest/services/Locators/Street_and_Address_Composite/GeocodeServer/geocodeAddresses

State of New Jersey Service (https://geo.nj.gov/arcgis/rest/services/Tasks/NJ_Geocode/GeocodeServer)
Endpoints formatted as METHODS: URL
GET/POST: https://geo.nj.gov/arcgis/rest/services/Tasks/NJ_Geocode/GeocodeServer/findAddressCandidates
GET/POST: https://geo.nj.gov/arcgis/rest/services/Tasks/NJ_Geocode/GeocodeServer/geocodeAddresses

ESRI Developer Documentation
https://developers.arcgis.com/rest/geocode/find-address-candidates/
https://developers.arcgis.com/rest/geocode/geocode-addresses/
'''

BASE_CRS = CRS('EPSG:32015')
SRID = BASE_CRS.to_epsg()

STATES = ['NY', 'NJ']

BASE_URLS = [{
              'state': 'NJ'
              ,'base_url': 'https://geo.nj.gov/arcgis/rest/services/Tasks/NJ_Geocode/GeocodeServer/'
              }
              ,{
              'state': 'NY'
              ,'base_url': 'https://gisservices.its.ny.gov/arcgis/rest/services/Locators/Street_and_Address_Composite/GeocodeServer/'
              }
            ]

APIS = ['geocodeaddresses', 'findaddresscandidates']

API_PATHS = [
             {
               'api': 'geocodeaddresses'
              ,'path': 'geocodeAddresses'
              ,'methods': ['GET', 'POST']
             }  
            ,{
               'api': 'findaddresscandidates'
              ,'path': 'findAddressCandidates'
              ,'methods': ['GET', 'POST']

             }
            ]

PARAM_MAP = [
                {
                    'state':'NY'
                    ,'api':'geocodeaddresses'
                    ,'full_address': 'Address'
                }
                ,{
                    'state':'NJ'
                    ,'api':'geocodeaddresses'
                    ,'full_address': 'Address'
                }
                ,{
                    'state': 'NY'
                    ,'api': 'findaddresscandidates'
                    ,'street_address': 'Street'
                    ,'city': 'City'
                    ,'zip_code': 'ZIP'
                    ,'full_address': 'SingleLine'
                }
                ,{
                 'state': 'NJ'
                ,'api': 'findaddresscandidates'
                ,'street_address': 'Street'
                ,'city': 'City'
                ,'zip_code': 'Postal'
                ,'full_address': 'SingleLine'
                }
            ]

OUT_KEYS = [
             {
               'api': 'geocodeaddresses'
              ,'keys': {
                        'spatialReference': 'spatialreference'
                        ,'locations': 'data'
                       }
             }  
            ,{
               'api': 'findaddresscandidates'
              ,'keys': {
                        'spatialReference': 'spatialreference'
                        ,'candidates': 'data'
                       }
            }
            ]

FIELD_LENGTHS = {'street_address': 100
                 ,'city': 40
                 ,'state': 2
                 ,'zip_code': 5
                 ,'full_address': 147}