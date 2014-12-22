import sys
from graphics import *
from classifier import *
from time import time
def accuracy():
    solver = classifier();
    correct = 0.0;
    total = 0.0;
    with open("validation.data", "r") as f:
        data = f.read().splitlines();
    for row in data:
        instance = row.split();
        predict = solver.solve(instance[1]);
        if (instance[0] == predict):
            correct = correct + 1;
        total = total + 1;
    print "Naive Bayes accuracy: %f" % (correct / total);
