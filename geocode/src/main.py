import requests
import json
from dataclasses import dataclass, field, asdict
from typing import Optional
import geopandas as gpd
from shapely.geometry import Point
from constants import FIELD_LENGTHS, SRID, BASE_CRS
from utils import get_api, get_endpoint, get_params, get_response_keys, get_state

@dataclass
class address:
    street_address: str = field(init = True)
    city: str = field(init = True)
    state: str = field(init = True)
    zip_code: Optional[str] = field(init = True, default= None)
    full_address: str = field(init=False, default = None)

    def __post_init__(self):
        self.full_address = ', '.join([v for v in asdict(self).values() if v is not None])
        self.fields_dict = asdict(self)

    def validate_fields(self):
        for k,v in self.fields_dict.items():
            if v is not None:
                if len(v) > FIELD_LENGTHS.get(k):
                    raise ValueError('The length of the {} fields is too long at {}, it can only be {} characters in length'.format(k, v, FIELD_LENGTHS.get(k)))
                else:
                    print('Field {} validated.'.format(k))

    def build_params(self, api):
        params_raw = get_params(self.state, api)
        key_match = set(params_raw).intersection(set(self.fields_dict.keys()))
        key_match.remove('state')
        params_processed = {k: v for k,v in params_raw.items() if k in key_match}
        fields_processed = {k:v for k,v in self.fields_dict.items() if k in key_match}
        self.params = {vt:v for kt,vt in params_processed.items() for k,v in fields_processed.items() if kt == k}
        #Add the key for format parameter, as we always want to return a json
        self.params.update({'f':'json'
                            ,'outSR': SRID})
        print('Request parameters generated.')

    def convert_location(self):
        if self.data and len(self.data) > 0:
            for d in self.data:
                location = d.get('location')
                grid = grid_xy(location.get('x'), location.get('y'))
                d.update(grid)
                d.update({'geometry': make_geom(location.get('x'), location.get('y'))})


    def geocode(self, api):
        self.build_params(api)
        endpoint = get_endpoint(self.state, api)
        response = requests.get(endpoint, params=self.params)
        response_keys = get_response_keys(api)
        if response:
            json_response = response.json()
            #Map the response keys into consistent attributes (spatialreference and data) of the address object
            for k,v in response_keys.items():
                setattr(self, v, json_response.get(k))
            self.convert_location()
            self.data = gpd.GeoDataFrame(self.data, crs = BASE_CRS)
       
test = address(street_address ='78 Brookside Ave', city ='Chester', state = 'NY')
test.validate_fields()
test.build_params(api='findaddresscandidates')
print(test.params)
test.geocode(api='findaddresscandidates')
print(test.data)