import functools
import operator
import shapely
import numpy as np

from operator import itemgetter
from itertools import groupby


def hex_to_rgb(hex):
    return tuple(int(hex[1:].upper()[i:i+2], 16) for i in (0, 2, 4))


def group_by_class(geoj):
    classes = [(idx, x['properties']['classification']['name']) for idx, x in enumerate(geoj['features'])]
    classes.sort(key=itemgetter(1))
    groups = groupby(classes, itemgetter(1))
    grouped_by_class = {key: shapely.GeometryCollection([shapely.from_geojson(str(geoj['features'][item[0]])) for item in data]) for (key, data) in groups}

    return grouped_by_class


def scale_poly(feats, downsample_rate):
    poly_points = functools.reduce(operator.iconcat, [x['geometry']['coordinates'] for x in feats], [])
    scaled_polygons = [np.round(np.array(x) / downsample_rate).astype(np.int32) for x in poly_points]
    return scaled_polygons


def scale_coordinates(coords, scale_factor):
    return coords // scale_factor


def scale_shapes(shapes, scale_factor):
    shapes = {k: shapely.transform(v, lambda v: scale_coordinates(v, scale_factor)) for k, v in shapes.items()}
    return shapes


def get_code_to_color_from_profile(json_obj):
    result = {}

    def iterate_nested_json(json_obj):
        for elem in json_obj:
            if 'color' in elem:
                result[elem['code']] = hex_to_rgb(elem['color'])
            if 'children' in elem:
                iterate_nested_json(elem['children'])

    iterate_nested_json(json_obj)
    return result


def get_code_to_id_from_profile(json_obj):
    result = {}

    def iterate_nested_json(json_obj):
        for elem in json_obj:
            if 'code' in elem:
                result[elem['code']] = elem['id']
            if 'children' in elem:
                iterate_nested_json(elem['children'])

    iterate_nested_json(json_obj)
    return result

