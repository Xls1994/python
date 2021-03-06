#!/usr/bin/python
import numpy as np

for i in range(100000):
    predictionF = "/home/jason/memoryCorpus/result/predict_"+ str(i)+".txt"
    goldF = "/home/jason/memoryCorpus/labels"
    try:
        predictions = np.loadtxt(predictionF, np.float)
        golds       = np.loadtxt(goldF, dtype=np.float)
    except:
        break

    count = 0.0
    index = 0
    correct = 0.0
    for one_hot in predictions:
        if np.argmax(one_hot) == np.argmax(golds[index]):
            correct += 1.0
        index += 1
        count += 1
    print("Accuracy "+ str(i) + ": " + str(float(correct / count)))