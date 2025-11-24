"""
Indian Café Manager - A simple point-of-sale system for a café
This application helps manage orders from menu selection to completion.
"""

import tkinter as tk
from tkinter import messagebox, ttk


# ============================================================================
# MENU & DATA STORAGE
# ============================================================================

# Our café's menu - add or modify items here
MENU = {
    "Samosa (2 pcs)": 30.00,
    "Vada Pav": 25.00,
    "Paneer Puff": 50.00,
    "Masala Maggi": 60.00,
    "Chai (Regular)": 20.00,
    "Filter Coffee": 40.00,
    "Cold Coffee": 70.00,
    "Gulab Jamun (2 pcs)": 50.00,
    "Chocolate Brownie": 90.00
}

# Keep track of all orders that have been placed
placed_orders = {}

# Counter for assigning unique order IDs
next_order_number = 1

# The order currently being built by the user
current_order = {
    "items": [],      # List of item names
    "total": 0.0      # Running total price
}


# ============================================================================
# ORDER BUILDING FUNCTIONS
# ============================================================================

def add_item_to_order(item_name):
    """
    Add a menu item to the current order.
    Updates both the data and the visual display.
    """
    # Add to our order data
    current_order["items"].append(item_name)
    current_order["total"] += MENU[item_name]
    
    # Show in the order list
    order_listbox.insert(tk.END, item_name)
    
    # Update the total price display
    update_total_display()


def remove_item_from_order():
    """
    Remove the selected item from the current order.
    Useful if customer changes their mind!
    """
    # Get what's selected in the listbox
    selection = order_listbox.curselection()
    
    if not selection:
        messagebox.showinfo(
            "No Selection", 
            "Please select an item to remove."
        )
        return
    
    # Get the item details
    index = selection[0]
    item_name = order_listbox.get(index)
    
    # Remove from our order data
    current_order["items"].remove(item_name)
    current_order["total"] -= MENU[item_name]
    
    # Remove from display
    order_listbox.delete(index)
    update_total_display()


def clear_current_order():
    """
    Clear everything from the current order.
    Starts fresh for a new order.
    """
    current_order["items"] = []
    current_order["total"] = 0.0
    
    # Clear the visual display
    order_listbox.delete(0, tk.END)
    update_total_display()


def update_total_display():
    """
    Update the total price label to show current order total.
    """
    total_label.config(text=f"Total: ₹{current_order['total']:.2f}")


# ============================================================================
# ORDER MANAGEMENT FUNCTIONS
# ============================================================================

def place_order():
    """
    Finalize the current order and move it to pending orders.
    This is called when customer confirms they want to order.
    """
    global next_order_number
    
    # Make sure there's something to order
    if not current_order["items"]:
        messagebox.showwarning(
            "Empty Order", 
            "Please add some items before placing an order!"
        )
        return
    
    # Create a unique order ID
    order_id = next_order_number
    next_order_number += 1
    
    # Save this order (make a copy so we don't lose data)
    placed_orders[order_id] = current_order.copy()
    
    # Add to the pending orders table
    items_summary = ", ".join(current_order["items"])
    pending_orders_tree.insert("", tk.END, values=(
        order_id,
        items_summary,
        f"₹{current_order['total']:.2f}"
    ))
    
    # Show success message to user
    messagebox.showinfo(
        "Order Confirmed! 🎉",
        f"Order #{order_id} has been placed successfully!\n"
        f"Total: ₹{current_order['total']:.2f}"
    )
    
    # Clear everything for the next order
    clear_current_order()


def complete_order():
    """
    Mark a pending order as complete and remove it from the list.
    Call this when the order has been served to the customer.
    """
    # Get the selected order from the table
    selection = pending_orders_tree.selection()
    
    if not selection:
        messagebox.showwarning(
            "No Selection", 
            "Please select an order to complete!"
        )
        return
    
    # Extract order details
    selected_item = selection[0]
    order_id = int(pending_orders_tree.item(selected_item)["values"][0])
    
    # Safety check - make sure order exists
    if order_id not in placed_orders:
        messagebox.showerror(
            "Error", 
            "Order not found in system!"
        )
        return
    
    # Complete the order (remove from pending)
    completed_order = placed_orders.pop(order_id)
    pending_orders_tree.delete(selected_item)
    
    # Show completion message
    messagebox.showinfo(
        "Order Completed! ✅",
        f"Order #{order_id} has been completed.\n"
        f"Amount: ₹{completed_order['total']:.2f}\n\n"
        f"Thank you! Come again!"
    )


# ============================================================================
# GUI SETUP - MAIN WINDOW
# ============================================================================

# Create the main application window
root = tk.Tk()
root.title("🇮🇳 Indian Café Manager")
root.geometry("1000x650")
root.configure(bg="#F5F5DC")  # Warm beige background


# ============================================================================
# LEFT PANEL - MENU SECTION
# ============================================================================

# Frame for the entire menu section
menu_frame = tk.Frame(
    root, 
    bg="#F5F5DC", 
    relief=tk.RIDGE, 
    borderwidth=2
)
menu_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Menu header
tk.Label(
    menu_frame,
    text="☕ Café Menu",
    font=("Arial", 18, "bold"),
    bg="#F5F5DC",
    fg="#8B4513"  # Chocolate brown
).pack(pady=10)

# Create scrollable area for menu items
menu_canvas = tk.Canvas(
    menu_frame, 
    width=280, 
    height=450, 
    bg="#F5F5DC", 
    highlightthickness=0
)
menu_scrollbar = tk.Scrollbar(
    menu_frame, 
    orient="vertical", 
    command=menu_canvas.yview
)
menu_canvas.configure(yscrollcommand=menu_scrollbar.set)

# Pack the canvas and scrollbar
menu_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
menu_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Frame inside canvas to hold all menu buttons
menu_buttons_frame = tk.Frame(menu_canvas, bg="#F5F5DC")
menu_canvas.create_window((0, 0), window=menu_buttons_frame, anchor="nw")

# Create a button for each menu item
for item, price in MENU.items():
    btn = tk.Button(
        menu_buttons_frame,
        text=f"{item}\n₹{price:.2f}",
        font=("Arial", 11),
        bg="#FFE4B5",           # Moccasin - warm yellow
        activebackground="#FFD700",  # Gold when pressed
        command=lambda i=item: add_item_to_order(i),
        width=28,
        height=2,
        cursor="hand2"          # Hand pointer on hover
    )
    btn.pack(pady=5, padx=10)

# Configure scrolling region
menu_buttons_frame.update_idletasks()
menu_canvas.configure(scrollregion=menu_canvas.bbox("all"))


# ============================================================================
# MIDDLE PANEL - CURRENT ORDER SECTION
# ============================================================================

# Frame for current order being built
current_order_frame = tk.Frame(
    root, 
    bg="#F5F5DC", 
    relief=tk.RIDGE, 
    borderwidth=2
)
current_order_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Current order header
tk.Label(
    current_order_frame,
    text="📝 Current Order",
    font=("Arial", 18, "bold"),
    bg="#F5F5DC",
    fg="#8B4513"
).pack(pady=10)

# Listbox showing items in current order
order_listbox = tk.Listbox(
    current_order_frame,
    width=45,
    height=18,
    font=("Arial", 11),
    selectmode=tk.SINGLE  # Only select one item at a time
)
order_listbox.pack(padx=10)

# Frame for action buttons
button_frame = tk.Frame(current_order_frame, bg="#F5F5DC")
button_frame.pack(pady=10)

# Remove item button
tk.Button(
    button_frame,
    text="Remove Item",
    font=("Arial", 10),
    bg="#FFB6C1",              # Light pink
    command=remove_item_from_order,
    width=12,
    cursor="hand2"
).pack(side=tk.LEFT, padx=5)

# Clear all button
tk.Button(
    button_frame,
    text="Clear All",
    font=("Arial", 10),
    bg="#FFA07A",              # Light salmon
    command=clear_current_order,
    width=12,
    cursor="hand2"
).pack(side=tk.LEFT, padx=5)

# Display total price
total_label = tk.Label(
    current_order_frame,
    text="Total: ₹0.00",
    font=("Arial", 16, "bold"),
    bg="#F5F5DC",
    fg="#006400"               # Dark green for money
)
total_label.pack(pady=10)

# Big "Place Order" button
tk.Button(
    current_order_frame,
    text="🛎️ Place Order",
    font=("Arial", 13, "bold"),
    bg="#90EE90",              # Light green
    activebackground="#32CD32",  # Lime green when pressed
    command=place_order,
    width=20,
    height=2,
    cursor="hand2"
).pack(pady=10)


# ============================================================================
# BOTTOM PANEL - PENDING ORDERS SECTION
# ============================================================================

# Frame for pending orders table
pending_orders_frame = tk.Frame(
    root, 
    bg="#F5F5DC", 
    relief=tk.RIDGE, 
    borderwidth=2
)
pending_orders_frame.grid(
    row=1, 
    column=0, 
    columnspan=2, 
    sticky="ew", 
    padx=10, 
    pady=10
)

# Pending orders header
tk.Label(
    pending_orders_frame,
    text="⏳ Pending Orders",
    font=("Arial", 18, "bold"),
    bg="#F5F5DC",
    fg="#8B4513"
).pack(pady=10)

# Table to show all pending orders
columns = ("Order ID", "Items", "Total")
pending_orders_tree = ttk.Treeview(
    pending_orders_frame,
    columns=columns,
    show="headings",           # Hide the default first column
    height=8
)

# Set up column headers
pending_orders_tree.heading("Order ID", text="Order #")
pending_orders_tree.heading("Items", text="Items Ordered")
pending_orders_tree.heading("Total", text="Total Amount")

# Set column widths and alignment
pending_orders_tree.column("Order ID", width=100, anchor=tk.CENTER)
pending_orders_tree.column("Items", width=600)
pending_orders_tree.column("Total", width=150, anchor=tk.CENTER)

pending_orders_tree.pack(padx=10)

# Complete order button
tk.Button(
    pending_orders_frame,
    text="✅ Complete Selected Order",
    font=("Arial", 12, "bold"),
    bg="#87CEEB",              # Sky blue
    activebackground="#4682B4",  # Steel blue when pressed
    command=complete_order,
    width=25,
    height=2,
    cursor="hand2"
).pack(pady=10)


# ============================================================================
# LAYOUT CONFIGURATION
# ============================================================================

# Make the layout responsive to window resizing
root.grid_rowconfigure(0, weight=1)     # Top section can expand
root.grid_rowconfigure(1, weight=0)     # Bottom section stays same size
root.grid_columnconfigure(0, weight=1)  # Left column can expand
root.grid_columnconfigure(1, weight=1)  # Right column can expand


# ============================================================================
# START THE APPLICATION
# ============================================================================

# This starts the GUI event loop - keeps window open and responsive
root.mainloop()