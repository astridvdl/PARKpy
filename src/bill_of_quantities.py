import os
import pandas as pd
import numpy as np

class BillOfQuantities:
    
    def __init__(self, data_path, categories):
        self.categories = categories
        self.content_list = []
        self.import_data(data_path)
        self.interpret_data()

    def import_data(self, data):
        #for file in [f for f in os.listdir(data) if f.endswith(".csv")]:
        for file in os.listdir(data):
            if file.endswith(".csv"):
                file_path = os.path.join(data,file)
                df = pd.read_csv(file_path, index_col=0)
                df = df[df["Size"].notnull()]         
                df['File'] = file
                self.content_list.append(df)
        self.content = pd.concat(self.content_list)

    def create(self):
        groups = self.content.groupby(["File"])
        print(groups.all())
        for file_name, group in groups:
            category_groups = group.groupby(["Category"])
            print(category_groups.all())


                


    def interpret_data(self):
        self.split_size()
        self.min_width()
        self.min_height()
        self.collate_area()
        self.add_category()
        #self.cleanup_data()


    def cleanup_data(self):
        self.content = self.content.drop([
            "Insulation Thickness",	
            "Size", 
            "Taper Type",
            "Bend Nominal Radius Scale",
            "Length",
            "Size_1",
            "Size_2",
            "Size_3",
            "Size_1_W",
            "Size_1_H",
            "Size_2_W",
            "Size_2_H",
            "Size_3_W",
            "Size_3_H",
            "Min_Width",
            "Min_Height",
            "Max_W_H",
            "Sum_W_H"], axis = 1)

    def collate_area(self):
        self.content["Area"] = self.content["Area"].apply(lambda x: x.replace(" m²", "")
                                if isinstance(x, str) else x).astype(float)
        self.content["Surface Area"] = self.content["Surface Area"].apply(lambda x: x.replace(" m²", "")
                                if isinstance(x, str) else x).astype(float)
        self.content["Area"] = np.where(self.content["Area"]!=0, self.content["Area"], self.content["Surface Area"])

    def split_size(self):
        self.content[['Size_1', 'Size_2', 'Size_3']] = self.content['Size'].str.split('-', expand=True)
        self.content[['Size_1_W', 'Size_1_H']] = self.content['Size_1'].str.split('x', expand=True)
        self.content[['Size_2_W', 'Size_2_H']] = self.content['Size_2'].str.split('x', expand=True)
        self.content[['Size_3_W', 'Size_3_H']] = self.content['Size_3'].str.split('x', expand=True)
        self.content[['Size_1_W', 'Size_1_H']] = self.content[['Size_1_W', 'Size_1_H']].apply(pd.to_numeric)
        self.content[['Size_2_W', 'Size_2_H']] = self.content[['Size_2_W', 'Size_2_H']].apply(pd.to_numeric)
        self.content[['Size_3_W', 'Size_3_H']] = self.content[['Size_3_W', 'Size_3_H']].apply(pd.to_numeric)

    def min_width(self):
        self.content['Min_Width'] = self.content[['Size_1_W', 'Size_2_W', "Size_3_W"]].min(axis=1)

    def min_height(self):
        self.content['Min_Height'] = self.content[['Size_1_H', 'Size_2_H', "Size_3_H"]].min(axis=1)  

    def add_category(self):
        self.content['Max_W_H'] = self.content[['Min_Width','Min_Height']].max(axis=1)
        self.content['Sum_W_H'] = self.content['Min_Width'] + self.content['Min_Height']
        self.conditions = [
            (self.content['Max_W_H'] < 750) & (self.content['Sum_W_H'] <= 1150),
            (self.content['Max_W_H'] < 750) & (self.content['Sum_W_H'] > 1150),
            (self.content['Max_W_H'] >= 750) & (self.content['Max_W_H'] < 1350),
            (self.content['Max_W_H'] >= 1350) & (self.content['Max_W_H'] < 2100),
            (self.content['Max_W_H'] >= 2100)
        ]
        self.content['Category'] = np.select(self.conditions, self.categories)


    def calc_quantities(self):
        self.content["quantity"] = "some value"
    
    def export(self,location):
        self.content.to_csv(f"{location}\\all_temp.csv")
        print(f"Successfully exported collated file")
        for file in self.content.File.unique():      
            file_data = self.content.loc[self.content["File"] == file]
            file_data.to_csv(f"{location}\\BOQ_{file}")
            print(f"Successfully Interpretted: {file}")
        

           
