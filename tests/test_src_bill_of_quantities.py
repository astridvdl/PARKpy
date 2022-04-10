import pytest
from src.bill_of_quantities import BillOfQuantities
import pandas as pd


class TestBillOfQuantities:

    def test_standardise_components_is_string_size_separated_into_width_and_height(self):

        data_out = {"Size": ["950x500-500x500-500x500", "450x550", "450x550-450x550"],
                    "Size_1": ["950x500", "450x550", "450x550"],
                    "Size_2": ["500x500", None, "450x550"],
                    "Size_3": ["500x500", None, None],
                    "Size_1_W" : [950,450,450],
                    "Size_1_H" : [500,550,550],
                    "Size_2_W" : [500,None,450],
                    "Size_2_H" : [500,None,550],
                    "Size_3_W" : [500,None,None],
                    "Size_3_H" : [500,None,None]
        }
        df_out = pd.DataFrame(data_out)
        
        data_in = [["950x500-500x500-500x500"], ["450x550"], ["450x550-450x550"]]
        df_in = pd.DataFrame(data_in, columns = ['Size'])
        data_obj = BillOfQuantities("","")
        data_obj.content = df_in
        BillOfQuantities.split_size(data_obj.content)

        

        assert data_obj.content.equals(df_out)