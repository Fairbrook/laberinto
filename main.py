
from copy import copy
from PIL import Image

image_path = "maze.png"
initial_point = (0, 199)


def get_bitarray(path: str) -> list:
    result = []
    with Image.open(path) as img:
        cols, _ = img.size
        row = []
        for pixel in list(img.getdata()):
            if len(row) >= cols:
                result.append(row)
                row = []
            row.append(pixel)
        if len(row) > 0:
            result.append(row)
    return result


def get_color(rgb: tuple) -> str:
    r, g, b, _ = rgb
    if r == g:
        if g == b:
            if b < 127:
                return 'black'
            return 'white'
    if g == 255 and b != g:
        return 'green'
    return 'unknown'


def get_valid_children(coords: tuple, maze: list) -> list:
    x, y = coords
    possible_coords = []
    if x > 0:
        possible_coords.append((x-1, y))
    if x < len(maze[y])-1:
        possible_coords.append((x+1, y))
    if y > 0:
        possible_coords.append((x, y-1))
    if y < len(maze)-1:
        possible_coords.append((x, y+1))
    return list(filter(lambda coord: get_color(maze[coord[1]][coord[0]]) != 'black', possible_coords))


def bsf(start: tuple, maze: list):
    parents = [{"point": start, "path": [start]}]
    visited = [start]
    next_parents = []
    while True:
        for parent in parents:
            children = get_valid_children(parent["point"], maze)
            for child in children:
                x, y = child
                if get_color(maze[y][x]) == "green":
                    return parent["path"] + [child]
                if child not in visited:
                    visited.append(child)
                    next_parents.append(
                        {"point": child, "path": parent["path"]+[child]})
        parents = next_parents


def draw_path(path: list, image: list):
    image_copy = copy(image)
    for coord in path:
        x, y = coord
        image_copy[y][x] = (0, 0, 255, 255)
    return image_copy


def matrix_to_img(matrix: list):
    matrix_copy = copy(matrix)
    image = []
    for row in matrix_copy:
        for byte in row:
            image.extend(byte)
    return bytes(image)


def show_result(path: list, image: list):
    size = len(image)
    img = Image.frombytes('RGBA', (size, size),
                          matrix_to_img(draw_path(path, image)))
    img.show()
    img.save("result.png")


bitarray = get_bitarray(image_path)
path_to_goal = bsf(initial_point, bitarray)
show_result(path_to_goal, bitarray)
