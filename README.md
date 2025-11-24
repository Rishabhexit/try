# Indian Café Manager (Tkinter GUI Application)

## Overview of the Project
The Indian Café Manager is a simple desktop GUI application that makes it easier to take, place, and manage customer orders in a small café. It is created using Python's built-in **Tkinter** library and offers a straightforward interface for selecting menu items, calculating orders, and tracking pending orders.

## Features
* **Dynamic Menu Selection:** You can easily add items from a set Indian snack and beverage menu to the current order.
* **Automatic Total Calculation:** The total amount updates automatically as you add or remove items.
* **Order Management:**
    * **Place Order:** Finalize the current order, give it a unique Order ID, and move it to the pending orders list.
    * **Clear Order:** Reset the current order.
    * **Remove Item:** Take out a selected item from the current order list.
    * **Complete Order:** Mark a pending order as fulfilled and remove it from the list.
* **Pending Order Tracking:** A clear table view (using `ttk.Treeview`) shows all orders awaiting fulfillment, including the Order ID, item summary, and total amount.
* **Alerts and Confirmation:** It uses `messagebox` to provide user feedback on confirmations and errors.

## Technologies/Tools Used
* **Primary Language:** Python 3
* **GUI Framework:** Tkinter (Standard Python Library)
* **Data Structures:** Python dictionaries (`dict`) and lists (`list`) are used for menu, current order, and placed orders storage.

## Steps to Install & Run the Project
l
1.  **Prerequisites:** Make sure you have Python 3 installed on your system. Tkinter usually comes with standard Python installations.
2.  **Save the Code:** Place the provided code into a file named `CAFEMANAGEMENT.PY`.
3.  **Run the Application:** Open your terminal or command prompt, go to the directory where you saved the file, and run:
    ```bash
    python CAFEMANAGEMENT.PY
    ```
4.  The application window ("Indian Café Manager") will open.

## Instructions for Testing
1.  **Creating an Order:** Click on different items in the "Café Menu" frame on the left side. Make sure the items show up in the "Current Order" list and that the "Total" updates correctly.
2.  **Removing Items:** Select an item in the list and click **'Remove Item'**. Confirm that the item is removed and the total decreases accurately.
3.  **Placing an Order:** Click the **'Place Order'** button.
    * Check that a confirmation message appears with the Order ID and Total.
    * Ensure that the order is cleared from the 'Current Order' panel.
    * Verify the new order appears in the "Pending Orders" table below.
4.  **Completing an Order:** Choose an order in the "Pending Orders" table and click **'Complete Selected Order'**. 
    * Confirm that a message appears.
    * Ensure that the order is removed from the pending orders table.
5.  **Error Handling Test:** Attempt to place an order without adding any items. You should see an "Empty Order" warning.