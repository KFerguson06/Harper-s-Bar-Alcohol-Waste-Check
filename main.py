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


running = True

while running:
    show_menu()
    choice = input("Choose an option (1-8): ")

    if choice == "1":
        view_inventory()
    elif choice == "2":
        add_or_restock()
    elif choice == "3":
        print("\nComing soon")
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
