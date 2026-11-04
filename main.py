inventory = {"Titos Vodka": 20.00, "Ketel One Vodka": 24.00, "Espolon Tequila": 25.00}

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
    print("\n--- Harpers Bar Menu ---")
    print("1. View Inventory")
    print("2. Restock Bottle")
    print("3. Record a day's sale")
    print("4. Inventory Comparison ")
    print("5. Flag when inventory vs sales are different")
    print("6. Pour cost reports with charts")
    print("7. Run 30-day simulation")
    print("8. Save and exit")


running = True

while running:
    show_menu()
    choice = input("Choose an option (1-8): ")

    if choice == "1":
        print("\nComing soon")
    elif choice == "2":
        print("\Coming soon")
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
