import requests
import json
from urllib.parse import urlparse, urlunparse
import geopandas as gpd
from shapely.geometry import Point
from constants import API_PATHS, APIS, BASE_URLS, BASE_CRS, STATES, SRID, PARAM_MAP


def check_state(state) -> str:
    '''
    Used to validate that the input state matches those in constants. This geocoder is built for only those states. Returns an upper case string.

    Args:
        state: the case insensitive two character US State abbreviation.
    '''
    if state and isinstance(state, str) and len(state) == 2:
        state_upper = state.upper()
        if state_upper in STATES:
            return state_upper
        else:
            error_text = 'The value of state must be a case insensitive version of: {}.'.format(', '.join(STATES))
            raise ValueError(error_text)          
    else:
        raise TypeError('The value of state must be a string and not empty')

def get_state(state) -> dict:
    '''
    Used to get the base url of the API for the specified state. Returns a dictionary.

    Args:
        state: the case insensitive two character US State abbreviation.
    '''
    state_upper = check_state(state)
    if state_upper:
        url = [b for b in BASE_URLS if b.get('state') == state_upper][0]
        return url
       
def check_api(api) -> str:
    if api and isinstance(api, str):
        api_lower = api.lower()
        if api_lower in APIS:
            return api_lower
        else:
            error_text = 'The value of api must be a case insensitive version of: {}.'.format(', '.join(APIS))
            raise ValueError(error_text)          
    else:
        raise TypeError('The value of api must be a string and not empty')

def get_api(api) -> dict:
    api_lower = check_api(api)
    api_path = [p for p in API_PATHS if p.get('api') == api_lower][0]
    return api_path

def get_params(state, api) -> dict:
    api_checked = check_api(api)
    state_checked = check_state(state)
    if api_checked and state_checked:
        params = [p for p in PARAM_MAP if (p.get('api') == api_checked and p.get('state') == state_checked)][0]
        return params

def get_endpoint(state, api) -> str:
    api_dict = get_api(api)
    url_dict = get_state(state)
   
    url = url_dict.get('base_url')
    api = api_dict.get('path')
    api_methods = api_dict.get('methods')

    if api and url and api_methods:
        endpoint = urlunparse(urlparse(url + api))
        return endpoint
    else:
        raise ValueError('No endpoint returned!')

def get_response_keys(api) -> list:
    #response_keys = [k for k in OUT_KEYS if k.get('api') == api][0]
    for k in OUT_KEYS:
        if k.get('api') == api:
            response_keys = k.get('keys')
            return response_keys
   
def make_geom(x, y):
    if isinstance(x, float) and isinstance(y, float):
        geom = Point(x, y)
        return geom
    else:
        raise TypeError('x and y must be of type float')
   
def grid_xy(x, y):
    if isinstance(x, float) and isinstance(y, float):
        grid_x5 = str(round(x, 0))[0:5]
        grid_y5 = str(round(y, 0))[0:5]
        grid_x7 = round(x,1)
        grid_y7 = round(y,1)
        grid_dict = {'grid_x': grid_x5
                     ,'grid_y': grid_y5
                     ,'x_rounded': grid_x7
                     ,'y_rounded': grid_y7}
        return grid_dict
    else:
        raise TypeError('x and y must be of type float')

#Limit the extents to subset results to territory envelope
def make_bounds(gdf) -> dict:
    '''
    Take a geodataframe and calculate the bounds of the envelope to use to limit the geocoding results, this is imprecise, but helpful. 
    Structured based on ESRIs requirements. Output as a dict.

    Args:
    gdf: a geodataframe to use to create the envelope.
    '''
    if not gdf.empty and isinstance(gdf, gpd.GeoDataFrame):
        bounds = gdf.envelope.bounds

        if not bounds.empty:
            bounds_dict = bounds.loc[0].to_dict()
            bounds_dict.update({
                                "spatialReference": {
                                                     "wkid": SRID
                                                    }
                               })
            return bounds_dict
        else:
            raise ValueError('The geographic envelope was not successfully generated!')
    else:
        raise TypeError('gdf must be a GeoDataFrame!')

#Clip the results to the territory polygon
def clip_results(in_geom, extent_geom):
    pass