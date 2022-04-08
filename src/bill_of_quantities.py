from operator import index
import os
from unicodedata import name
import pandas as pd
import numpy as np
from src.boq_section import BoQSection

class BillOfQuantities:
    
    def __init__(self, data_path):
        self.categories = [] #revise
        self.section_names = []
        self.content_list = []
        self._import_data(data_path)
        #self.interpret_data()

    def _import_data(self, data):
        #for file in [f for f in os.listdir(data) if f.endswith(".csv")]:
        for file in os.listdir(data):
            if file.endswith(".csv"):
                file_path = os.path.join(data,file)
                file_name = file.rsplit(".",1)[0]
                
                df = pd.read_csv(file_path)
                df = df[df["Size"].notnull()]         
                #df['File'] = file
                
                self.content_list.append(df) #rather send df to section object?
                #section = self.create_section(file_name)
                self.section_names.append(file_name)

        #self.content = pd.concat(self.content_list) #revise

    def create_boq(self, categories):
        #create boq heading?
        self.create_boq_sections(categories, self.section_names, self.content_list)
        # required?

    def create_boq_sections(self,categories,section_names, component_data):
        self.sorted_sections = []
        for section in enumerate(section_names):
            #section_components = 
            print (f"\n----\n{section[0]}: {section[1]}")
            print(component_data[section[0]])
            #sorted_section = self.create_section(section, categories, all_components[0])
            #sorted_section = BoQSection(section, categories, all_components[0])
            #self.sorted_sections.append(sorted_section)
            #print(sorted_section.name())
        
        self.content = pd.concat(self.content_list)

    def create_section(self, name, categories, components):  
        return BoQSection(name, categories, components) 




    def create(self):
        file_grouped = self.content.groupby(["File"])
        for file_name, group in file_grouped:
            print(file_name)           
            category_grouped = group.groupby(["Category"]).sum()
            
            category_grouped["Rate"] = category_grouped.index.to_series().apply(lambda x:self.categories[x])
            category_grouped["Cost"] = category_grouped["Quantity"] * category_grouped["Rate"]
            category_grouped.loc["Total", "Cost"] = category_grouped["Cost"].sum()
            print(category_grouped)

            category_grouped.to_csv(f"output\\csv\\Test_BOQ_{file_name}", index = True)





    def organise_data(self):
        self.split_size()
        self.min_width()
        self.min_height()
        self.collate_area()
        #self.add_category()
        #self.cleanup_data()


    def cleanup_data(self):
        self.content = self.content.drop([
            "Bend Angle",
            "Insulation Type",
            "Insulation Thickness",	
            "Size",
            "Count",
            "Area",
            "Surface Area", 
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
        self.content["Quantity"] = np.where(self.content["Area"]!=0, self.content["Area"], self.content["Surface Area"])

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
        #self.content['Rate'] = np.select(self.conditions, self.categories.values())


    def calc_quantities(self):
        self.content["quantity"] = "some value"
    
    def export(self,location):
        self.content.to_csv(f"{location}\\all_temp.csv")
        print(f"Successfully exported collated file")
        for file in self.content.File.unique():      
            file_data = self.content.loc[self.content["File"] == file]
            file_data.to_csv(f"{location}\\BOQ_{file}")
            print(f"Successfully Interpretted: {file}")
        

           
