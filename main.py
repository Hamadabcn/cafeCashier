# Import the datetime module
import datetime

# Define the class for a product
class Product:
# Initialize the product with its name and price
  def __init__(self, name, price):
    self.name = name
    self.price = price

# Define the class for a receipt
class Receipt:
# Initialize the receipt with an empty list of items and a zero total
  def __init__(self):
    self.items = []
    self.total = 0

# Define the method to add an item to the receipt
  def add_item(self, product, quantity):
    # Create a dictionary with the product name, price, and quantity
    item = {"name": product.name, "price": product.price, "quantity": quantity}
    # Append the item to the items list
    self.items.append(item)
    # Update the total by adding the product price times the quantity
    self.total += product.price * quantity

# Define the method to print the receipt
  def print_receipt(self):
    # Print the header with the current date and time
    print(f"COFFEE PLACE - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Print a line of dashes
    print("-" * 40)
    # Loop through the items list
    for item in self.items:
    # Print the item name, quantity, and price
      print(f"{item['name']} x {item['quantity']} - £{item['price']:.2f}")
    # Print a line of dashes
    print("-" * 40)
    # Print the total
    print(f"TOTAL: £{self.total:.2f}")
    # Print a thank you message
    print("Thank you for your visit!")

# Define the class for a cashier
class Cashier:
# Initialize the cashier with a list of products and a receipt
  def __init__(self, products):
    self.products = products
    self.receipt = Receipt()

# Define the method to display the menu
  def display_menu(self):
    # Print the menu header
    print("Welcome to Coffee Place!")
    print("Please choose from the following products:")
    # Loop through the products list
    for i, product in enumerate(self.products):
    # Print the product index, name, and price
      print(f"{i + 1}. {product.name} - £{product.price:.2f}")

# Define the method to take the order
  def take_order(self):
    # Display the menu
    self.display_menu()
    # Initialize an empty list to store the order
    order = []
    # Loop until the user enters 0
    while True:
    # Prompt the user to enter the product index and quantity
      choice = input("Enter the product index and quantity (e.g. 1 2) or 0 to finish: ")
      # Check if the user entered 0
      if choice == "0":
        # Break the loop
        break
    # Split the choice by space
      choice = choice.split()
    # Check if the choice has two elements
      if len(choice) == 2:
        # Try to convert the elements to integers
        try:
          index = int(choice[0])
          quantity = int(choice[1])
        # Check if the index is valid
          if 1 <= index <= len(self.products):
            # Get the product from the products list
            product = self.products[index - 1]
            # Add the product and quantity to the order list
            order.append((product, quantity))
          else:
            # Print an error message
            print("Invalid product index.")
        except ValueError:
        # Print an error message
          print("Invalid input.")
      else:
        # Print an error message
        print("Invalid input.")
    # Return the order list
    return order

# Define the method to process the order
  def process_order(self, order):
    # Loop through the order list
    for product, quantity in order:
    # Add the item to the receipt
        self.receipt.add_item(product, quantity)

# Define the method to complete the order
  def complete_order(self):
    # Print the receipt
    self.receipt.print_receipt()
    # Clear the receipt
    self.receipt = Receipt()

# Create a list of products
products = [
Product("Coffee", 1.50),
Product("Tea", 1.20),
Product("Muffin", 2.00),
Product("Sandwich", 3.50),
Product("Cake", 2.50),
Product("Pizza Margarita", 6.50)
]

# Create a cashier object
cashier = Cashier(products)

# Test the program
# Take an order
order = cashier.take_order()
# Process the order
cashier.process_order(order)
# Complete the order
cashier.complete_order()
