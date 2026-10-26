# 🛒 Smart Vending Machine CLI (v2.0)

A modular, terminal-based smart vending machine simulation written in pure Python. The application handles multi-item shopping cart sessions, dynamic inventory management, multi-currency cash and UPI simulations, discount codes, receipt generation, and a protected administrative back-end.

---

## 🚀 Key Features

* **Multi-Item Shopping Cart:** Select multiple items, adjust quantities, view live subtotals, and clear your cart before checkout.
* **Dynamic Inventory Control:** Available stock automatically accounts for items currently held in active user carts, preventing overselling.
* **Dual Payment Processing:**
  * **Cash:** Tracks inserted notes/coins, computes pending balance, dispenses calculated change, and provides a cancellation refund mechanism.
  * **UPI / QR Simulation:** Simulates UPI app payment authorization with a 4-digit PIN verification.
* **Promotions Engine:** Supports order-level discount codes (e.g., `SAVE10` gives 10% off on orders ₹50 and above).
* **Automated Receipt Generation:** Formats and prints itemized receipts with invoice numbering, payment mode details, and change breakdowns.
* **Hidden Admin Panel:** Access via administrative code `999` and a secure PIN (`1234`) to:
  * View cumulative revenue and order metrics.
  * Restock current items.
  * Add entirely new items with custom codes, names, prices, and stock counts.

---

## 📋 Menu & Default Inventory

| Code | Item Name | Price (₹) | Initial Stock |
| :---: | :--- | :---: | :---: |
| `1` | Water Bottle | 20 | 10 |
| `2` | Diet Coke | 30 | 10 |
| `3` | Cold Coffee | 40 | 10 |
| `4` | Potato Chips | 25 | 15 |
| `5` | Chocolate Bar | 50 | 8 |

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.8 or higher installed on your system.

### Running the Project
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/smart-vending-machine.git
   cd smart-vending-machine
