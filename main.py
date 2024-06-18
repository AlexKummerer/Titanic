import sys
from load_data import load_data

all_data = load_data()
print(all_data.keys())

print(all_data['totalCount'])

def print_help():
    print("Available commands:") 
    print("help")
    print("show_countries")
    print("top_countries <num_countries>")


def main():
    print("Welcome to the Ships CLI! Enter 'help' to view available commands.")
    input_user = input()
    help = print_help
    if input_user == "help":
        help()
    
    
    
if __name__ == '__main__':
    main()
        