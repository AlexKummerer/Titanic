from load_data import load_data
import matplotlib.pyplot as plt
import geopandas as gpd
from geodatasets import get_path


all_data: dict[str, list[dict[str, str]]] = load_data()
ships: list[dict[str, str]] = all_data["data"]

def draw_map():
    """Draw the ships on a world map using their location data."""
    lons: list[float] = [float(ship["LON"]) for ship in ships if ship["LON"]]
    lats: list[float] = [float(ship["LAT"]) for ship in ships if ship["LAT"]]
    names: list[str] = [ship["SHIPNAME"] for ship in ships]

    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    gdf = gpd.GeoDataFrame(
        {"Name": names, "Longitude": lons, "Latitude": lats},
        geometry=gpd.points_from_xy(lons, lats),
    )

    # Initialize the map plot
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color='lightgrey')
    

    # Plot the ship locations
    gdf.plot(ax=ax, color='red', markersize=50, alpha=0.6, edgecolor='black')    
    
    
    plt.title("Ship Locations on World Map")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Save the plot to a file
    plt.savefig("ship_locations_map.png")
    plt.show()


def print_help() -> None:
    """Prints the help message listing available commands."""
    print("Available commands:")
    print("help")
    print("show_countries")
    print("top_countries <num_countries>")
    print("ships_by_types")
    print("search_ship <name>")
    print("speed_histogram")
    print("draw_map")


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
    "draw_map": draw_map,
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
