import sys
from load_data import load_data

all_data = load_data()
ships = all_data["data"]


def print_help():
    """Prints the help message listing available commands."""
    print("Available commands:")
    print("help")
    print("show_countries")
    print("top_countries <num_countries>")


def show_countries():
    """Prints the list of countries without duplicates, ordered alphabetically."""
    countries = sorted(set(ship["COUNTRY"] for ship in ships))
    for country in countries:
        print(country)
    7


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


def main():
    """Main function to run the Ships CLI."""

    print("Welcome to the Ships CLI! Enter 'help' to view available commands.")
    while True:
        command = input("py# ").strip().lower()
        if command == "help":
            print_help()
        elif command == "show_countries":
            show_countries()
        elif command.startswith("top_countries"):
            try:
                num_countries = int(command.split()[1])
                top_countries(num_countries)
            except (IndexError, ValueError):
                print("Error: Please provide a valid number for top_countries.")
        elif command == "exit":
            print("Exiting the Ships CLI. Goodbye!")
            break
        else:
            print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
