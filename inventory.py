"""
Let us assume that you work for a Nike warehouse. As store manager you are
responsible for stock taking.
Nike warehouses store the following information for each shoe item:
- Country
- Code
- Product
- Cost
- Quantity

Users (store managers) can use the program to do the following:
- capture new shoes to inventory
- view all shoes in inventory
- search shoes by code
- restock lowest quantity item
- show value for each item
- show highest quantity item
"""

#======== Libraries ==========
# make sure you have the tabulate library installed by doing the following:
# - Type CMD in the search bar and open the Command Prompt application.
# - Type "pip install tabulate --user" and press Enter
# if installation does not work, follow steps in https://www.youtube.com/watch?v=I6-_W-SuSG4
from tabulate import tabulate

#========The beginning of the class==========
class Shoe:
    # Instance variables (specific to a particular instance of the class)
    def __init__(self, country, code, product, cost, quantity):
        '''
        In this function, initialises the following attributes:
            - country
            - code
            - product
            - cost
            - quantity
        '''
        self.country  = str(country)
        self.code     = str(code)
        self.product  = str(product)
        self.cost     = int(cost)
        self.quantity = int(quantity)

    def get_cost(self, code):
        '''
        returns the cost of the shoe for a specific shoe code.
        '''
        if self.code == code:
            return self.cost
        else:
            print("code not found")

    def get_quantity(self):
        '''
        returns the quantity of the shoes
        '''
        return self.quantity
    
    def get_value(self):
        """
        returns value = cost * quantity
        """
        return self.cost * self.quantity
    
    def __str__(self):
        '''
        returns a string representation of the shoe class
        '''
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"
    
    def print_table(self):
        """
        prints the string represenation of the shoe with headers in table form
        using Python's tabulate module (see https://pypi.org/project/tabulate/)
        """
        print(tabulate([str(self).split(",")], headers=["Country","Code","Product","Cost","Quantity"]))


#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []

#==========Functions outside the class==============
def underline(my_string):
    """
    function underlines a given string
    """
    return "\u0332" + my_string

def read_inventory():
    '''
    Function opens inventory.txt and reads the data from this file 
    '''
    try:
        in_file = open("inventory.txt","r")
    except OSError:
        # if opening the file causes an error
        # (see https://www.topbug.net/blog/2020/10/03/catching-filenotfounderror-watch-out/)
        contents = "error"
        return contents

    # if opening of file was successful
    contents = in_file.read()
    in_file.close()
    return contents

def write_to_inventory(my_string):
    """
    write data to inventory.txt (overwrite)
    """
    f = open("inventory.txt","w")        
    f.write(my_string)
    f.close()
    return

def write_shoe_list_to_inventory():
    """
    function writes the shoe list to the inventory file
    """
    inventory_update = "Country,Code,Product,Cost,Quantity"
    for shoe in shoe_list:
        inventory_update += "\n" + str(shoe)
    write_to_inventory(inventory_update)

def read_shoes_data():
    '''
    Function converts each line from inventory.txt into a shoe object and 
    appends it to the shoe list (ignores first line, representing the header)
    '''
    # Each line in the inventory represents data to create one Shoe object
    inventory = read_inventory()

    for line in inventory.split("\n")[1::]: # skips first line (header)
        country  = line.split(",")[0].strip()
        code     = line.split(",")[1].strip()
        product  = line.split(",")[2].strip()
        cost     = line.split(",")[3].strip()
        quantity = line.split(",")[4].strip()
        shoe_obj = Shoe(country, code, product, cost, quantity) 
        shoe_list.append(shoe_obj)
    return shoe_list

def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    # user inputs
    country  = input("Country:  ").strip()
    code     = input("Code:     ").strip()
    product  = input("Product:  ").strip()

    cost = None
    while cost is None:
        try:
            cost     = float(input("Cost:     ").strip())
        except ValueError:
            print(f"Oops, this is not a float. Please try again.")

    quantity = None
    while quantity is None:
        try:
            quantity = float(input("Quantity: ").strip())
        except ValueError:
            print(f"Oops, this is not a float. Please try again.")

    # create shoe object        
    shoe_obj = Shoe(country, code, product, cost, quantity)

    # add user created shoe to shoe list
    shoe_list.append(shoe_obj)

    # write updated shoe list to inventory file
    write_shoe_list_to_inventory()

    # prints shoe object to console (in table form)
    print(f"\n{shoe_obj.product} has been added to inventory:\n")
    shoe_obj.print_table()

def view_all():
    '''
    This function iterates over the shoes list and produces a table  
    using Python's tabulate module (see https://pypi.org/project/tabulate/)
    '''
    table = []
    for shoe in shoe_list:
        table.append(str(shoe).split(","))
    print(tabulate(table, headers=["Country","Code","Product","Cost","Quantity"]))

def re_stock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Asks the user how much 
    quantity of shoes they want to re-stock. This quantity is updated on
    the file for this shoe.
    '''
    # Find the shoe object with the lowest quantity: assume the first shoe in the list
    # is the one with the lowest quantity. Update this assumption whenever you find one
    # in the shoe list with an even lower quantity.
    lowest_q = shoe_list[0]
    for shoe in shoe_list:
        # if shoe has lower quantity than lowest_q, update lowest_q
        if shoe.quantity < lowest_q.quantity:
            lowest_q = shoe
    
    # prints lowest shoe object (in table form)
    print(f"\n{lowest_q.product} has lowest quantity:\n")
    lowest_q.print_table()

    # Ask user how much quantity to re-stock
    add_quantity = int(input("How much quantity would you like to add? "))
    lowest_q.quantity = lowest_q.quantity + add_quantity

    # write updated shoe list to inventory file
    write_shoe_list_to_inventory()

    # message to console
    print(f"Updated quantity for {lowest_q.product} (quantity: {lowest_q.quantity})")

def search_shoe():
    pass
    '''
    This function searches for a shoe from the list using the
    shoe code and returns this object so that it will be printed.
    '''
    code_lookup = input("What shoe code are you looking for? \nInput: ").strip().lower()
    is_found = False
    while is_found == False:
        for shoe in shoe_list:
            if shoe.code.lower() == code_lookup:
                # prints shoe object (in table form)
                shoe.print_table()
                is_found = True
                break # breaks for loop
        
        if is_found == False:
            # if code not found, try again or exit to return to menu
            code_lookup = input(f"""Code not found. Try again (type {underline("e")} to {underline("e")}xit to menu)\nInput: """).strip().lower()
            if code_lookup == "e":
                break
        else:
            # break while loop if code was found
            break
    
def value_per_item():
    pass
    '''
    This function calculates the total value for each item and
    prints this information on the console for all the shoes 
    using Python's tabulate module (see https://pypi.org/project/tabulate/)
    '''
    table = []
    for shoe in shoe_list:
        value = shoe.get_value()
        table.append(str(shoe).split(",") + [value])
    print(tabulate(table, headers=["Country","Code","Product","Cost","Quantity","Value"]))

def highest_qty():
    '''
    Function determines the product with the highest quantity and
    print this shoe as being for sale.
    '''
    # Assume the first shoe in the list is the one with the highest quantity.
    # Update this assumption whenever you find one in the shoe list with an 
    # even higher quantity.
    highest_q = shoe_list[0]
    for shoe in shoe_list:
        # if shoe has higher quantity than highest_q, update highest_q
        if shoe.quantity > highest_q.quantity:
            highest_q = shoe
    
    # prints lowest shoe object (in table form) as being on sale
    print(f"\n{highest_q.product} is on SALE:\n")
    highest_q.print_table()

#==========Main Menu=============
'''
Menu that executes each function above.
'''
# read shoes data from inventory file
read_shoes_data()

while True:
    menu = input(f"""
Please select among the following:
c      {underline("c")}apture new shoe to inventory
va     {underline("v")}iew {underline("a")}ll shoes in inventory
s      {underline("s")}earch shoes by code
re     {underline("re")}stock lowest quantity item
v      show {underline("v")}alue for each item
hq     show {underline("h")}ighest {underline("q")}uantity
e      {underline("e")}xit

selection: """).strip().lower()
    if menu == "c":
        capture_shoes()

    elif menu == "va":
        view_all()

    elif menu == "re":
        re_stock()

    elif menu == "s":
        search_shoe()

    elif menu == "v":
        value_per_item()

    elif menu == "hq":
        highest_qty()

    elif menu == "e":
        print("Goodbye!")
        exit()

    else:
        # on Error
        print("You have made a wrong choice, Please Try again")