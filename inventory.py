
import csv
import os
from datetime import datetime

PRODUCT_FILE = "products.csv"
SALES_FILE = "sales.csv"


# Create CSV files automatically
def create_files():
    if not os.path.exists(PRODUCT_FILE):
        with open(PRODUCT_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["product_id", "name", "price", "quantity"])

    if not os.path.exists(SALES_FILE):
        with open(SALES_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "bill_id", "date", "product_id",
                "product_name", "quantity",
                "unit_price", "total"
            ])


# Read products
def load_products():
    with open(PRODUCT_FILE, "r", newline="") as file:
        return list(csv.DictReader(file))


# Save products
def save_products(products):
    with open(PRODUCT_FILE, "w", newline="") as file:
        fields = ["product_id", "name", "price", "quantity"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(products)


# Add product
def add_product():
    products = load_products()

    product_id = input("Enter Product ID: ").strip()

    if any(p["product_id"] == product_id for p in products):
        print("Product ID already exists!")
        return

    name = input("Enter Product Name: ").strip()

    try:
        price = float(input("Enter Product Price: "))
        quantity = int(input("Enter Quantity: "))

        if not name or price <= 0 or quantity < 0:
            print("Enter valid product details!")
            return

    except ValueError:
        print("Please enter valid numbers!")
        return

    products.append({
        "product_id": product_id,
        "name": name,
        "price": str(price),
        "quantity": str(quantity)
    })

    save_products(products)
    print("Product added successfully!")


# View products
def view_products():
    products = load_products()

    if not products:
        print("No products available!")
        return

    print("\n----------- PRODUCT INVENTORY -----------")
    print(f"{'ID':<10}{'Name':<20}{'Price':<12}{'Stock':<10}")
    print("-" * 52)

    for p in products:
        print(
            f"{p['product_id']:<10}"
            f"{p['name']:<20}"
            f"{float(p['price']):<12.2f}"
            f"{p['quantity']:<10}"
        )


# Search product
def search_product():
    products = load_products()
    product_id = input("Enter Product ID to search: ").strip()

    for p in products:
        if p["product_id"] == product_id:
            print("\nProduct Found!")
            print("Name:", p["name"])
            print("Price:", p["price"])
            print("Quantity:", p["quantity"])
            return

    print("Product not found!")


# Update product
def update_product():
    products = load_products()
    product_id = input("Enter Product ID to update: ").strip()

    for p in products:
        if p["product_id"] == product_id:
            try:
                new_price = float(input("Enter New Price: "))
                new_quantity = int(input("Enter New Quantity: "))

                if new_price <= 0 or new_quantity < 0:
                    print("Invalid values!")
                    return

                p["price"] = str(new_price)
                p["quantity"] = str(new_quantity)

                save_products(products)
                print("Product updated successfully!")
                return

            except ValueError:
                print("Enter valid numbers!")
                return

    print("Product not found!")


# Delete product
def delete_product():
    products = load_products()
    product_id = input("Enter Product ID to delete: ").strip()

    updated_products = [
        p for p in products if p["product_id"] != product_id
    ]

    if len(updated_products) == len(products):
        print("Product not found!")
        return

    save_products(updated_products)
    print("Product deleted successfully!")


# Generate customer bill
def generate_bill():
    products = load_products()
    bill_items = []
    grand_total = 0

    if not products:
        print("No products available!")
        return

    bill_id = "B" + datetime.now().strftime("%Y%m%d%H%M%S")

    while True:
        product_id = input(
            "\nEnter Product ID (or type done): "
        ).strip()

        if product_id.lower() == "done":
            break

        found = False

        for p in products:
            if p["product_id"] == product_id:
                found = True

                try:
                    quantity = int(input("Enter Quantity: "))

                    if quantity <= 0:
                        print("Quantity must be positive!")
                        break

                    stock = int(p["quantity"])

                    if quantity > stock:
                        print("Insufficient stock!")
                        break

                    price = float(p["price"])
                    total = price * quantity

                    p["quantity"] = str(stock - quantity)

                    bill_items.append({
                        "product_id": p["product_id"],
                        "product_name": p["name"],
                        "quantity": quantity,
                        "unit_price": price,
                        "total": total
                    })

                    grand_total += total
                    print("Product added to bill!")

                except ValueError:
                    print("Enter a valid quantity!")

                break

        if not found:
            print("Product not found!")

    if not bill_items:
        print("No items added. Bill cancelled!")
        return

    # Save updated stock
    save_products(products)

    # Save sales records
    with open(SALES_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        for item in bill_items:
            writer.writerow([
                bill_id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                item["product_id"],
                item["product_name"],
                item["quantity"],
                item["unit_price"],
                item["total"]
            ])

    print("\n============= CUSTOMER BILL =============")
    print("Bill ID:", bill_id)
    print("-" * 45)

    for item in bill_items:
        print(
            item["product_name"],
            "x", item["quantity"],
            "=", round(item["total"], 2)
        )

    print("-" * 45)
    print("Grand Total: Rs.", round(grand_total, 2))
    print("Thank you for shopping!")
    print("==========================================")


# Low stock alert

def low_stock_alert():
    products = load_products()
    print("\n----------- LOW STOCK PRODUCTS -----------")

    found = False

    for p in products:
        if int(p["quantity"]) <= 5:
            print(p["name"], "- Remaining:", p["quantity"])
            found = True

    if not found:
        print("All products have sufficient stock!")


# Sales report
def sales_report():
    with open(SALES_FILE, "r", newline="") as file:
        sales = list(csv.DictReader(file))

    if not sales:
        print("No sales records available!")
        return

    total_sales = sum(float(s["total"]) for s in sales)
    total_items = sum(int(s["quantity"]) for s in sales)
    total_bills = len(set(s["bill_id"] for s in sales))

    print("\n=========== SALES REPORT ===========")
    print("Total Bills:", total_bills)
    print("Items Sold:", total_items)
    print("Total Revenue: Rs.", round(total_sales, 2))
    print("====================================")


# Main menu
def main():
    create_files()

    while True:
        print("\n===================================")
        print(" SMART SHOP INVENTORY SYSTEM")
        print("===================================")
        print("1. Add Product")
        print("2. View Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Generate Customer Bill")
        print("7. Low Stock Alert")
        print("8. Sales Report")
        print("9. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            search_product()
        elif choice == "4":
            update_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            generate_bill()
        elif choice == "7":
            low_stock_alert()
        elif choice == "8":
            sales_report()
        elif choice == "9":
            print("Thank you for using Smart Inventory!")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
