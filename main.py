inventory = {"Titos Vodka": {"bottle_cost": 20.00, "drink_price": 8.00, "oz_on_hand": 46.86}, "Ketel One Vodka": {"bottle_cost": 24.00, "drink_price": 10.50, "oz_on_hand": 35.73}, "Espolon Tequila": {"bottle_cost": 25.00, "drink_price": 8.00, "oz_on_hand": 34.36}}

sales = {
    "2026-10-01": {
        "Titos Vodka": 32.00,
        "Ketel One Vodka": 52.50,
        "Espolon Tequila": 48.00 }}

inventory_counts = {
    "2026-10-01": {
        "Titos Vodka": 68.89,
        "Ketel One Vodka": 67.13,
        "Espolon Tequila": 63.75}}


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


running = True

while running:
    show_menu()
    choice = input("Choose an option (1-8): ")

    if choice == "1":
        view_inventory()
    elif choice == "2":
        print("\nComing soon")
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
        print("Goodbye!")
        running = False
    else:
        print("Please enter 1, 2, 3, 4, 5, 6, 7, or 8.")
