import os

import numpy as np
from PIL import ImageOps
from PIL import Image
from skimage.feature import greycomatrix, greycoprops
from skimage.measure import shannon_entropy
from sklearn import svm
from math import pi
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def compute_descriptors(image):
    imageArray = np.array(image, dtype=np.uint8)
    glcm = greycomatrix(imageArray, distances=[1, 2, 4, 8, 16], angles=[0, pi / 4, pi / 2, 3 * pi / 4], levels=256)

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


def loadAndComputeDescriptorsAtPath(path=None, image=None):
    if image is None:
        image = Image.open(path)
    imageEqualized = ImageOps.equalize(image)
    imageGray = imageEqualized.convert("L")
    image16Colors = imageGray.quantize(colors=16)
    image32Colors = imageGray.quantize(colors=32)
    allDescriptors = compute_all_descriptors(image32Colors) + compute_all_descriptors(image16Colors)
    return allDescriptors


def readImages():
    basePath = "imgs/"
    typesY = []

    imagesDescriptorsX = []
    for i in range(1, 5):
        j = 0
        print(i)
        for entry in os.scandir(basePath + str(i) + "/"):
            if entry.path.endswith(".png") and entry.is_file():
                j += 1
                print(j)
                imagesDescriptorsX.append(loadAndComputeDescriptorsAtPath(entry.path))
                typesY.append(i)
                if j == 100:
                    break

    print(len(imagesDescriptorsX))

    X_train, X_test, y_train, y_test = train_test_split(imagesDescriptorsX,
                                                        typesY,
                                                        test_size=.3,
                                                        random_state=1234123)

    clf = svm.SVC(kernel='linear', probability=True, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(y_pred)
    print(y_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)
    return clf
