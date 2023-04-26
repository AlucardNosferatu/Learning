import xml.etree.ElementTree as ET
import tensorflow as tf
import numpy as np
import os
from PIL import Image
from Config import H, W, H_Counter, W_Counter, Data_Size, useHisto_Counter, oneHot_Counter, DataFileSize
from DIP import add_patch, get_patch, Array2Img, getHisto
import matplotlib.pyplot as plt
from tqdm import tqdm
import pickle

path = "Data4Parser"
pic_path = path + "\\JPG"
xml_path = path + "\\XML"
pic_ext = ".jpg"


def scan_files(directory, prefix="", postfix=""):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if special_file.endswith(postfix) and special_file.startswith(prefix):
                files_list.append(os.path.join(root, special_file))
    return files_list


###############################################
#
#          获取大图中可被检测对象的个数
#
#    一张大图（H*W*3）对应一个整型数（1）
#
###############################################
def get_counts():
    file_list = scan_files(directory=xml_path, postfix=".xml")
    file_list.sort()
    counts = []
    for file in tqdm(file_list[:Data_Size]):
        tree = ET.parse(file)
        root = tree.getroot()
        count = 0
        for obj in root.iter('object'):
            count += 1
        counts.append(count)
    return counts


def count_one_hot(counts, mc):
    new_counts = []
    for i in counts:
        temp = [0] * mc
        temp[i - 1] = 1
        new_counts.append(temp)
    return new_counts


###############################################
#
#      获取某个大图中可被检测的对象list
#
#            一张大图（H*W*3）
# 
#       对应一个xml对象的list（1*list）
#
#         长度由各大图对应counts决定
#
###############################################
def get_objs(file):
    tree = ET.parse(file)
    root = tree.getroot()
    objs = []
    for obj in root.iter('object'):
        objs.append(obj)
    return objs


###############################################
#
#      获取全部大图中可被检测的对象list
#
#       全部大图（batch个数*H*W*3）
# 
#       对应一个xml对象的list（1*list）
#
#       长度由各大图对应counts之和决定
#
###############################################
def get_all_objs():
    file_list = scan_files(directory=xml_path, postfix=".xml")
    file_list.sort()
    objs = []
    for file in tqdm(file_list[:Data_Size]):
        tree = ET.parse(file)
        root = tree.getroot()
        for obj in root.iter('object'):
            objs.append(obj)
    return objs


def get_objs_with_size():
    file_list = scan_files(directory=xml_path, postfix=".xml")
    file_list.sort()
    objs = []
    for file in tqdm(file_list[:Data_Size]):
        tree = ET.parse(file)
        root = tree.getroot()
        temp = []
        for size in root.iter('size'):
            temp.append(size)
        for obj in root.iter('object'):
            temp.append(obj)
        objs.append(temp)
    return objs


###############################################
#
#        获取某个可被检测的对象的分类
# 
#        一个xml对象对应一个分类（str）
#
###############################################
def get_class(obj):
    cls_name = obj.find('name').text.strip().lower()
    return cls_name


###############################################
#
#      获取某大图可被检测的对象的分类集合
# 
#      一大图对应一个分类列表（str型list）
#
###############################################
def get_classes(objs):
    classes = []
    for obj in objs:
        cls_name = obj.find('name').text.strip().lower()
        classes.append(cls_name)
    return classes


###############################################
#
#        获取某个可被检测的对象的坐标
# 
#  一个xml对象对应一个坐标（长度为4的整型list）
#
#               最左上角为原点
#
#     [左上角x，左上角y，右下角x，右下角y]
#
###############################################
def get_coordinate(obj):
    xml_box = obj.find('bndbox')
    xmin = (float(xml_box.find('xmin').text) - 1)
    ymin = (float(xml_box.find('ymin').text) - 1)
    xmax = (float(xml_box.find('xmax').text) - 1)
    ymax = (float(xml_box.find('ymax').text) - 1)
    return [xmin, ymin, xmax, ymax]


###############################################
#
#      获取某大图所有可被检测的对象的坐标
# 
#              一大图的对象list
#
#  对应一个坐标列表（长度为4的整型list的list）
#
#     [左上角x，左上角y，右下角x，右下角y]
#
###############################################
def get_coordinates(objs, normalization=False):
    coordinates = []
    for obj in tqdm(objs):
        if normalization:
            size = obj[0]
            w = int(size.find('width').text)
            h = int(size.find('height').text)
            for i in range(1, len(obj)):
                xml_box = obj[i].find('bndbox')
                xmin = (float(xml_box.find('xmin').text) - 1)/w
                ymin = (float(xml_box.find('ymin').text) - 1)/h
                xmax = (float(xml_box.find('xmax').text) - 1)/w
                ymax = (float(xml_box.find('ymax').text) - 1)/h
                coordinates.append([xmin, ymin, xmax, ymax])
        else:
            xml_box = obj.find('bndbox')
            xmin = (float(xml_box.find('xmin').text) - 1)
            ymin = (float(xml_box.find('ymin').text) - 1)
            xmax = (float(xml_box.find('xmax').text) - 1)
            ymax = (float(xml_box.find('ymax').text) - 1)
            coordinates.append([xmin, ymin, xmax, ymax])
    return coordinates


def GIE_deprecated(file_list=None, used_coordinates=None, patch_check=True):
    imgs = []
    counts = get_counts()
    k = 0
    for i in range(0, len(file_list)):
        img = Image.open(file_list[i])
        img = img.convert("RGB")
        for j in range(0, counts[i]):
            if patch_check:
                plt.imshow(img)
                plt.show()
            img_array = tf.keras.preprocessing.image.img_to_array(img.resize((H, W), Image.ANTIALIAS),
                                                                  data_format="channels_last")
            imgs.append(img_array)
            img = add_patch(img, used_coordinates[k])
            # if(patch_check):
            #    plt.imshow(img)
            #    plt.show()
            k += 1
    return imgs


def GIE(file_list=None, patch_check=True, NoPatch=False):
    imgs = []
    for picFile in tqdm(file_list[:Data_Size]):
        img = Image.open(picFile)
        img = img.convert("RGB")
        ano_file = picFile.replace("JPG", "XML").replace("jpg", "xml")
        objs = get_objs(ano_file)
        for obj in objs:
            c1 = get_coordinate(obj)
            patch_img, background = get_patch(img, c1)
            if not NoPatch:
                for other in objs:
                    c2 = get_coordinate(other)
                    background = add_patch(background, c2)
            background = add_patch(background, c1, source=patch_img)
            if patch_check:
                plt.imshow(background)
                plt.show()
            img_array = tf.keras.preprocessing.image.img_to_array(background.resize((H, W), Image.ANTIALIAS),
                                                                  data_format="channels_last")
            imgs.append(img_array / 255)
    return imgs


###############################################
#
#        将路径下的大图转化为numpy array
#
###############################################     
def get_images(expand4tailor=False, used_coordinates=None, patch_check=False, useHisto=useHisto_Counter, NoPatch=False):
    file_list = scan_files(directory=pic_path, postfix=pic_ext)
    file_list.sort()
    imgs = []
    if expand4tailor:
        # imgs = GIE_deprecated(file_list=file_list,used_coordinates=used_coordinates,patch_check=patch_check)
        imgs = GIE(file_list=file_list, patch_check=patch_check, NoPatch=NoPatch)
    else:
        for path in tqdm(file_list[:Data_Size]):
            img = Image.open(path)
            img = img.convert("RGB")
            img = img.resize((H_Counter, W_Counter), Image.ANTIALIAS)
            if useHisto:
                histo = getHisto(img)
                imgs.append(histo)
            else:
                img_array = tf.keras.preprocessing.image.img_to_array(img, data_format="channels_last")
                imgs.append(img_array / 255)
    return imgs


def labels_normalization(counts):
    mc = max(counts) - 17
    for i in range(0, len(counts)):
        counts[i] /= mc
        if counts[i] > 1:
            counts[i] = 1
    return counts


###############################################
#
#        Counter模型需要的数据装填方法
#
#      输出图片array和对应的分类个数array
#
#   训练图片array：（batch个数，64，64，3）
#
#        分类个数array：（batch个数，1）
#
###############################################
def counter_loader(CheckImgs=False, OneHot=oneHot_Counter):
    if os.path.exists('DataCache\\images_count.pkl'):
        f = open('DataCache\\images_count.pkl', 'rb')
        imgs = pickle.load(f)
        f.close()
    else:
        imgs = get_images()
        f = open('DataCache\\images_count.pkl', 'wb')
        pickle.dump(imgs, f)
        f.close()
    if os.path.exists('DataCache\\counts.pkl'):
        f = open('DataCache\\counts.pkl', 'rb')
        counts = pickle.load(f)
        f.close()
    else:
        counts = get_counts()
        # counts = labels_normalization(counts)
        f = open('DataCache\\counts.pkl', 'wb')
        pickle.dump(counts, f)
        f.close()
    mc = max(counts)
    if OneHot:
        length = len(counts)
        counts = count_one_hot(counts, mc)
        counts_labels = np.array(counts).reshape((length, mc))
    else:
        mc = 1
        counts_labels = np.array(counts).reshape((len(counts), 1))
    images = np.array(imgs)
    if CheckImgs:
        for i in range(0, len(imgs)):
            print(counts[i])
            plt.imshow(imgs[i])
            plt.show()
    return images, counts_labels, mc


def tailor_loader(CheckImgs=False, NoPatch=False):
    c_flist = scan_files("DataCache", prefix="coordinates", postfix=".pkl")
    i_flist = scan_files("DataCache", prefix="images_coordinate", postfix=".pkl")
    coordinates = []
    if len(c_flist) > 0:
        for each in tqdm(c_flist):
            f = open(each, 'rb')
            temp = pickle.load(f)
            f.close()
            coordinates += temp
    else:
        # all_objs = get_all_objs()
        all_objs = get_objs_with_size()
        coordinates = get_coordinates(all_objs,normalization=True)
        files_count = int(len(coordinates) / DataFileSize)
        for i in tqdm(range(0, files_count)):
            temp = []
            if i == files_count - 1:
                temp = coordinates[i * DataFileSize:]
            else:
                temp = coordinates[i * DataFileSize:(i + 1) * DataFileSize]
            f = open('DataCache\\coordinates_' + str(i) + '.pkl', 'wb')
            pickle.dump(temp, f)
            f.close()
    coordinates_labels = np.array(coordinates)
    imgs = []
    if len(i_flist) > 0:
        for each in tqdm(i_flist):
            f = open(each, 'rb')
            temp = pickle.load(f)
            f.close()
            imgs += temp
    else:
        imgs = get_images(expand4tailor=True, used_coordinates=coordinates, NoPatch=NoPatch)
        files_count = int(len(imgs) / DataFileSize)
        for i in tqdm(range(0, files_count)):
            temp = []
            if i == files_count - 1:
                temp = imgs[i * DataFileSize:]
            else:
                temp = imgs[i * DataFileSize:(i + 1) * DataFileSize]
            f = open('DataCache\\images_coordinate_' + str(i) + '.pkl', 'wb')
            pickle.dump(temp, f)
            f.close()
    images = np.array(imgs)
    if CheckImgs:
        for i in range(0, len(imgs)):
            print(coordinates[i])
            plt.imshow(imgs[i])
            plt.show()
    return images, coordinates_labels
