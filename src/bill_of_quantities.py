import os
import pandas as pd

class BillOfQuantities:
    def __init__(self, data):
        content = []
        file_names = []

        #for file in [f for f in os.listdir(data) if f.endswith(".csv")]:
        for file in os.listdir(data):
            if file.endswith(".csv"):
                file_path = os.path.join(data,file)
                df = pd.read_csv(file_path, index_col=0)
                df = df[df["Size"].notnull()]

                df.to_csv(f"output/temp/cleaned_{file}",index = False)
                
                content.append(df)
                file_names.append(file)
        
        master_df = pd.concat(content)
        master_df.to_csv("output/csv/all_cleaned.csv",index = False) 


    def clean_data(self, data):
        return

    def export_to_csv(self):
        return

    def export_to_excel(self):
        return
