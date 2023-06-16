import argparse
import PIL.Image
import geojson
import rasterio.features
import numpy as np
import shapely
import openslide
import json

from util import group_by_class, scale_shapes, get_code_to_color_from_profile


def main(args):
    with open(args.profile_path, 'r') as file:
        json_data = json.loads(file.read())
    code_to_color = get_code_to_color_from_profile(json_data)

    # Load Slide
    slide = openslide.open_slide(args.svs_path)
    slide_img = slide.read_region((0,0), len(slide.level_dimensions)-1, slide.level_dimensions[-1]).convert('RGB')

    # Get target resolution
    mpp = float(slide.properties['openslide.mpp-x'])
    full_res = slide.level_dimensions[0]
    downsample_rate = args.output_resolution / mpp
    target_res = np.round(np.array(full_res) / downsample_rate).astype(int)

    # Load Annotations
    geoj = geojson.load(open(args.annotation_path, 'rb'))
    shapes_by_class = group_by_class(geoj)
    shapes_by_class = scale_shapes(shapes_by_class, downsample_rate)

    # Rasterize Annotations
    annotation_img, _ = visualize_annotations(code_to_color, shapes_by_class, [target_res[0], target_res[1]])

    # Blend Annotations and Slide
    PIL.Image.blend(slide_img.resize(target_res), annotation_img, alpha=args.alpha).save(args.output_path)


def visualize_annotations(class_to_color, shapes_by_class, resolution):
    annotation_img = np.zeros(np.array((resolution[1], resolution[0], 3)), dtype=np.uint8)
    area_per_class = {}
    for class_name in shapes_by_class.keys():
        img = rasterio.features.rasterize([shapes_by_class[class_name]], out_shape=np.array((resolution[1], resolution[0])))
        annotation_img[img != 0] = np.array(class_to_color[class_name])

        area_per_class[class_name] = shapely.area(shapes_by_class[class_name])
    annotation_img = PIL.Image.fromarray(annotation_img)

    return annotation_img, area_per_class


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualisation of Whole Slide Image (WSI) and annotations.')

    parser.add_argument('--svs_path', type=str, required=True, help='Path to Whole Slide Image (WSI) as .svs')
    parser.add_argument('--annotation_path', type=str, required=True,
                        help='Annotations as .geojson exported from QuPath')
    parser.add_argument('--profile_path', type=str, required=True, help='Path to the Tissue Maps profile as .json')
    parser.add_argument('--output_path', type=str, required=True, help='Path where the output image is saved')
    parser.add_argument('--output_resolution', type=float, required=True,
                        help='Resolution of the output in micro meters per pixel.')
    parser.add_argument('--alpha', type=float, default=0.5, help='Alpha value for overlay of annotations and WSI')

    args = parser.parse_args()

    print(f"Processing WSI from: {args.svs_path}")
    print(f"\tApplying annotations from: {args.annotation_path}")
    print(f"\tUsing Tissue Types profile: {args.profile_path}")
    print(f"\tOutput will be generated with a resolution of: {args.output_resolution} micrometer per pixel")
    print(f"\tAlpha for overlay: {args.alpha}")

    main(args)