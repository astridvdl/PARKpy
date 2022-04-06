from src.category import Category
from src.bill_of_quantities import BillOfQuantities

if __name__ == "__main__":
    df1_obj = Category("../data/Duct Fitting Schedule Low Pressure Insulated Rect.csv")
    df1 = df1_obj.dataframe()
    df1 = df1_obj.split_size(df1)
    df1 = df1_obj.min_width(df1)
    df1 = df1_obj.min_height(df1)
    df1 = df1_obj.categorize(df1)
    # print(df1)




data_location = "raw_data"
mechanical_boq = BillOfQuantities(data_location)
mechanical_boq.export_to_csv()
mechanical_boq.export_to_excel()
print(mechanical_boq)



