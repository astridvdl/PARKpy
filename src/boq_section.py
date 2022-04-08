import pandas as pd
import numpy as np

class BoQSection:
    def __init__(self, name, categories, data):
        self.name = name
        self.categories = categories

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name