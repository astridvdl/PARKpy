
from src.bill_of_quantities import BillOfQuantities
from src.category import Category

if __name__ == "__main__":
    boq_categories = {
        1: 1.00,
        2: 2.50,
        3: 4.00,
        4: 5.00,
        5: 6.00
        }
    mechanical_boq = BillOfQuantities("raw_data",boq_categories)
    mechanical_boq.create()
    #mechanical_boq.create() #variables?
    mechanical_boq.export("output\\csv")

    '''
    
    mechanical_boq.export_excel("output\\excel")

    cat1 = Category(1, 2.50)
    cat2 = Category(2, 5.50)
    cat3 = Category(3, 5.50)

    cat_list = [cat1, cat2]
    mechanical_boq.categorize(cat_list)

    sortedIntocat1 = cat1.categorizeBOQ(mechanical_boq)



    sortedIntocat1.export_csv()

'''


