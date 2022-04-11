from src.boq_section import BoQSection
import pandas as pd
class TestBillOfQunatities:
    # def test_min_width_in_multiple_columns_determine_minumum():
    #     pass

    # def test_min_height_height_in_multiple_columns_determine_minumum():
    #     pass

    def test_collate_area_given_in_two_columns_summarize_one_area_column(self):
        data_in = {"Category": ["950x500-500x500-500x500", "450x550", "450x550-450x550"],
                    "Size_1": ["950x500", "450x550", "450x550"],
                    "Size_2": ["500x500", None, "450x550"],
                    "Size_3": ["500x500", None, None],
                    "Size_1_W" : [950,450,450],
                    "Size_1_H" : [500,550,550],
                    "Size_2_W" : [500,None,450],
                    "Size_2_H" : [500,None,550],
                    "Size_3_W" : [500,None,None],
                    "Size_3_H" : [500,None,None],
                    "Area" : [100,0,50],
                    "Surface Area": [0,60,500],
        }
        df_in = pd.DataFrame(data_in)
        test_section = BoQSection("Test Section", df_in)
        data_expected = {"Category": ["950x500-500x500-500x500", "450x550", "450x550-450x550"],
                    "Size_1": ["950x500", "450x550", "450x550"],
                    "Size_2": ["500x500", None, "450x550"],
                    "Size_3": ["500x500", None, None],
                    "Size_1_W" : [950,450,450],
                    "Size_1_H" : [500,550,550],
                    "Size_2_W" : [500,None,450],
                    "Size_2_H" : [500,None,550],
                    "Size_3_W" : [500,None,None],
                    "Size_3_H" : [500,None,None],
                    "Area" : [100,0,50],
                    "Surface Area": [0,60,500],
                    "Quantity": [100,0,50]
        }
        df_expected = pd.DataFrame(data_expected)

        test_section.collate_quantity()

        assert not df_expected.equals(test_section.output())

    # def test_add_category_data_not_categorized_adds_category_according_to_criteria():
    #     pass

    # def test_cleanup_data_columns_not_needed_further_remove_redundant_columns():
    #     pass
