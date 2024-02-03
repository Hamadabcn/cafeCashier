import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Receipt:
    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, product, quantity):
        item = {"name": product.name, "price": product.price, "quantity": quantity}
        self.items.append(item)
        self.total += product.price * quantity

    def remove_item(self, index):
        removed_item = self.items.pop(index)
        self.total -= removed_item["price"] * removed_item["quantity"]

    def print_receipt(self):
        receipt_text = f"COFFEE PLACE - {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
        receipt_text += "-" * 40 + "\n"
        for item in self.items:
            receipt_text += f"{item['name']} x {item['quantity']} - €{item['price'] * item['quantity']:.2f}\n"
        receipt_text += "-" * 40 + "\n"
        receipt_text += f"TOTAL: €{self.total:.2f}\n"
        receipt_text += "Thank you for your visit!"

        return receipt_text

class Cashier:
    def __init__(self, products):
        self.products = products
        self.receipt = Receipt()

    def display_menu(self):
        return [f"{i + 1}. {product.name} - €{product.price:.2f}" for i, product in enumerate(self.products)]

    def take_order(self, index, quantity):
        product = self.products[index]
        self.receipt.add_item(product, quantity)

    def remove_item(self, index):
        if 0 <= index < len(self.receipt.items):
            self.receipt.remove_item(index)

    def complete_order(self):
        receipt_text = self.receipt.print_receipt()
        self.receipt = Receipt()
        return receipt_text

class CoffeeShopGUI:
    def __init__(self, master, products):
        self.master = master
        self.master.title("Coffee Place")

        self.products = products
        self.cashier = Cashier(products)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=10)
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TListbox", font=("Arial", 12), width=40)

        self.create_widgets()

    def create_widgets(self):
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        # Create frames for better organization
        menu_frame = tk.Frame(self.master)
        order_frame = tk.Frame(self.master)

        # Welcome label
        self.label = ttk.Label(self.master, text="Welcome to Coffee Place!", font=("Arial", 18, "bold"))
        self.label.pack(pady=10)

        # Menu listbox
        self.menu_listbox = tk.Listbox(menu_frame, selectmode=tk.SINGLE, height=len(self.products), font=("Arial", 12))
        for item in self.cashier.display_menu():
            self.menu_listbox.insert(tk.END, item)
        self.menu_listbox.pack(pady=10)

        # Quantity entry and Add to Order button
        self.quantity_label = ttk.Label(menu_frame, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = ttk.Entry(menu_frame, width=10)
        self.quantity_entry.pack()
        self.add_button = ttk.Button(menu_frame, text="Add to Order", command=self.add_to_order)
        self.add_button.pack(pady=10)

        # Your Order label and Order Listbox
        self.order_label = ttk.Label(order_frame, text="Your Order:", font=("Arial", 14, "bold"))
        self.order_label.pack()

        # Listbox to display the order
        self.order_listbox = tk.Listbox(order_frame, height=10, width=40, font=("Arial", 12))
        self.order_listbox.pack()

        # Remove Item button and Complete Order button
        self.remove_button = ttk.Button(order_frame, text="Remove Item", command=self.remove_item)
        self.remove_button.pack(pady=10)
        self.complete_order_button = ttk.Button(order_frame, text="Complete Order", command=self.complete_order)
        self.complete_order_button.pack(pady=10)

        # Pack frames
        menu_frame.pack(side=tk.LEFT, padx=20)
        order_frame.pack(side=tk.RIGHT, padx=20)

    def add_to_order(self):
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
        selected_index = self.order_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.cashier.remove_item(index)
            self.update_order_display()
        else:
            messagebox.showwarning("No Selection", "Please select an item to remove from the order.")

    def complete_order(self):
        if self.cashier.receipt.items:
            receipt_text = self.cashier.complete_order()
            self.update_order_display(receipt_text)
        else:
            messagebox.showinfo("Coffee Place", "No items in the order.")

    def update_order_display(self, receipt_text=None):
        self.order_listbox.delete(0, tk.END)
        if receipt_text:
            lines = receipt_text.split('\n')
            for line in lines:
                self.order_listbox.insert(tk.END, line)
        else:
            for item in self.cashier.receipt.items:
                display_text = f"{item['name']} x {item['quantity']} - €{item['price'] * item['quantity']:.2f}"
                self.order_listbox.insert(tk.END, display_text)

if __name__ == "__main__":
    root = tk.Tk()
    products = [
        Product("Coffee", 1.50),
        Product("Tea", 1.20),
        Product("Muffin", 2.00),
        Product("Sandwich", 3.50),
        Product("Cake", 2.50),
        Product("Pizza Margarita", 6.50),
        Product("Patatas Bravas", 5.50),
    ]
    app = CoffeeShopGUI(root, products)
    root.mainloop()
