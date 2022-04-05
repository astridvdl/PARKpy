import os
import pandas as pd


class Category:
    
    def __init__(self, path):
        self.abs_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        self.path = os.path.join(self.abs_path, path)

    def dataframe(self):
        self.df = pd.read_csv(self.path)
        return self.df

    def catergorize(self, df):
        self.df = df
        self.df[['Size_1', 'Size_2', 'Size_3']] = self.df['Size'].str.split('-', expand=True)
        self.df[['Size_1_W', 'Size_1_H']] = self.df['Size_1'].str.split('x', expand=True)
        self.df[['Size_2_W', 'Size_2_H']] = self.df['Size_2'].str.split('x', expand=True)
        self.df[['Size_3_W', 'Size_3_H']] = self.df['Size_3'].str.split('x', expand=True)
        return self.df


if __name__ == "__main__":
    df1_obj = Category("../data/Duct Fitting Schedule Low Pressure Insulated Rect.csv")
    df1 = df1_obj.dataframe()
    df1 = df1_obj.catergorize(df1)
    print(df1)
    df1.to_csv("test_out.csv",index = False)
    