from ctypes import alignment
import os
from numpy import NaN
import pandas as pd
import xlwings as xw
from src.boq_section import BoQSection
class BillOfQuantities:
    
    def __init__(self, data_path):
        self.categories = [] 
        self.section_names = []
        self.content_list = []
        self.data_path = data_path

    def run_csv_out(self):
        self._import_components(self.data_path)
        self.standardise_components()

    def _import_components(self, directory):
        for file in os.listdir(directory):
            if file.endswith(".csv"):
                file_path = os.path.join(directory,file)
                file_name = file.rsplit(".",1)[0]
                
                df = pd.read_csv(file_path)      
                df['Section'] = file_name 
                
                self.content_list.append(df) 
                self.section_names.append(file_name)

        self.raw_content = pd.concat(self.content_list) 
        

    def standardise_components(self):
        self.raw_content = self.raw_content[self.raw_content["Size"].notnull()]   
        self.raw_content[['Size_1', 'Size_2', 'Size_3']] = self.raw_content['Size'].str.split('-', expand=True)
        self.raw_content[['Size_1_W', 'Size_1_H']] = self.raw_content['Size_1'].str.split('x', expand=True)
        self.raw_content[['Size_2_W', 'Size_2_H']] = self.raw_content['Size_2'].str.split('x', expand=True)
        self.raw_content[['Size_3_W', 'Size_3_H']] = self.raw_content['Size_3'].str.split('x', expand=True)
        self.raw_content[['Size_1_W', 'Size_1_H']] = self.raw_content[['Size_1_W', 'Size_1_H']].apply(pd.to_numeric)
        self.raw_content[['Size_2_W', 'Size_2_H']] = self.raw_content[['Size_2_W', 'Size_2_H']].apply(pd.to_numeric)
        self.raw_content[['Size_3_W', 'Size_3_H']] = self.raw_content[['Size_3_W', 'Size_3_H']].apply(pd.to_numeric)
        return self.raw_content

    def create_boq(self, title):
        print(title)

    def create_boq_sections(self, categories):
        self.all_sections = []
        self.section_group = self.raw_content.groupby(["Section"])
        for name, group in self.section_group:
            sorted_section = BoQSection(name,group)
            sorted_section.format_by(categories)
            self.all_sections.append(sorted_section)
    
    def export_seperate_csvs(self,location):
        
        for section in self.all_sections:      
            section.export_csv(location)
            print(f"Successfully Created Bill of Quantities for: {section}")

    def export_to_xlsx(self, workbook="HVAC BOQ - Ducting.xlsx", sheet="MainBOQ", data=pd.DataFrame()):
        self._format_excel_raw(data)
        excel_file = xw.Book()
        excel_file.sheets.add(sheet)
        excel_file.sheets("Sheet1").delete()
        excel_file.save(r"output\\excel\\{0}".format(workbook))
        excel_sheet = excel_file.sheets(sheet)
        excel_sheet.range("A1").value = "Item,Description,Unit,Qty,Rate,Amount".split(',')
        excel_sheet.range("A2").options(transpose=True).value = [1,1.1,1.2,1.3,1.4,1.5]
        excel_sheet.range("B2").options(transpose=True).value = ("Ducting", 
        "Category 1 (W<750 or H<750 or W+H<1150)", 
        "Category 2 (W<750 or H<750 or W+H>1150)", 
        "Category 3 (750<W<1350 or 750<H<1350)", 
        "Category 4 (1350<W<2100 or 1350<H<2100)", 
        "Category 5 (2100<W or 2100<H)")
        excel_sheet["C3"].options(pd.DataFrame, header=0, index=False, expand='table').value = self.df
        total = self.df["Cost"].sum()
        excel_sheet.range("F8").value = total
        excel_sheet.autofit(axis="columns")
        excel_file.save()
        excel_file.close()


    def _format_excel_raw(self, data):
        self.df = data[["Category",	"Quantity",	"Rate",	"Cost"]]
        self.df = self.df[self.df["Rate"].notna()]
        self.df = self.df.groupby(["Category", "Rate"]).sum(["Quantity", "Cost"]).reset_index()
        self.df = self.df[["Quantity","Rate","Cost"]]
        #self.df =self.df.rename(columns = {"Quantity":"Qty", "Cost":"Amount"})
        self.df.insert(0,"Unit","m²")
        print(self.df)
        return self.df

        