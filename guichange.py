import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class Product:
    def __init__(self, name, price, quantity):
        # Initialize a product with a name, price, and quantity
        self.name = name
        self.price = price
        self.quantity = quantity

class Receipt:
    def __init__(self):
        # Initialize a receipt with empty items and total
        self.items = []
        self.total = 0

    def add_item(self, product, quantity):
        # Add an item to the receipt
        item = {"name": product.name, "price": product.price, "quantity": quantity}
        self.items.append(item)
        self.total += product.price * quantity

    def remove_item(self, index):
        # Remove an item from the receipt based on its index
        removed_item = self.items.pop(index)
        self.total -= removed_item["price"] * removed_item["quantity"]

    def print_receipt(self):
        # Generate a receipt text including date, items, IVA, and total
        iva_rate = 0.21  # IVA tax rate (21% in Spain)

        receipt_text = f"COFFEE PALACE - {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
        receipt_text += "-" * 40 + "\n"

        for item in self.items:
            item_total = item["price"] * item["quantity"]
            receipt_text += f"{item['name']} x {item['quantity']} - €{item_total:.2f}\n"

        # Calculate IVA without affecting the total
        iva_amount = self.total * iva_rate
        receipt_text += f"IVA ({iva_rate * 100}%): €{iva_amount:.2f}\n"

        receipt_text += "-" * 40 + "\n"
        receipt_text += f"TOTAL: €{self.total:.2f}\n"
        receipt_text += "\nThank you for your visit, \nsee you soon!"

        return receipt_text

class Cashier:
    def __init__(self, products):
        # Initialize a cashier with a list of products and no current receipt
        self.products = products
        self.receipt = None

    def start_new_order(self):
        # Start a new order by creating a new receipt
        self.receipt = Receipt()

    def display_menu(self):
        # Display the menu as a list of formatted strings
        menu_items = []
        for i, product in enumerate(self.products):
            menu_items.append("{}. {} - €{:.2f}".format(i + 1, product.name, product.price))
        return menu_items

    def take_order(self, index, quantity):
        # Take an order by adding items to the current receipt
        if self.receipt is None:
            self.start_new_order()
        product = self.products[index]
        self.receipt.add_item(product, quantity)

    def remove_item(self, index):
        # Remove an item from the current receipt based on its index
        if self.receipt is not None and 0 <= index < len(self.receipt.items):
            self.receipt.remove_item(index)

    def complete_order(self):
        # Complete the order by generating a receipt text
        if self.receipt is not None and self.receipt.items:
            return self.receipt.print_receipt()

class CoffeeShopGUI:
    def __init__(self, master, products):
        # Initialize the CoffeeShopGUI with a master window and a list of products
        self.master = master
        self.master.title("COFFEE PALACE")

        self.products = products
        self.cashier = Cashier(products)

        # Configure styles for ttk elements
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 16), padding=10)
        self.style.configure("TLabel", font=("Arial", 16))
        self.style.configure("TListbox", font=("Arial", 16), width=60, height=15)  # Adjust width and height here

        # Create GUI widgets
        self.create_widgets()

    def create_widgets(self):
        # Create and configure the main GUI widgets
        self.master.geometry("1200x700")
        self.master.resizable(True, True)  # Allow window resizing

        # Create frames for better organization
        menu_frame = tk.Frame(self.master)
        order_frame = tk.Frame(self.master)

        # Welcome label with bold styling
        self.label = ttk.Label(self.master, text="     Welcome to The COFFEE PALACE!\n Where every Coffee is a special Coffee!", font=("Courier", 30, "bold"))
        self.label.pack(pady=10)

        # Menu label
        self.menu_label = ttk.Label(menu_frame, text="Menu:", font=("Arial", 14, "bold"), background="#EFEFEF")
        self.menu_label.pack()

        # Menu listbox with subtle color and border
        self.menu_listbox = tk.Listbox(menu_frame, selectmode=tk.SINGLE, font=("Arial", 14), bd=2, relief=tk.GROOVE, width=60, height=15)
        for item in self.cashier.display_menu():
            self.menu_listbox.insert(tk.END, item)
        self.menu_listbox.pack(pady=10)

        # Quantity entry and Add to Order button with bold styling
        self.quantity_label = ttk.Label(menu_frame, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = ttk.Entry(menu_frame, width=24)  # Adjust width here
        self.quantity_entry.pack()
        self.add_button = ttk.Button(menu_frame, text="Add to Order", command=self.add_to_order, style="TButton")
        self.add_button.pack(pady=5)

        # Complete Order button with a different color
        self.complete_order_button = ttk.Button(menu_frame, text="Complete Order", command=self.complete_order, style="TButton")
        self.complete_order_button.pack(pady=5)

        # Your Order label and Order Listbox with a different background color
        self.order_label = ttk.Label(order_frame, text="Your Order:", font=("Arial", 14, "bold"), background="#EFEFEF")
        self.order_label.pack()

        # Listbox to display the order with italic font
        self.order_listbox = tk.Listbox(order_frame, height=15, width=60, font=("Arial", 14, "italic"))  # Adjust width and height here
        self.order_listbox.pack()

        # Remove Item button with a different color
        self.remove_button = ttk.Button(order_frame, text="Remove Item", command=self.remove_item, style="TButton")
        self.remove_button.pack(pady=10)

        # Payment Entry and Calculate Change button
        self.payment_label = ttk.Label(order_frame, text="Payment:")
        self.payment_label.pack()
        self.payment_entry = ttk.Entry(order_frame, width=24)
        self.payment_entry.pack()
        self.calculate_change_button = ttk.Button(order_frame, text="Calculate Change", command=self.calculate_change, style="TButton")
        self.calculate_change_button.pack(pady=10)

        # Pack frames
        menu_frame.pack(side=tk.LEFT, padx=20)
        order_frame.pack(side=tk.RIGHT, padx=20)

    def add_to_order(self):
        # Add selected items to the order based on user input
        selected_index = self.menu_listbox.curselection()
        if selected_index:
            try:
                quantity = int(self.quantity_entry.get())
                if quantity > 0:
                    index = selected_index[0]
                    self.cashier.take_order(index, quantity)
                    self.update_order_display()
                else:
                    messagebox.showwarning("Invalid Quantity", "Please enter a valid quantity greater than 0.")
            except ValueError:
                messagebox.showwarning("Invalid Quantity", "Please enter a valid numeric quantity.")
        else:
            messagebox.showwarning("No Selection", "Please select a product from the menu.")

    def remove_item(self):
        # Remove selected items from the order based on user input
        selected_index = self.order_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.cashier.remove_item(index)
            self.update_order_display()
        else:
            messagebox.showwarning("No Selection", "Please select an item to remove from the order.")

    def complete_order(self):
        # Complete the order and display the receipt
        if self.cashier.receipt is not None and self.cashier.receipt.items:
            receipt_text = self.cashier.complete_order()
            self.update_order_display(receipt_text)
        else:
            messagebox.showinfo("Coffee PALACE", "No items in the order.")

    def calculate_change(self):
        # Calculate change for the payment and start a new order
        try:
            payment = float(self.payment_entry.get())
            if payment >= self.cashier.receipt.total:
                change = payment - self.cashier.receipt.total
                messagebox.showinfo("Change Calculation", f"Change: €{change:.2f}")
                # Start a new order after completing the payment
                self.cashier.start_new_order()
                self.update_order_display()
            else:
                messagebox.showwarning("Insufficient Payment", "Insufficient payment. Please enter an amount equal to or greater than the total.")
        except ValueError:
            messagebox.showwarning("Invalid Payment", "Please enter a valid numeric payment amount.")

    def update_order_display(self, receipt_text=None):
        # Update the order display based on the current receipt
        self.order_listbox.delete(0, tk.END)
        if receipt_text:
            lines = receipt_text.split('\n')
            for line in lines:
                self.order_listbox.insert(tk.END, line)
        else:
            for item in self.cashier.receipt.items:
                item_total = item['price'] * item['quantity']
                display_text = f"{item['name']} x {item['quantity']} - €{item_total:.2f}"
                self.order_listbox.insert(tk.END, display_text)

if __name__ == "__main__":
    root = tk.Tk()
    products = [
        Product("Coffee", 1.50, 10),
        Product("Tea", 1.20, 15),
        Product("Beer", 2.30, 20),
        Product("Muffin", 2.00, 25),
        Product("Sandwich", 3.50, 30),
        Product("Cake", 2.50, 12),
        Product("Pizza Margarita", 6.50, 8),
        Product("Patatas Bravas", 5.50, 18),
        # Add more products here
        Product("Hamburger with Cheese", 7.00, 15),
        Product("Coca-Cola", 2.80, 10),
        Product("Vermut", 2.20, 20),
        Product("Fanta Naranja", 2.80, 10),
        Product("Nestea", 2.30, 10)
    ]
    app = CoffeeShopGUI(root, products)
    root.mainloop()
