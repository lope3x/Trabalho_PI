import os

import numpy as np
from PIL import ImageOps
from PIL.Image import Image
from skimage.feature import greycomatrix, greycoprops
from skimage.measure import shannon_entropy
from math import pi
import matplotlib.pyplot as plt


def compute_descriptors(image):
    imageArray = np.array(image, dtype=np.uint8)
    glcm = greycomatrix(imageArray, distances=[1, 2, 4, 8, 16], angles=[0, pi / 4, pi / 2, 3 * pi / 4], levels=256)

    # Debug test
    # matrix = glcm[:,:,0,0]
    #
    # plt.plot(matrix)
    # plt.show()

    contrast = greycoprops(glcm, 'contrast')
    homogenity = greycoprops(glcm, 'homogeneity')
    entropy = []

    glcms = []

    for i in range(0, 5):
        for j in range(0, 4):
            glcms.append(glcm[:, :, i, j])

    for matrix in glcms:
        entropy.append(shannon_entropy(matrix))

    arrayzaocomtudo = []

    for i in contrast:
        for j in i:
            arrayzaocomtudo.append(j)

    for i in homogenity:
        for j in i:
            arrayzaocomtudo.append(j)

    for i in entropy:
        arrayzaocomtudo.append(i)

    return arrayzaocomtudo


def compute_all_descriptors(image):
    image128 = image
    image64 = image.resize((64, 64))
    image32 = image.resize((32, 32))

    descriptors128 = compute_descriptors(image128)
    descriptors64 = compute_descriptors(image64)
    descriptors32 = compute_descriptors(image32)

    descriptors = descriptors32 + descriptors64 + descriptors128
    return descriptors


def loadAndComputeDescriptorsAtPath(path):
    image = Image.open(path)
    imageEqualized = ImageOps.equalize(image)
    imageGray = imageEqualized.convert("L")
    image16Colors = imageGray.quantize(colors=16)
    image32Colors = imageGray.quantize(colors=32)
    allDescriptors = compute_all_descriptors(image32Colors) + compute_all_descriptors(image16Colors)
    return allDescriptors

def readImages():
    basePath = "/imgs/"
    types = [
        1,
        2,
        3,
        4
    ]

    imagesDescriptors = [
        [None],
        [None],
        [None],
        [None]
    ]
    for i in range(1, 5):
        j = 0
        for entry in os.scandir(basePath+str(i)):
            if entry.path.endswith(".png") and entry.is_file():
                imagesDescriptors[i][j] = loadAndComputeDescriptorsAtPath(entry.path)

    for i in range(1, 5):
        print(i)
        print(imagesDescriptors[i])
    #
    #
    # (Image.open(self.filepath)).convert("L")
