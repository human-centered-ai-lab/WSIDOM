import argparse
import json
import geojson
import openslide
import numpy as np
import rasterio.features
import PIL

from util import get_code_to_id_from_profile
from util import group_by_class, scale_shapes


def export_annotations(code_to_color, all_layer_annotations, resolution):
    annotation_img = np.zeros(np.array((resolution[1], resolution[0], 3)), dtype=np.uint8)

    for idx, layer_annotations in enumerate(all_layer_annotations):
        for class_name in layer_annotations.keys():
            img = rasterio.features.rasterize([layer_annotations[class_name]], out_shape=np.array((resolution[1], resolution[0])))
            annotation_img[img != 0, idx] = np.array(code_to_color[class_name])

    annotation_img = PIL.Image.fromarray(annotation_img)

    return annotation_img



def export(args):
    with open(args.profile_path, 'r') as file:
        json_data = json.loads(file.read())
    code_to_id = get_code_to_id_from_profile(json_data)

    # Get target resolution
    slide = openslide.open_slide(args.svs_path)
    mpp = float(slide.properties['openslide.mpp-x'])
    full_res = slide.level_dimensions[0]
    downsample_rate = args.output_resolution / mpp
    target_res = np.round(np.array(full_res) / downsample_rate).astype(int)

    # Load Annotations
    all_layer_annotations = []
    for path in [args.layer_1_path, args.layer_2_path, args.layer_3_path]:
        geoj = geojson.load(open(path, 'rb'))
        shapes_by_class = group_by_class(geoj)
        shapes_by_class = scale_shapes(shapes_by_class, downsample_rate)
        all_layer_annotations.append(shapes_by_class)

    # Rasterize Annotations
    annotation_img = export_annotations(code_to_id, all_layer_annotations, [target_res[0], target_res[1]])

    # Export Annotations
    annotation_img.save(args.output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export annotations from Whole Slide Image (WSI) as Tissue Maps .png')

    parser.add_argument('--svs_path', type=str, required=True, help='Path to Whole Slide Image (WSI) as .svs')
    parser.add_argument('--layer_1_path', type=str, required=True, help='Layer 1 annotations as .geojson exported from QuPath')
    parser.add_argument('--layer_2_path', type=str, required=True, help='Layer 2 annotations as .geojson exported from QuPath')
    parser.add_argument('--layer_3_path', type=str, required=True, help='Layer 3 annotations as .geojson exported from QuPath')
    parser.add_argument('--profile_path', type=str, required=True, help='Path to the Tissue Maps profile as .json')
    parser.add_argument('--output_path', type=str, required=True, help='Path where the output image is saved')
    parser.add_argument('--output_resolution', type=float, required=True,
                        help='Resolution of the output in micro meters per pixel.')

    args = parser.parse_args()

    export(args)