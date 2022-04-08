from src.bill_of_quantities import BillOfQuantities

if __name__ == "__main__":
    boq_hvac_categories = {
        1: 1.00,
        2: 2.50,
        3: 4.00,
        4: 5.00,
        5: 6.00
        }

    my_boq = BillOfQuantities("raw_data")
    #mechanical_boq.create_boq_sections(boq_categories)
    my_boq.create_boq("AIR CONDITIONING & VENTILATION INSTALLATION") #create excel
    my_boq.create_boq_sections(boq_hvac_categories)
    my_boq.export_seperate_csvs("output\\csv")
    #mechanical_boq.export_Excel("output\\excel)
