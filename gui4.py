import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class CoffeeShopGUI:
    def __init__(self, master, products):
        self.master = master
        self.master.title("COFFEE PALACE")

        self.products = products
        self.cashier = Cashier(products)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 14), padding=10, background="#808080", foreground="green")
        self.style.configure("TLabel", font=("Arial", 16))
        self.style.configure("TListbox", font=("Arial", 14), width=60, height=15, background="#EFEFEF")
        self.style.configure("TFrame", background="#D3D3D3")

        self.create_widgets()

    def create_widgets(self):
        self.master.geometry("1200x700")
        self.master.resizable(True, True)

        menu_frame = ttk.Frame(self.master, style="TFrame")
        order_frame = ttk.Frame(self.master, style="TFrame")

        self.label = ttk.Label(self.master, text="    Welcome to The COFFEE PALACE\nWhere every Coffee is a Special Coffee!\n         How can I help you!", font=("Courier", 20, "bold"), anchor='center', background="#D3D3D3")
        self.label.pack(pady=10, fill='x')

        self.menu_label = ttk.Label(menu_frame, text="Menu:", font=("Arial", 16, "bold"), background="#D3D3D3")
        self.menu_label.pack()

        self.menu_listbox = tk.Listbox(menu_frame, selectmode=tk.SINGLE, font=("Arial", 14), bd=2, relief=tk.GROOVE, width=60, height=18, background="#EFEFEF")
        for item in self.cashier.display_menu():
            self.menu_listbox.insert(tk.END, item)
        self.menu_listbox.pack(pady=10)

        self.menu_listbox.config(fg='black')  # Set the text color to black

        self.quantity_label = ttk.Label(menu_frame, text="Quantity:", background="#D3D3D3")
        self.quantity_label.pack()
        self.quantity_entry = ttk.Entry(menu_frame, width=24)
        self.quantity_entry.pack()
        self.add_button = ttk.Button(menu_frame, text="Add to Order", command=self.add_to_order, style="TButton")
        self.add_button.pack(pady=5)

        self.complete_order_button = ttk.Button(menu_frame, text="Complete Order", command=self.complete_order, style="TButton")
        self.complete_order_button.pack(pady=5)

        self.order_label = ttk.Label(order_frame, text="Your Order:", font=("Arial", 16, "bold"), background="#D3D3D3")
        self.order_label.pack()

        self.order_listbox = tk.Listbox(order_frame, height=18, width=60, font=("Arial", 14, "italic"), background="#EFEFEF")
        self.order_listbox.pack()

        self.order_listbox.config(fg='black')  # Set the text color to black

        self.remove_button = ttk.Button(order_frame, text="Remove Item", command=self.remove_item, style="TButton")
        self.remove_button.pack(pady=10)

        self.payment_label = ttk.Label(order_frame, text="Payment:", background="#D3D3D3")
        self.payment_label.pack()
        self.payment_entry = ttk.Entry(order_frame, width=24)
        self.payment_entry.pack()
        self.calculate_change_button = ttk.Button(order_frame, text="Calculate Change", command=self.calculate_change, style="TButton")
        self.calculate_change_button.pack(pady=10)

        menu_frame.pack(side=tk.LEFT, padx=20, fill='both', expand=True)
        order_frame.pack(side=tk.RIGHT, padx=20, fill='both', expand=True)

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
        if self.cashier.receipt is not None and self.cashier.receipt.items:
            receipt_text = self.cashier.complete_order()
            self.update_order_display(receipt_text)
        else:
            messagebox.showinfo("Coffee PALACE", "No items in the order.")

    def calculate_change(self):
        try:
            payment = float(self.payment_entry.get())
            if payment >= self.cashier.receipt.total:
                change = payment - self.cashier.receipt.total
                messagebox.showinfo("Change Calculation", f"Change: €{change:.2f}")
                self.cashier.start_new_order()
                self.update_order_display()
            else:
                messagebox.showwarning("Insufficient Payment", "Insufficient payment. Please enter an amount equal to or greater than the total.")
        except ValueError:
            messagebox.showwarning("Invalid Payment", "Please enter a valid numeric payment amount.")

    def update_order_display(self, receipt_text=None):
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

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

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
        iva_rate = 0.21

        receipt_text = f"COFFEE PALACE - {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
        receipt_text += "-" * 40 + "\n"

        for item in self.items:
            item_total = item["price"] * item["quantity"]
            receipt_text += f"{item['name']} x {item['quantity']} - €{item_total:.2f}\n"

        iva_amount = self.total * iva_rate
        receipt_text += f"IVA ({iva_rate * 100}%): €{iva_amount:.2f}\n"

        receipt_text += "-" * 40 + "\n"
        receipt_text += f"TOTAL: €{self.total:.2f}\n"
        receipt_text += "\nThank you for your visit, \nsee you soon!"

        return receipt_text

class Cashier:
    def __init__(self, products):
        self.products = products
        self.receipt = None

    def start_new_order(self):
        self.receipt = Receipt()

    def display_menu(self):
        menu_items = []
        for i, product in enumerate(self.products):
            menu_items.append("{}. {} - €{:.2f}".format(i + 1, product.name, product.price))
        return menu_items

    def take_order(self, index, quantity):
        if self.receipt is None:
            self.start_new_order()
        product = self.products[index]
        self.receipt.add_item(product, quantity)

    def remove_item(self, index):
        if self.receipt is not None and 0 <= index < len(self.receipt.items):
            self.receipt.remove_item(index)

    def complete_order(self):
        if self.receipt is not None and self.receipt.items:
            return self.receipt.print_receipt()

if __name__ == "__main__":
    root = tk.Tk()
    products = [
        Product("Coffee", 1.50, 10),
        Product("Coffee with Milk", 1.95, 10),
        Product("Coffee with Soy Milk", 1.95, 10),
        Product("Tea", 1.20, 15),
        Product("Coca-Cola", 2.80, 10),
        Product("Fanta Naranja", 2.80, 10),
        Product("Nestea", 2.30, 10),
        Product("Beer", 2.30, 20),
        Product("Vermut", 2.20, 20),
        Product("Tuna Sandwich", 3.50, 30),
        Product("Pizza Margarita", 6.50, 8),
        Product("Patatas Bravas", 5.50, 18),
        Product("Hamburger with Cheese", 7.00, 15),        
        Product("Pallea para dos", 45, 10),
        Product("Muffin", 2.00, 25),        
        Product("cheese Cake", 3.50, 12)
    ]
    app = CoffeeShopGUI(root, products)
    root.mainloop()
