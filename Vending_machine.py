inventory = {
    "1": ["Water Bottle", 20, 10],
    "2": ["Diet Coke", 30, 10],
    "3": ["Cold Coffee", 40, 10],
    "4": ["Potato Chips", 25, 15],
    "5": ["Chocolate Bar", 50, 8]
}

machine_revenue = 0
receipt_counter = 1000
ADMIN_PIN = "1234"

print("==========================================")
print("       SMART VENDING MACHINE v2.0         ")
print("==========================================")

while True:
    cart = {}  # Stores {item_code: quantity} for the current session

    # --- STEP 1: SHOPPING LOOP ---
    while True:
        print("\n------------------ MENU ------------------")
        print(f"{'Code':<6} {'Item Name':<16} {'Price':<8} {'Status'}")
        print("------------------------------------------")
        for code, (item_name, item_price, item_stock) in inventory.items():
            # Calculate available stock factoring in items already in the user's cart
            in_cart = cart.get(code, 0)
            available_stock = item_stock - in_cart
            stock_status = f"{available_stock} left" if available_stock > 0 else "OUT OF STOCK"
            print(f"[{code}]    {item_name:<16} ₹{item_price:<7} ({stock_status})")
        print("------------------------------------------")

        if cart:
            cart_total = sum(inventory[c][1] * q for c, q in cart.items())
            print(f"🛒 Cart: {sum(cart.values())} item(s) | Subtotal: ₹{cart_total}")
            print("Options: Enter Code to add item | 'PAY' to checkout | 'CLEAR' to empty cart | 'QUIT' to exit")
        else:
            print("Options: Enter Code to select item | 'QUIT' to exit")

        choice = input("\nEnter choice: ").strip().upper()

        if choice == 'QUIT':
            print("\nThank you for visiting! Have a nice day.\n")
            exit()

        # Hidden Admin Access (Enter 999)
        if choice == '999':
            pin = input("Enter Admin PIN: ").strip()
            if pin == ADMIN_PIN:
                while True:
                    print("\n=== ADMIN PANEL ===")
                    print(f"Total Revenue Collected: ₹{machine_revenue}")
                    print(f"Total Orders Completed : {receipt_counter - 1000}")
                    print("1. Restock Existing Item")
                    print("2. Add New Item to Machine")
                    print("3. Exit Admin Panel")
                    admin_choice = input("Select option: ").strip()

                    if admin_choice == '1':
                        r_code = input("Enter item code to restock: ").strip()
                        if r_code in inventory:
                            add_qty = input(f"Enter quantity to add to {inventory[r_code][0]}: ").strip()
                            if add_qty.isdigit() and int(add_qty) > 0:
                                inventory[r_code][2] += int(add_qty)
                                print(f"Updated! New stock for {inventory[r_code][0]}: {inventory[r_code][2]}")
                            else:
                                print("Invalid quantity.")
                        else:
                            print("Item code not found.")
                    elif admin_choice == '2':
                        new_code = input("Enter new item code: ").strip()
                        if new_code in inventory or not new_code:
                            print("Invalid or already existing code.")
                            continue
                        new_name = input("Enter item name: ").strip()
                        new_price = input("Enter item price (₹): ").strip()
                        new_stock = input("Enter opening stock: ").strip()
                        if new_price.isdigit() and new_stock.isdigit() and int(new_price) > 0:
                            inventory[new_code] = [new_name, int(new_price), int(new_stock)]
                            print(f"{new_name} added successfully!")
                        else:
                            print("Invalid price or stock numbers.")
                    elif admin_choice == '3':
                        break
            else:
                print("Access Denied: Incorrect PIN.")
            continue

        if choice == 'CLEAR':
            cart.clear()
            print("Cart cleared!")
            continue

        if choice == 'PAY':
            if not cart:
                print("Your cart is empty! Add some items first.")
                continue
            break  # Proceed to checkout

        if choice not in inventory:
            print("Invalid choice. Please try again!")
            continue

        # Fetch selected item details
        name, price, stock = inventory[choice]
        available_stock = stock - cart.get(choice, 0)

        if available_stock <= 0:
            print(f"Sorry, no more {name} available to add.")
            continue

        print(f"\nSelected: {name} - ₹{price} (Available: {available_stock})")
        qty_input = input(f"Enter quantity of {name} (or '0' to cancel): ").strip()

        if not qty_input.isdigit():
            print("Invalid input! Please enter a valid number.")
            continue

        quantity = int(qty_input)
        if quantity == 0:
            continue
        if quantity < 0:
            print("Quantity must be at least 1.")
            continue
        if quantity > available_stock:
            print(f"Sorry, we only have {available_stock} more {name}(s) available.")
            continue

        cart[choice] = cart.get(choice, 0) + quantity
        print(f"Added {quantity} x {name} to your cart!")

        # Ask user if they want to checkout immediately or keep shopping
        next_step = input("Press Enter to add more items, or type 'PAY' to checkout: ").strip().upper()
        if next_step == 'PAY':
            break

    # --- STEP 2: CHECKOUT & PROMO CODES ---
    subtotal = sum(inventory[c][1] * q for c, q in cart.items())
    discount = 0

    print("\n================ CHECKOUT ================")
    for c, q in cart.items():
        i_name, i_price, _ = inventory[c]
        print(f"{q} x {i_name:<16} = ₹{i_price * q}")
    print("------------------------------------------")
    print(f"Subtotal: ₹{subtotal}")

    if subtotal >= 50:
        promo = input("Have a promo code? (Try 'SAVE10' or press Enter to skip): ").strip().upper()
        if promo == "SAVE10":
            discount = int(subtotal * 0.10)
            print(f"Promo applied! You saved ₹{discount}.")
        elif promo != "":
            print("Invalid promo code. Proceeding without discount.")

    final_total = subtotal - discount
    print(f"Total Payable Amount: ₹{final_total}")

    # --- STEP 3: PAYMENT PROCESSING ---
    payment_success = False
    payment_method = ""
    change_given = 0
    amount_paid = 0

    while not payment_success:
        print("\nSelect Payment Method:")
        print("[1] Cash (Notes / Coins)")
        print("[2] UPI / QR Pay")
        print("[3] Cancel Order")
        pay_choice = input("Enter payment option (1/2/3): ").strip()

        if pay_choice == '1':
            payment_method = "Cash"
            inserted = 0
            while inserted < final_total:
                remaining = final_total - inserted
                cash_in = input(f"Insert Cash (Remaining ₹{remaining}) or type 'CANCEL': ").strip().upper()
                if cash_in == 'CANCEL':
                    if inserted > 0:
                        print(f"Refunding your inserted ₹{inserted}...")
                    break
                if not cash_in.isdigit() or int(cash_in) <= 0:
                    print("Please insert a valid positive rupee amount.")
                    continue
                inserted += int(cash_in)

            if inserted >= final_total:
                amount_paid = inserted
                change_given = inserted - final_total
                payment_success = True

        elif pay_choice == '2':
            payment_method = "UPI"
            pin = input(f"Approve ₹{final_total} on your UPI app. Enter 4-digit UPI PIN: ").strip()
            if len(pin) == 4 and pin.isdigit():
                amount_paid = final_total
                change_given = 0
                payment_success = True
            else:
                print("Transaction Failed! Invalid 4-digit UPI PIN.")

        elif pay_choice == '3':
            print("Order cancelled. Returning to main menu...")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

    # --- STEP 4: DISPENSE & PRINT RECEIPT ---
    if payment_success:
        receipt_counter += 1
        machine_revenue += final_total

        # Deduct purchased quantities from inventory
        for c, q in cart.items():
            inventory[c][2] -= q

        print("\n==========================================")
        print("              OFFICIAL RECEIPT            ")
        print(f"Receipt No: #{receipt_counter:<10} Mode: {payment_method}")
        print("------------------------------------------")
        print(f"{'Item':<18} {'Qty':<5} {'Price'}")
        print("------------------------------------------")
        for c, q in cart.items():
            i_name, i_price, _ = inventory[c]
            print(f"{i_name:<18} x{q:<4} ₹{i_price * q}")
        print("------------------------------------------")
        if discount > 0:
            print(f"{'Subtotal':<24} ₹{subtotal}")
            print(f"{'Discount (SAVE10)':<24} -₹{discount}")
        print(f"{'Total Amount':<24} ₹{final_total}")
        print(f"{'Amount Paid':<24} ₹{amount_paid}")
        if change_given > 0:
            print(f"{'Change Returned':<24} ₹{change_given}")
        print("==========================================")
        print("✅ Payment Successful!")
        if change_given > 0:
            print(f"🪙 Please collect your change of ₹{change_given} from the coin tray.")
        print("📦 Order dispensed. Please collect your items below!\n")
