import os
import pandas as pd

class BillOfQuantities:
    def __init__(self, data):
        self.content_list = []
        self.file_names = []
        self.clean_data(data)

    def clean_data(self, data):
        #for file in [f for f in os.listdir(data) if f.endswith(".csv")]:
        for file in os.listdir(data):
            if file.endswith(".csv"):
                file_path = os.path.join(data,file)
                df = pd.read_csv(file_path, index_col=0)
                df = df[df["Size"].notnull()]
                #df.to_csv(f"output/temp/cleaned_{file}",index = False)
                self.content_list.append(df)
                self.file_names.append(file)
        
        singular_df = pd.concat(self.content_list)
        singular_df.to_csv("output/csv/all_cleaned.csv",index = False)
        print(singular_df) 


    def export_to_csv(self):
        return

    def export_to_excel(self):
        return
