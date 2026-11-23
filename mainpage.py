# Harper's Bar menu: run this file to start the app
import bar
import reports_graphs

# Prints the menu choices
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

bar.load_inventory()
bar.load_sales()
bar.load_counts()

running = True

while running:
    show_menu()
    choice = input("Choose an option (1-8): ")

    if choice == "1":
        bar.view_inventory()
    elif choice == "2":
        bar.add_or_restock()
    elif choice == "3":
        bar.record_sale()
    elif choice == "4":
        reports_graphs.inventory_comparison()
    elif choice == "5":
        reports_graphs.flag_differences()
    elif choice == "6":
        reports_graphs.pour_cost_report()
        reports_graphs.pour_cost_charts()
    elif choice == "7":
        print("\nComing soon")
    elif choice == "8":
        bar.save_inventory()
        bar.save_sales()
        bar.save_counts()
        print("Inventory, sales, and counts saved. Goodbye!")
        running = False
    else:
        print("Please enter 1, 2, 3, 4, 5, 6, 7, or 8.")
