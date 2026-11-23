# Harper's Bar data: loads and saves the CSV files, and views, restocks, and records sales

POUR_OZ = 1.5   # ounces in one drink
BOTTLE_OZ = 25.36   # ounces in one 750 ml bottle

inventory = {}
sales = []
counts = []

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

# Reads inventory_counts.csv into the counts list, one dictionary per bottle per day
def load_counts():
    with open("inventory_counts.csv", "r") as file:
        file.readline()
        for line in file:
            parts = line.strip().split(",")
            count = {"date": parts[0],
                     "item": parts[1],
                     "oz_start": float(parts[2]),
                     "oz_end": float(parts[3])}
            counts.append(count)

# Writes the counts list back to inventory_counts.csv
def save_counts():
    with open("inventory_counts.csv", "w") as file:
        file.write("date,item,oz_start,oz_end\n")
        for count in counts:
            file.write(count["date"] + "," + count["item"] + "," +
                       str(count["oz_start"]) + "," + str(count["oz_end"]) + "\n")

# Keeps asking until the user types a number (like 12 or 12.50), then returns it
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

# Records a sale and that day's ending count, and updates the ounces on hand
def record_sale():
    date = input("Date (YYYY-MM-DD): ")
    if date == "":
        print("Date cannot be blank.")
        return

    name = input("Bottle name: ").strip()
    item = find_item(name)
    if item == "":
        print(name, "is not in the inventory.")
        return

    for sale in sales:
        if sale["date"] == date and sale["item"] == item:
            print(item, "already has a sale recorded on", date)
            return

    pour_type = input("Pour type (free pour or jigger): ").lower()
    if pour_type != "free pour" and pour_type != "jigger":
        print("Pour type must be free pour or jigger.")
        return

    drinks_sold = get_whole_number("Drinks sold: ")

    oz_start = inventory[item]["oz_on_hand"]
    if drinks_sold * POUR_OZ > oz_start:
        print("Not enough", item, "on hand. Only", oz_start, "ounces left.")
        return

    print("Ounces at start of day:", oz_start)
    oz_end = get_number("Ounces left at end of day: ")
    if oz_end > oz_start:
        print("Ending ounces cannot be more than", oz_start)
        return

    total_price = round(drinks_sold * inventory[item]["drink_price"], 2)
    inventory[item]["oz_on_hand"] = oz_end

    sale = {"date": date, "item": item, "pour_type": pour_type,
            "drinks_sold": drinks_sold, "total_price": total_price}
    sales.append(sale)

    count = {"date": date, "item": item, "oz_start": oz_start, "oz_end": oz_end}
    counts.append(count)

    print("Sale recorded:", drinks_sold, item, "drinks for $", total_price)
    print(item, "ounces used:", round(oz_start - oz_end, 2),
          "(should be", drinks_sold * POUR_OZ, ")")
    print(item, "ounces on hand:", inventory[item]["oz_on_hand"])

# Prints each bottle with its cost, drink price, and ounces on hand
def view_inventory():
    print("\n--- Current Inventory ---")
    for item in inventory:
        print(item)
        print("Bottle cost: $", inventory[item]["bottle_cost"])
        print("Drink price: $", inventory[item]["drink_price"])
        print("Ounces on hand:", inventory[item]["oz_on_hand"])


# Restocks a bottle that already exists, or adds a new bottle with its details
def add_or_restock():
    name = input("Enter the bottle name: ").strip()
    if name == "":
        print("Bottle name cannot be blank.")
        return

    item = find_item(name)
    if item != "":
        print(item, "- bottle cost: $", inventory[item]["bottle_cost"],
              "drink price: $", inventory[item]["drink_price"])
        bottles = get_whole_number("How many bottles are you adding? ")
        if bottles == 0:
            print("Bottles added must be more than 0.")
            return
        ounces = round(bottles * BOTTLE_OZ, 2)
        cost = round(bottles * inventory[item]["bottle_cost"], 2)
        inventory[item]["oz_on_hand"] = round(inventory[item]["oz_on_hand"] + ounces, 2)
        print(item, "restocked with", bottles, "bottles (", ounces, "oz ) for $", cost)
        print("Ounces on hand:", inventory[item]["oz_on_hand"])
    else:
        print(name, "is a new bottle.")
        bottle_cost = get_number("Bottle cost: $")
        drink_price = get_number("Drink price: $")
        bottles = get_whole_number("How many bottles are you adding? ")
        ounces = round(bottles * BOTTLE_OZ, 2)
        inventory[name] = {"bottle_cost": bottle_cost, "drink_price": drink_price, "oz_on_hand": ounces}
        print(name, "added to inventory with", ounces, "ounces.")

# Finds a bottle in the inventory even if the capital letters are different
# and returns its name, or "" if it is not in the inventory
def find_item(name):
    for item in inventory:
        if item.lower() == name.lower():
            return item
    return ""

