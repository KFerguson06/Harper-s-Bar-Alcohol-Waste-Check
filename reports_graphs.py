# Harper's Bar reports: compares inventory to sales, flags differences, and makes the report and charts
import matplotlib.pyplot as plt
import bar

FLAG_PERCENT = 10   # flag a day when the liquor used is off by more than 10%

# Matches each day's inventory count with that day's sales for the same bottle
# and returns a list with one dictionary per bottle per day
def build_comparison():
    comparison = []
    for count in bar.counts:
        item = count["item"]
        drinks_sold = 0
        revenue = 0
        pour_type = ""
        for sale in bar.sales:
            if sale["date"] == count["date"] and sale["item"] == item:
                drinks_sold = drinks_sold + sale["drinks_sold"]
                revenue = revenue + sale["total_price"]
                pour_type = sale["pour_type"]

        if pour_type != "" and item in bar.inventory:
            oz_used = round(count["oz_start"] - count["oz_end"], 2)
            oz_expected = drinks_sold * bar.POUR_OZ
            cost_per_oz = bar.inventory[item]["bottle_cost"] / bar.BOTTLE_OZ
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
    print("\nOunces per drink by pour type (should be", bar.POUR_OZ, "):")
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
            cost_per_oz = bar.inventory[row["item"]]["bottle_cost"] / bar.BOTTLE_OZ
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
    if len(bar.sales) == 0:
        print("\nNo sales recorded yet.")
        return

    total_drinks = 0
    total_revenue = 0
    dates = []
    drinks_by_item = {}
    for sale in bar.sales:
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

# Returns only the comparison rows for one pour type, such as "jigger"
def filter_pour_type(comparison, pour_type):
    rows = []
    for row in comparison:
        if row["pour_type"] == pour_type:
            rows.append(row)
    return rows

# Draws and saves two charts that compare free pour and jigger
def pour_cost_charts():
    comparison = build_comparison()
    if len(comparison) == 0:
        print("\nNo inventory counts yet, so there is nothing to chart.")
        return

    # Bar chart: pour cost for each bottle, free pour next to jigger
    by_item = group_totals(comparison, "item")
    free_by_item = group_totals(filter_pour_type(comparison, "free pour"), "item")
    jigger_by_item = group_totals(filter_pour_type(comparison, "jigger"), "item")

    names = []
    positions = []
    free_costs = []
    jigger_costs = []
    position = 0
    for item in by_item:
        names.append(item)
        positions.append(position)
        if item in free_by_item:
            free_costs.append(pour_cost(free_by_item[item]["liquor_cost"], free_by_item[item]["revenue"]))
        else:
            free_costs.append(0)
        if item in jigger_by_item:
            jigger_costs.append(pour_cost(jigger_by_item[item]["liquor_cost"], jigger_by_item[item]["revenue"]))
        else:
            jigger_costs.append(0)
        position = position + 1

    free_positions = []
    jigger_positions = []
    for position in positions:
        free_positions.append(position - 0.2)
        jigger_positions.append(position + 0.2)

    plt.figure(figsize=(10, 6))
    plt.bar(free_positions, free_costs, width=0.4, label="Free pour")
    plt.bar(jigger_positions, jigger_costs, width=0.4, label="Jigger")
    plt.xticks(positions, names, rotation=45)
    plt.title("Pour Cost by Bottle: Free Pour vs Jigger")
    plt.xlabel("Bottle")
    plt.ylabel("Pour cost (%)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("pour_cost_by_bottle.png")
    plt.show()

    # Line chart: average ounces poured per drink each day, one line for each pour type
    by_date = group_totals(comparison, "date")
    days = []
    target = []
    for date in by_date:
        days.append(date[5:])
        target.append(bar.POUR_OZ)

    free_by_date = group_totals(filter_pour_type(comparison, "free pour"), "date")
    free_days = []
    free_oz = []
    for date in free_by_date:
        free_days.append(date[5:])
        free_oz.append(oz_per_drink(free_by_date[date]["oz_used"], free_by_date[date]["drinks_sold"]))

    jigger_by_date = group_totals(filter_pour_type(comparison, "jigger"), "date")
    jigger_days = []
    jigger_oz = []
    for date in jigger_by_date:
        jigger_days.append(date[5:])
        jigger_oz.append(oz_per_drink(jigger_by_date[date]["oz_used"], jigger_by_date[date]["drinks_sold"]))

    plt.figure(figsize=(10, 6))
    plt.plot(days, target, linestyle="--", color="gray", label="Target (1.5 oz)")
    plt.plot(free_days, free_oz, marker="o", label="Free pour")
    plt.plot(jigger_days, jigger_oz, marker="o", label="Jigger")
    plt.xticks(rotation=90)
    plt.title("Average Ounces Poured per Drink by Day")
    plt.xlabel("Date")
    plt.ylabel("Ounces per drink")
    plt.legend()
    plt.tight_layout()
    plt.savefig("oz_per_drink_by_day.png")
    plt.show()

    print("\nCharts saved as pour_cost_by_bottle.png and oz_per_drink_by_day.png")

