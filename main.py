POUR_OZ = 1.5   # ounces in one drink

inventory = {}
sales = []

# Reads inventory.csv into the inventory dictionary
def load_inventory():
    with open("inventory.csv", "r") as file:
        file.readline()
        for line in file:
            parts = line.strip().split(",")
            item = parts[0]
            inventory[item] = {"bottle_cost": float(parts[1]),
                               "drink_price": float(parts[2]),
                               "oz_on_hand": float(parts[3])}
            

# Writes the inventory dictionary back to inventory.csv
def save_inventory():
    with open("inventory.csv", "w") as file:
        file.write("item,bottle_cost,drink_price,oz_on_hand\n")
        for item in inventory:
            details = inventory[item]
            file.write(item + "," + str(details["bottle_cost"]) + "," +
                       str(details["drink_price"]) + "," + str(details["oz_on_hand"]) + "\n")

# Reads sales.csv into the sales list, one dictionary per sale
def load_sales():
    with open("sales.csv", "r") as file:
        file.readline()
        for line in file:
            parts = line.strip().split(",")
            sale = {"date": parts[0],
                    "item": parts[1],
                    "pour_type": parts[2],
                    "drinks_sold": int(parts[3]),
                    "total_price": float(parts[4])}
            sales.append(sale)

# Writes the sales list back to sales.csv
def save_sales():
    with open("sales.csv", "w") as file:
        file.write("date,item,pour_type,drinks_sold,total_price\n")
        for sale in sales:
            file.write(sale["date"] + "," + sale["item"] + "," + sale["pour_type"] + "," +
                       str(sale["drinks_sold"]) + "," + str(sale["total_price"]) + "\n")

def show_menu():
    print("\n--- Harper's Bar Menu ---")
    print("1. View Inventory")
    print("2. Restock Bottle")
    print("3. Record a day's sale")
    print("4. Inventory Comparison ")
    print("5. Flag when inventory vs sales are different")
    print("6. Pour cost reports with charts")
    print("7. Run 30-day simulation")
    print("8. Save and exit")

def get_number(prompt):
    answer = input(prompt)
    while not answer.replace(".", "", 1).isdigit():
        print("Please enter a number, like 12 or 12.50.")
        answer = input(prompt)
    return float(answer)

# Keeps asking until the user types a whole number (like 5), then returns it
def get_whole_number(prompt):
    answer = input(prompt)
    while not answer.isdigit():
        print("Please enter a whole number, like 5.")
        answer = input(prompt)
    return int(answer)

# Records a sale, lowers the ounces on hand, and adds the sale to the sales list
def record_sale():
    date = input("Date (YYYY-MM-DD): ")
    if date == "":
        print("Date cannot be blank.")
        return

    item = input("Bottle name: ").strip()
    if item not in inventory:
        print(item, "is not in the inventory.")
        return

    pour_type = input("Pour type (free pour or jigger): ").lower()
    if pour_type != "free pour" and pour_type != "jigger":
        print("Pour type must be free pour or jigger.")
        return

    drinks_sold = get_whole_number("Drinks sold: ")
    if drinks_sold == 0:
        print("Drinks sold must be more than 0.")
        return

    oz_used = drinks_sold * POUR_OZ
    if oz_used > inventory[item]["oz_on_hand"]:
        print("Not enough", item, "on hand. Only", inventory[item]["oz_on_hand"], "ounces left.")
        return

    total_price = round(drinks_sold * inventory[item]["drink_price"], 2)
    inventory[item]["oz_on_hand"] = round(inventory[item]["oz_on_hand"] - oz_used, 2)

    sale = {"date": date, "item": item, "pour_type": pour_type,
            "drinks_sold": drinks_sold, "total_price": total_price}
    sales.append(sale)

    print("Sale recorded:", drinks_sold, item, "drinks for $", total_price)
    print(item, "ounces on hand:", inventory[item]["oz_on_hand"])

def view_inventory():
    print("\n--- Current Inventory ---")
    for item in inventory:
        print(item)
        print("Bottle cost: $", inventory[item]["bottle_cost"])
        print("Drink price: $", inventory[item]["drink_price"])
        print("Ounces on hand:", inventory[item]["oz_on_hand"])


# Restocks a bottle that already exists, or adds a new bottle with its details
def add_or_restock():
    item = input("Enter the bottle name: ")

    if item in inventory:
        ounces = get_number("How many ounces are you adding? ")
        inventory[item]["oz_on_hand"] = inventory[item]["oz_on_hand"] + ounces
        print(item, "restocked. Ounces on hand:", inventory[item]["oz_on_hand"])
    else:
        bottle_cost = get_number("Bottle cost: $")
        drink_price = get_number("Drink price: $")
        ounces = get_number("Ounces on hand: ")
        inventory[item] = {"bottle_cost": bottle_cost, "drink_price": drink_price, "oz_on_hand": ounces}
        print(item, "added to inventory.")

load_inventory()
load_sales()

running = True

while running:
    show_menu()
    choice = input("Choose an option (1-8): ")

    if choice == "1":
        view_inventory()
    elif choice == "2":
        add_or_restock()
    elif choice == "3":
        record_sale()
    elif choice == "4":
        print("\nComing soon")
    elif choice == "5":
        print("\nComing soon")
    elif choice == "6":
        print("\nComing soon")
    elif choice == "7":
        print("\nComing soon")
    elif choice == "8":
        save_inventory()
        save_sales()
        print("Inventory and sales saved. Goodbye!")
        running = False
    else:
        print("Please enter 1, 2, 3, 4, 5, 6, 7, or 8.")
