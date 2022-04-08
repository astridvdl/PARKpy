import os
import pandas as pd
import numpy as np
from src.boq_section import BoQSection

class BillOfQuantities:
    
    def __init__(self, data_path):
        self.categories = [] #revise
        self.section_names = []
        self.content_list = []
        self._import_components(data_path)
        #self.interpret_data()

    def _import_components(self, directory):
        #for file in [f for f in os.listdir(data) if f.endswith(".csv")]:
        for file in os.listdir(directory):
            if file.endswith(".csv"):
                file_path = os.path.join(directory,file)
                file_name = file.rsplit(".",1)[0]
                
                df = pd.read_csv(file_path)      
                df['Section'] = file_name 
                
                self.content_list.append(df) #rather send df to section object?
                self.section_names.append(file_name)

        self.raw_content = pd.concat(self.content_list) #revise
        self._standardise_components()

    def _standardise_components(self):
        self.raw_content = self.raw_content[self.raw_content["Size"].notnull()]   
        self.raw_content[['Size_1', 'Size_2', 'Size_3']] = self.raw_content['Size'].str.split('-', expand=True)
        self.raw_content[['Size_1_W', 'Size_1_H']] = self.raw_content['Size_1'].str.split('x', expand=True)
        self.raw_content[['Size_2_W', 'Size_2_H']] = self.raw_content['Size_2'].str.split('x', expand=True)
        self.raw_content[['Size_3_W', 'Size_3_H']] = self.raw_content['Size_3'].str.split('x', expand=True)
        self.raw_content[['Size_1_W', 'Size_1_H']] = self.raw_content[['Size_1_W', 'Size_1_H']].apply(pd.to_numeric)
        self.raw_content[['Size_2_W', 'Size_2_H']] = self.raw_content[['Size_2_W', 'Size_2_H']].apply(pd.to_numeric)
        self.raw_content[['Size_3_W', 'Size_3_H']] = self.raw_content[['Size_3_W', 'Size_3_H']].apply(pd.to_numeric)

    def create_boq(self, title):
        #create boq excel file with heading?
        print(title)

    def create_boq_sections(self, categories):
        self.all_sections = []
        section_group = self.raw_content.groupby(["Section"])
        for name, group in section_group:
            sorted_section = BoQSection(name,group)
            sorted_section.format_by(categories)
            self.all_sections.append(sorted_section)
    
    def export_seperate_csvs(self,location):
        for section in self.all_sections:      
            section.export_csv(location)
            print(f"Successfully Created Bill of Quantities for: {section}")


