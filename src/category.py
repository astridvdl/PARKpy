import os
import pandas as pd


class Category:
    
    def __init__(self, path):
        self.abs_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        self.path = os.path.join(self.abs_path, path)

    def dataframe(self):
        self.df = pd.read_csv(self.path)
        return self.df

if __name__ == "__main__":
    df1_obj = Category("../data/Duct Fitting Schedule Low Pressure Insulated Rect.csv")
    df1 = df1_obj.dataframe()
    print(df1)
    