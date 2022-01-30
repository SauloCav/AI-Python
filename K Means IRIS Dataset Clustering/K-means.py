#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import math
from sklearn import datasets
from matplotlib import pyplot as plt

iris = datasets.load_iris()
X = iris.data
y = iris.target
