#!/usr/bin/env python3

import argparse
import math
import yaml
from typing import NamedTuple
from PIL import Image, ImageDraw

PADDING_PX = 32


class XY(NamedTuple):
    x: int
    y: int


class Hex():
    center: XY
    radius: int
    corners: list[XY]

    def __init__(self, center: XY, radius: int):
        self.center = center
        self.radius = radius
        self.corners = []
        for corner in range(6):
            self.corners.append(self.corner_coord(corner))

    def corner_coord(self, id: int) -> XY:
        angle = math.radians(60 * id - 30)  # Point up
        return XY(
            int(self.center.x + self.radius * math.cos(angle)),
            int(self.center.y + self.radius * math.sin(angle))
        )

    def draw_border(self, draw):
        draw.line(self.corners + [self.corners[0]],
                  fill=(255, 255, 255, 255), width=2)

    def draw_empty(self, draw):
        draw.polygon(self.corners, fill=(255, 255, 255, 0))


def read_config(path: str):
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
        return config


def coords_to_dict(raw: list[str]) -> dict[str, bool]:
    if not raw:
        return None
    coords = {}
    for coord in raw:
        coords[coord] = True
    return coords


def as_coord(row: int, col: int) -> str:
    return "{0}:{1}".format(row, col)


def calculate_hex_scaling(img_width, img_height, rows, cols) -> int:
    radius_width = int((img_width - PADDING_PX) / (cols * math.sqrt(3)))
    radius_height = int((img_height - PADDING_PX) / (1.5 * (rows + 0.5)))
    return min(radius_width, radius_height)


def slice_image(img, rows, cols, keep):
    img_width, img_height = img.size
    radius = calculate_hex_scaling(img_width, img_height, rows, cols)
    col_width = radius * math.sqrt(3)
    row_height = radius * 1.5
    grid_width = cols * col_width + PADDING_PX
    grid_height = rows * row_height + (radius/2) + PADDING_PX

    x_offset: int = (img_width - grid_width - PADDING_PX) / 2
    y_offset: int = (img_height - grid_height - PADDING_PX) / 2
    img = img.crop((x_offset, y_offset, x_offset +
                   grid_width, y_offset + grid_height))
    y = PADDING_PX / 2 + radius
    draw = ImageDraw.Draw(img)
    for row in range(rows):
        x = PADDING_PX / 2
        if row % 2 == 0:
            x += col_width / 2

        for col in range(cols):
            if col == 0 and row % 2 != 0:
                x += col_width
                continue
            coord = as_coord(row, col)
            center = XY(int(x), int(y))
            hex = Hex(center, radius)
            if keep and coord not in keep:
                hex.draw_empty(draw)
            hex.draw_border(draw)
            x += col_width
        y += row_height

    return img


def generate_map(config):
    print("Generating map for {0}".format(config['map']))
    base = None
    for area in config['areas']:
        img = Image.open(area['img']).convert('RGBA')
        coords = coords_to_dict(area['coords'])
        print("  * Processing area type: {0}".format(area['type']))
        result = slice_image(img, config['width'], config['height'], coords)
        if base:
            base.paste(result, None, result)
        else:
            base = result
    return base


def main():
    parser = argparse.ArgumentParser(
        description='Create a hex map from multiple images'
    )
    parser.add_argument(
        '--config', '-c',
        required=True,
        help='Path to config file'
    )
    args = parser.parse_args()
    config = read_config(args.config)

    img = generate_map(config)
    if not img:
        print("  ! Failed to generate map")
        return
    img.show()
    img.save(config['map'])


if __name__ == '__main__':
    main()
