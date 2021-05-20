import os

import numpy as np
from PIL import ImageOps
from PIL import Image
from skimage.feature import greycomatrix, greycoprops
from skimage.measure import shannon_entropy
from sklearn import svm
from math import pi
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

from joblib import dump, load


def loadSVM():
    return load('svm.joblib')


def saveSVM(clf):
    dump(clf, 'svm.joblib')


def compute_entropy_for_glcm4D(glcm4D):
    entropyList = []
    for i in range(0, 5):
        for j in range(0, 4):
            entropy = shannon_entropy(glcm4D[:, :, i, j])
            entropyList.append(entropy)
    return entropyList


def compute_descriptors(image):
    imageArray = np.array(image, dtype=np.uint8)
    glcm4D = greycomatrix(imageArray, distances=[1, 2, 4, 8, 16], angles=[0, pi / 4, pi / 2, 3 * pi / 4], levels=256)

    contrastMatrix = greycoprops(glcm4D, 'contrast')
    homogeneityMatrix = greycoprops(glcm4D, 'homogeneity')
    entropyList = compute_entropy_for_glcm4D(glcm4D)

    contrastList = np.hstack(contrastMatrix)
    homogeneityList = np.hstack(homogeneityMatrix)

    return list(contrastList) + list(homogeneityList) + list(entropyList)


def compute_for_all_images_sizes(image):
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
    allDescriptors = compute_for_all_images_sizes(image32Colors) + compute_for_all_images_sizes(image16Colors)
    return allDescriptors


def readImagesAndComputeDescriptors():
    basePath = "imgs/"
    types = []
    imagesDescriptors = []
    num_of_images_processed = 0
    for i in range(1, 5):
        for entry in os.scandir(basePath + str(i) + "/"):
            if entry.path.endswith(".png") and entry.is_file():
                imagesDescriptors.append(loadAndComputeDescriptorsAtPath(entry.path))
                types.append(i)
                num_of_images_processed += 1
                print(f"Gerando descritores {num_of_images_processed}/400")
    return imagesDescriptors, types


def trainSVM():
    imagesDescriptors, types = readImagesAndComputeDescriptors()

    X_train, X_test, y_train, y_test = train_test_split(imagesDescriptors,
                                                        types,
                                                        test_size=.25)

    clf = svm.SVC(kernel='linear', probability=True, random_state=42)
    print("Iniciando treinamento do SVM")
    clf.fit(X_train, y_train)

    y_predicted = clf.predict(X_test)
    print(f"Predicted Values {y_predicted}")
    print(f"Expected Values {y_test}")
    accuracy = accuracy_score(y_test, y_predicted)

    confusionMatrix = confusion_matrix(y_test, y_predicted)

    print(confusionMatrix)

    computeMetrics(confusionMatrix)

    print(f"Accuracy {accuracy}")
    return clf


def computeMetrics(confusionMatrix):
    mean_sensibility = 0
    for i in range(0, 3):
        mean_sensibility += confusionMatrix[i][i] / 100

    sum = 0

    for i in range(0, 3):
        for j in range(0, 3):
            if i != j:
                sum += confusionMatrix[i][j] / 300
    specificity = 1 - sum

    print(f"Sensiblidade Média: {mean_sensibility}")
    print(f"Especificidade: {specificity}")
