from src.bill_of_quantities import BillOfQuantities
import pandas as pd

if __name__ == "__main__":
    boq_hvac_categories = {
        1: 1.00,
        2: 2.50,
        3: 4.00,
        4: 5.00,
        5: 6.00
        }

    my_boq = BillOfQuantities("data")

    my_boq.create_boq("AIR CONDITIONING & VENTILATION INSTALLATION") 
    my_boq.create_boq_sections(boq_hvac_categories)
    my_boq.export_seperate_csvs("output\\csv")
    my_boq.export_to_xlsx()
