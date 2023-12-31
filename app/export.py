from PIL import Image
from os.path import join

def get_propper_file_ending(export_type: str) -> str:
    if export_type == "PNG":
        return ".png"
    elif export_type == "JPEG":
        return ".jpeg"
    else:
        return ".png"


def merge_vertical(images, out_path: str, out_file_name: str, export_type: str):
    final_width = max([image.size[0] for image in images])
    final_height = sum([image.size[1] for image in images])
    current_height: int = 0
    combined_image = Image.new("RGB", (final_width, final_height), color=(255, 255, 255))
    for image in images:
        combined_image.paste(image, (0, current_height))
        current_height += image.size[1]
    combined_image.save(join(out_path, f"{out_file_name}_combined{get_propper_file_ending(export_type)}"), export_type)


def merge_horizontal(images, out_path: str, out_file_name: str, export_type: str):
    final_width = sum([image.size[0] for image in images])
    final_height = max([image.size[1] for image in images])
    current_width: int = 0
    combined_image = Image.new("RGB", (final_width, final_height), color=(255, 255, 255))
    for image in images:
        combined_image.paste(image, (current_width, 0))
        current_width += image.size[0]
    combined_image.save(join(out_path, f"{out_file_name}_combined{get_propper_file_ending(export_type)}"), export_type)