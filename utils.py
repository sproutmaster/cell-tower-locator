import math
import json
import xmltodict

# Semi-axes of WGS-84 geo-dial reference

WGS84_a = 6378137.0  # Major semi axis [m]
WGS84_b = 6356752.3  # Minor semi axis [m]


def degree_to_radians(degrees):
    """
    degrees to radians
    """
    return math.pi * degrees / 180.0


def radians_to_degree(radians):
    """
    radians to degrees
    """
    return 180.0 * radians / math.pi


def wgs84_earth_radius(lat):
    """
    Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
    https://en.wikipedia.org/wiki/Earth_radius
    """
    an = WGS84_a * WGS84_a * math.cos(lat)
    bn = WGS84_b * WGS84_b * math.sin(lat)
    ad = WGS84_a * math.cos(lat)
    bd = WGS84_b * math.sin(lat)
    return math.sqrt((an * an + bn * bn) / (ad * ad + bd * bd))


def bounding_box(latitude_in_degrees, longitude_in_degrees, half_side_in_km):
    """
    Bounding box surrounding the point at given coordinates, assuming local approximation of Earth surface as a sphere
    of radius given by WGS84
    """
    lat = degree_to_radians(latitude_in_degrees)
    lon = degree_to_radians(longitude_in_degrees)
    half_side = 1000 * half_side_in_km

    radius = wgs84_earth_radius(lat)  # Radius of Earth at given latitude

    p_radius = radius * math.cos(lat)  # Radius of the parallel at given latitude

    lat_min = lat - half_side / radius
    lat_max = lat + half_side / radius
    lon_min = lon - half_side / p_radius
    lon_max = lon + half_side / p_radius

    return radians_to_degree(lat_min), radians_to_degree(lon_min), radians_to_degree(lat_max), radians_to_degree(
        lon_max)


def xml_to_json(xml_data):
    json_data = json.dumps(xmltodict.parse(xml_data), indent=4)
    return json_data
