
from PIL import Image

image_path = "maze.png"
initial_point = (0,199)

def get_bitarray(path: str)->list:
    result = []
    with Image.open(path) as img:
        cols, _ = img.size
        row = []
        for pixel in list(img.getdata()):
            if len(row) >= cols:
                result.append(row)
                row = []
            row.append(pixel)
        if len(row)>0:
            result.append(row)
    return result

def get_color(rgb: tuple)->str:
    r,g,b,_ = rgb
    if r==g:
        if g==b:
            if b<127:
                return 'black'
            return 'white'
    if g==255 and b != g:
        return 'green'
    return 'unknown'

def get_valid_children(coords: tuple, maze:list)->list:
    x,y = coords
    possible_coords = []
    if x>0:
        possible_coords.append((x-1,y))
    if x<len(maze[y])-1:
        possible_coords.append((x+1,y))
    if y>0:
        possible_coords.append((x,y-1))
    if y<len(maze)-1:
        possible_coords.append((x,y+1))
    return list(filter(lambda coord: get_color(maze[coord[1]][coord[0]])!='black',possible_coords))
        

def bsf(start:tuple, maze:list):
    parents = [{"point":start, "path": [start]}]
    visited = [start]
    next_parents = []
    while True:
        for parent in parents:
            children = get_valid_children(parent["point"], maze)
            for child in children:
                x,y = child
                if get_color(maze[y][x]) == "green":
                    return parent["path"] + [child]
                if child not in visited:
                    visited.append(child)
                    next_parents.append({"point":child, "path":parent["path"]+[child]})
        parents = next_parents
                


bitarray = get_bitarray(image_path)
path_to_goal = bsf(initial_point, bitarray)
for coord in path_to_goal:
    x,y = coord
    bitarray[y][x] = (0,0,255,255)
size = len(bitarray)
plain = []
for row in bitarray:
    for byte in row:
        plain.extend(byte)
img = Image.frombytes('RGBA', (size,size),bytes(plain))
img.show()
img.save("result.png")