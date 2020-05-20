from PIL import Image
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np


def scan_files(directory, prefix=None, postfix=None):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))
    return files_list


def add_patch(img, coordinate, source=None):
    c = map(int, coordinate)
    c = tuple(c)
    if (source):
        img.paste(source, c)
    else:
        img.paste((0, 0, 0), c)
    return img


def get_patch(img, coordinate):
    c = map(int, coordinate)
    c = tuple(c)
    BG = img.copy()
    patch = BG.crop(c)
    return patch, BG


def get_objs(file):
    tree = ET.parse(file)
    root = tree.getroot()
    objs = []
    for obj in root.iter('object'):
        objs.append(obj)
    return objs


def get_coordinate(obj):
    xml_box = obj.find('bndbox')
    xmin = (float(xml_box.find('xmin').text) - 1)
    ymin = (float(xml_box.find('ymin').text) - 1)
    xmax = (float(xml_box.find('xmax').text) - 1)
    ymax = (float(xml_box.find('ymax').text) - 1)
    return [xmin, ymin, xmax, ymax]


def Array2Img(imgs_array):
    imgs_array *= 255
    img = Image.fromarray(np.uint8(imgs_array))
    return img


def getHisto(img):
    width, height = img.size
    pixels = img.load()
    r = [0] * 256
    g = [0] * 256
    b = [0] * 256
    for w in range(0, width):
        for h in range(0, height):
            p = pixels[w, h]
            r[p[0]] += 1
            g[p[1]] += 1
            b[p[2]] += 1
    histo = [r, g, b]
    return histo


def region_expansion(image, coordinate):

    pass
