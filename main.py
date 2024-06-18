from load_data import load_data

all_data = load_data()
ships = all_data["data"]


def print_help():
    """Prints the help message listing available commands."""
    print("Available commands:")
    print("help")
    print("show_countries")
    print("top_countries <num_countries>")
    print("ships_by_types")

def ships_by_types():
    """Displays the count of ships by their types."""

    ship_types_count = {}
    for ship in ships: 
        ship_type = ship["TYPE_SUMMARY"]
        if ship in ship_types_count:
            ship_types_count[ship_type] += 1
        else:
            ship_types_count[ship_type] = 1

    sorted_ship_types = sorted(ship_types_count.items(), key=lambda x: x[1], reverse=True)
    for ship_type, count in sorted_ship_types:
        print(f"{ship_type}: {count}")   

def show_countries():
    """Prints the list of countries without duplicates, ordered alphabetically."""
    countries = sorted(set(ship["COUNTRY"] for ship in ships))
    for country in countries:
        print(country)
    


def top_countries(num_countries):
    """Prints the top countries by the number of ships."""
    country_counts = {}
    for ship in ships:
        country = ship["COUNTRY"]
        if country in country_counts:
            country_counts[country] += 1
        else:
            country_counts[country] = 1

    sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
    for country, count in sorted_countries[:num_countries]:
        print(f"{country}: {count}")


dispatch = {
    "help": print_help,
    "show_countries": show_countries,
    "top_countries": top_countries,
    "ships_by_types": ships_by_types,
    "exit": None,
}


def main():
    """Main function to run the Ships CLI."""

    print("Welcome to the Ships CLI! Enter 'help' to view available commands.")
    while True:
        command_input = input("py# ").strip().lower()
        if not command_input:
            continue

        parts = command_input.split()
        command = parts[0]

        if command in dispatch:
            if command == "top_countries":
                if len(parts) == 2:
                    try:
                        num_countries = int(parts[1])
                        dispatch[command](num_countries)
                    except ValueError:
                        print("Error: Please provide a valid number for top_countries.")
                else:
                    print("Usage: top_countries <num_countries>")
            elif command == "exit":
                print("Exiting the Ships CLI. Goodbye!")
                break
            else:
                dispatch[command]()
        else:
            print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
