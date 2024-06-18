from load_data import load_data
import matplotlib.pyplot as plt

all_data: dict[str, list[dict[str, str]]] = load_data()
ships: list[dict[str, str]] = all_data["data"]


def print_help() -> None:
    """Prints the help message listing available commands."""
    print("Available commands:")
    print("help")
    print("show_countries")
    print("top_countries <num_countries>")
    print("ships_by_types")
    print("search_ship <name>")
    print("speed_histogram")


def speed_histogram() -> None:
    """Create a histogram of ship speeds and save it to a file."""
    speeds: list[float] = [float(ship["SPEED"]) for ship in ships if ship["SPEED"]]
    plt.hist(speeds, bins=30, edgecolor="green")
    plt.xlabel("Speed")
    plt.ylabel("Number of Ships")
    plt.title("Histogram of Ship Speeds")
    plt.savefig("speed_histogram.png")
    plt.close()
    print("Speed histogram saved to 'speed_histogram.png'.")


def ships_by_types() -> None:
    """Displays the count of ships by their types."""

    ship_types_count: dict[str, int] = {}
    for ship in ships:
        ship_type: str = ship["TYPE_SUMMARY"]
        if ship in ship_types_count:
            ship_types_count[ship_type] += 1
        else:
            ship_types_count[ship_type] = 1

    sorted_ship_types: list[tuple[str, int]] = sorted(
        ship_types_count.items(), key=lambda x: x[1], reverse=True
    )
    for ship_type, count in sorted_ship_types:
        print(f"{ship_type}: {count}")


def search_ship(name: str) -> None:
    """Search for ships by name (case insensitive and partial match)."""
    search_term: str = name.lower()
    found_ships: list[str] = [
        ship["SHIPNAME"] for ship in ships if search_term in ship["SHIPNAME"].lower()
    ]

    if found_ships:
        print("Ships found:")
        for ship_name in found_ships:
            print(ship_name)
    else:
        print("No ships found matching the search term.")


def show_countries():
    """Prints the list of countries without duplicates, ordered alphabetically."""
    countries: list[str] = sorted(set(ship["COUNTRY"] for ship in ships))
    for country in countries:
        print(country)


def top_countries(num_countries):
    """Prints the top countries by the number of ships."""
    country_counts: dict = {}
    for ship in ships:
        country: str = ship["COUNTRY"]
        if country in country_counts:
            country_counts[country] += 1
        else:
            country_counts[country] = 1

    sorted_countries: list[tuple] = sorted(
        country_counts.items(), key=lambda x: x[1], reverse=True
    )
    for country, count in sorted_countries[:num_countries]:
        print(f"{country}: {count}")


dispatch = {
    "help": print_help,
    "show_countries": show_countries,
    "top_countries": top_countries,
    "ships_by_types": ships_by_types,
    "search_ship": search_ship,
    "speed_histogram": speed_histogram,
    "exit": None,
}


def main():
    """Main function to run the Ships CLI."""

    print("Welcome to the Ships CLI! Enter 'help' to view available commands.")
    while True:
        command_input: str = input("py# ").strip().lower()
        if not command_input:
            continue

        parts: list[str] = command_input.split()
        command: str = parts[0]

        if command in dispatch:
            if command == "top_countries":
                if len(parts) == 2:
                    try:
                        num_countries: int = int(parts[1])
                        dispatch[command](num_countries)
                    except ValueError:
                        print("Error: Please provide a valid number for top_countries.")
                else:
                    print("Usage: top_countries <num_countries>")
            elif command == "search_ship":
                if len(parts) == 2:
                    dispatch[command](parts[1])
                else:
                    print("Usage: search_ship <name>")
            elif command == "exit":
                print("Exiting the Ships CLI. Goodbye!")
                break
            else:
                dispatch[command]()
        else:
            print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
