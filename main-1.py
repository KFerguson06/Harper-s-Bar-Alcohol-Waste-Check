POUR_OZ = 1.5   # ounces in one drink
BOTTLE_OZ = 25.36   # ounces in one 750 ml bottle
FLAG_PERCENT = 10   # flag a day when the liquor used is off by more than 10%

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

# Matches each day's inventory count with that day's sales for the same bottle
# and returns a list with one dictionary per bottle per day
def build_comparison():
    comparison = []
    for count in counts:
        item = count["item"]
        drinks_sold = 0
        revenue = 0
        pour_type = ""
        for sale in sales:
            if sale["date"] == count["date"] and sale["item"] == item:
                drinks_sold = drinks_sold + sale["drinks_sold"]
                revenue = revenue + sale["total_price"]
                pour_type = sale["pour_type"]

        if pour_type != "" and item in inventory:
            oz_used = round(count["oz_start"] - count["oz_end"], 2)
            oz_expected = drinks_sold * POUR_OZ
            cost_per_oz = inventory[item]["bottle_cost"] / BOTTLE_OZ
            row = {"date": count["date"],
                   "item": item,
                   "pour_type": pour_type,
                   "drinks_sold": drinks_sold,
                   "oz_expected": oz_expected,
                   "oz_used": oz_used,
                   "oz_extra": round(oz_used - oz_expected, 2),
                   "liquor_cost": round(oz_used * cost_per_oz, 2),
                   "revenue": round(revenue, 2)}
            comparison.append(row)
    return comparison

# Adds up the comparison rows for each group, such as each bottle or each pour type
def group_totals(comparison, field):
    groups = {}
    for row in comparison:
        key = row[field]
        if key not in groups:
            groups[key] = {"drinks_sold": 0, "oz_expected": 0, "oz_used": 0,
                           "liquor_cost": 0, "revenue": 0}
        for total in groups[key]:
            groups[key][total] = groups[key][total] + row[total]
    return groups

# Returns pour cost as a percent: what the liquor cost divided by what it sold for
def pour_cost(liquor_cost, revenue):
    if revenue == 0:
        return 0
    return round(liquor_cost / revenue * 100, 1)

# Returns the average ounces poured in each drink
def oz_per_drink(oz_used, drinks_sold):
    if drinks_sold == 0:
        return 0
    return round(oz_used / drinks_sold, 2)

# Shows how many ounces each bottle should have used compared to how many it did use
def inventory_comparison():
    comparison = build_comparison()
    if len(comparison) == 0:
        print("\nNo inventory counts match your sales yet.")
        return

    by_item = group_totals(comparison, "item")
    print("\n--- Inventory Comparison ---")
    for item in by_item:
        totals = by_item[item]
        print(item)
        print("   Drinks sold:     ", totals["drinks_sold"])
        print("   Ounces expected: ", round(totals["oz_expected"], 2))
        print("   Ounces used:     ", round(totals["oz_used"], 2))
        print("   Extra ounces:    ", round(totals["oz_used"] - totals["oz_expected"], 2))
        print("   Ounces per drink:", oz_per_drink(totals["oz_used"], totals["drinks_sold"]))

    by_pour = group_totals(comparison, "pour_type")
    print("\nOunces per drink by pour type (should be", POUR_OZ, "):")
    for pour_type in by_pour:
        totals = by_pour[pour_type]
        print("  ", pour_type, oz_per_drink(totals["oz_used"], totals["drinks_sold"]))

# Lists each day a bottle used more or less liquor than its sales say it should have
def flag_differences():
    comparison = build_comparison()
    if len(comparison) == 0:
        print("\nNo inventory counts match your sales yet.")
        return

    print("\n--- Flagged Days (off by more than", FLAG_PERCENT, "percent) ---")
    flags = 0
    extra_cost = 0
    flags_by_pour = {}
    for row in comparison:
        percent_off = 0
        if row["oz_expected"] > 0:
            percent_off = row["oz_extra"] / row["oz_expected"] * 100
        elif row["oz_used"] > 0:
            percent_off = 100

        if percent_off > FLAG_PERCENT or percent_off < -FLAG_PERCENT:
            flags = flags + 1
            cost_per_oz = inventory[row["item"]]["bottle_cost"] / BOTTLE_OZ
            cost = round(row["oz_extra"] * cost_per_oz, 2)
            extra_cost = extra_cost + cost

            pour_type = row["pour_type"]
            if pour_type not in flags_by_pour:
                flags_by_pour[pour_type] = 0
            flags_by_pour[pour_type] = flags_by_pour[pour_type] + 1

            if percent_off > 0:
                problem = "OVER"
            else:
                problem = "UNDER"
            print(row["date"], row["item"], "(" + pour_type + ")", problem, "by",
                  row["oz_extra"], "oz, cost $", cost)

    if flags == 0:
        print("No days were flagged. Inventory matches sales.")
        return

    print("\nDays checked:  ", len(comparison))
    print("Days flagged:  ", flags)
    print("Cost of extra liquor: $", round(extra_cost, 2))
    print("Flags by pour type:")
    for pour_type in flags_by_pour:
        print("  ", pour_type, flags_by_pour[pour_type])

# Prints a summary of sales and pour cost, with totals for each bottle
def pour_cost_report():
    if len(sales) == 0:
        print("\nNo sales recorded yet.")
        return

    total_drinks = 0
    total_revenue = 0
    dates = []
    drinks_by_item = {}
    for sale in sales:
        item = sale["item"]
        total_drinks = total_drinks + sale["drinks_sold"]
        total_revenue = total_revenue + sale["total_price"]
        if sale["date"] not in dates:
            dates.append(sale["date"])
        if item not in drinks_by_item:
            drinks_by_item[item] = 0
        drinks_by_item[item] = drinks_by_item[item] + sale["drinks_sold"]

    best_seller = ""
    best_drinks = 0
    for item in drinks_by_item:
        if drinks_by_item[item] > best_drinks:
            best_seller = item
            best_drinks = drinks_by_item[item]

    print("\n--- Pour Cost Report ---")
    print("Days recorded:       ", len(dates))
    print("Total drinks sold:   ", total_drinks)
    print("Total revenue:        $", round(total_revenue, 2))
    print("Average revenue/day:  $", round(total_revenue / len(dates), 2))
    print("Best seller:         ", best_seller, "(", best_drinks, "drinks )")

    comparison = build_comparison()
    if len(comparison) == 0:
        print("\nNo inventory counts yet, so pour cost cannot be figured.")
        return

    total_cost = 0
    total_counted_revenue = 0
    for row in comparison:
        total_cost = total_cost + row["liquor_cost"]
        total_counted_revenue = total_counted_revenue + row["revenue"]
    print("Total liquor cost:    $", round(total_cost, 2))
    print("Overall pour cost:   ", pour_cost(total_cost, total_counted_revenue), "%")

    by_item = group_totals(comparison, "item")
    worst_item = ""
    worst_cost = 0
    for item in by_item:
        item_cost = pour_cost(by_item[item]["liquor_cost"], by_item[item]["revenue"])
        if item_cost > worst_cost:
            worst_item = item
            worst_cost = item_cost
    print("Highest pour cost:   ", worst_item, "(", worst_cost, "% )")

    by_pour = group_totals(comparison, "pour_type")
    print("\nPour cost by pour type:")
    for pour_type in by_pour:
        totals = by_pour[pour_type]
        print("  ", pour_type, pour_cost(totals["liquor_cost"], totals["revenue"]), "%")

    print("\nTotals by bottle:")
    for item in by_item:
        totals = by_item[item]
        print("  ", item, "- drinks:", totals["drinks_sold"],
              "revenue: $", round(totals["revenue"], 2),
              "pour cost:", pour_cost(totals["liquor_cost"], totals["revenue"]), "%")

load_inventory()
load_sales()
load_counts()

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
        inventory_comparison()
    elif choice == "5":
        flag_differences()
    elif choice == "6":
        pour_cost_report()
    elif choice == "7":
        print("\nComing soon")
    elif choice == "8":
        save_inventory()
        save_sales()
        print("Inventory and sales saved. Goodbye!")
        running = False
    else:
        print("Please enter 1, 2, 3, 4, 5, 6, 7, or 8.")
