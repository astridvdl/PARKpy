from src.bill_of_quantities import BillOfQuantities

if __name__ == "__main__":
    mechanical_boq = BillOfQuantities("raw_data")
    mechanical_boq.split_size()
    mechanical_boq.min_width()
    mechanical_boq.min_height()
    mechanical_boq.categorize()

    mechanical_boq.export("output\\csv")





