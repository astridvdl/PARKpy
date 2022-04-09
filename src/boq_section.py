import numpy as np
class BoQSection:
    def __init__(self, name, data):
        self.name = name
        self.content = data
        self._standardise_section_components()

    def _standardise_section_components(self):
        self._min_width()
        self._min_height()
        self._collate_quantity()

    def _min_width(self):
        self.content['Min_Width'] = self.content[['Size_1_W', 'Size_2_W', "Size_3_W"]].min(axis=1)

    def _min_height(self):
        self.content['Min_Height'] = self.content[['Size_1_H', 'Size_2_H', "Size_3_H"]].min(axis=1) 

    def _collate_quantity(self):
        self.content["Area"] = self.content["Area"].apply(lambda x: x.replace(" m²", "")
                                if isinstance(x, str) else x).astype(float)
        self.content["Surface Area"] = self.content["Surface Area"].apply(lambda x: x.replace(" m²", "")
                                if isinstance(x, str) else x).astype(float)
        self.content["Quantity"] = np.where(self.content["Area"]!=0, self.content["Area"], self.content["Surface Area"]) 

    def format_by(self, categories):
        self._add_categories(categories)  
        self._cleanup_data()
        category_grouped = self.content.groupby(["Category"]).sum()
        
        category_grouped["Rate"] = category_grouped.index.to_series().apply(lambda x:categories[x])
        category_grouped["Cost"] = category_grouped["Quantity"] * category_grouped["Rate"]
        category_grouped.loc["Total", "Cost"] = category_grouped["Cost"].sum()

        self.content = category_grouped
        return category_grouped
    
    def _add_categories(self,categories):
        self.content['Max_W_H'] = self.content[['Min_Width','Min_Height']].max(axis=1)
        self.content['Sum_W_H'] = self.content['Min_Width'] + self.content['Min_Height']
        conditions = [
            (self.content['Max_W_H'] < 750) & (self.content['Sum_W_H'] <= 1150),
            (self.content['Max_W_H'] < 750) & (self.content['Sum_W_H'] > 1150),
            (self.content['Max_W_H'] >= 750) & (self.content['Max_W_H'] < 1350),
            (self.content['Max_W_H'] >= 1350) & (self.content['Max_W_H'] < 2100),
            (self.content['Max_W_H'] >= 2100)
        ]
        self.content['Category'] = np.select(conditions, categories)

    def _cleanup_data(self):
        self.content = self.content.drop([
            "Family and Type",
            "Section",
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

    def output(self):
        return self.content

    def __str__(self)-> str:
        return self.name

    def export_csv(self,location):
        self.content.to_csv(f"{location}\\BOQ_{self.name}.csv")
