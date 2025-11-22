
"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: 20240620/w2181893
 4. Date: 2024/11/12
****************************************************************************
"""

from graphics import *
import csv
import math

# variables
results = {}                  # dictionary to hold analysis results
data_list = []                # list to store CSV rows
destination_count = {}        # dictionary to count destinations
airportcode = ""              # user input airport code
year = 0                      # user input year
selected_data_file = ""       # filename of CSV
airlines_in_csv = set()       # airlines in loaded CSV
valid_airline_entered = False # flag for histogram input
airline_code = ""             # user input airline code

# Airport and airline data from tables 2 and 3 as of in specification
VALID_AIRPORTS = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Adolfo Suárez-Barajas", 
    "CDG": "Charles De Gaulle International",
    "IST": "Istanbul Airport International",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Portela",
    "FRA": "Frankfurt Main",
    "FCO": "Rome Fiumicino",
    "MUC": "Munich International",
    "BCN": "Barcelona International"
}

VALID_AIRLINES = {
    "BA": "British Airways",
    "AF": "Air France",
    "AY": "Finnair", 
    "KL": "KLM",
    "SK": "Scandinavian Airlines",
    "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines",
    "W6": "Wizz Air",
    "U2": "easyJet",
    "FR": "Ryanair",
    "A3": "Aegean Airlines",
    "SN": "Brussels Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "IB": "Iberia",
    "LH": "Lufthansa"
}

def load_csv(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list"
    This function was given in the coursework specification
    """
    with open(CSV_chosen, 'r') as file:  
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)

def airportcode_validate():
    """
    This function prompts the user to enter an airport code and validates it against the VALID_AIRPORTS dictionary
    """
    while True:
        airportcode = input("Please enter a three-letter city code: ").strip().upper()

        # Check if airportcode is valid
        if airportcode in VALID_AIRPORTS:
            return airportcode  
        else:
            print("Invalid airport code. Please try again.")

def year_validate():
    """
    This function prompts the user to enter a year and validates it to ensure it is a four-digit number and is in range of 2000-2025.
    """
    while True:
        year = input("Please enter the year required in the format YYYY: ").strip()

        # Check if input is a 4-digit number
        if year.isdigit() and len(year) == 4:
            year_int = int(year)

        # Check if within valid range
            if 2000 <= year_int <= 2025:
                return year_int
            else:
                print("Invalid year. Please enter a year between 2000 and 2025.")
        else:
            print("Invalid format. Please enter a four-digit year in digits.")

def validate_airline_code():
    """
    This function validate airline code for histogram using specification tables
    """
    while True:
        airlinecode = input("Enter a two-character Airline code to plot a histogram: ").strip().upper()
        
        #checking if the airline code is in the VALID_AIRLINES dictionary
        if airlinecode not in VALID_AIRLINES:
            print("Unavailable Airline code please try again.")
            continue
            
        return airlinecode
    
def get_airlines_from_data():
    """
    This function extract airline codes that actually exist in the loaded csv
    """
    airlines_in_csv = set() #Use of a set to avoid duplicate airline codes
    for row in data_list:
        flight_num = row[1] 
        if flight_num and len(flight_num) >= 2:
            airline_code = flight_num[:2] # The first 2 letters are airline code 
            airlines_in_csv.add(airline_code)
    return airlines_in_csv

def analyze_data(airportcode, year):
    """
    This function analyze the data from data_list and calculate all required outcomes to on dictionary 'results'
    """

    # 1: Total number of departure flights
    results['total_departure_flights'] = len(data_list)

    # 2: Total number of flights departing from terminal 2
    results['departure_terminal_2'] = sum(1 for row in data_list if row[8]=='2')
    
    # 3: Total number of departures of flights that are under 600 miles
    results['under_600_miles'] = sum(1 for row in data_list if row[5].isdigit() and int(row[5]) < 600)  

    # 4: Total number of departure flights by Air France aircraft
    results['air_france_flights'] = sum(1 for row in data_list if row[1].startswith('AF'))

    # 5: Total number of flights departing in temperatures below 15C
    results['flights_below_15c'] = 0
    for row in data_list:
        try:
            # Remove degree symbol and whitespace
            temp_str = row[10].split('°')[0].strip()
            # Convert to float
            temp_val = float(''.join(c for c in temp_str if c.isdigit() or c == '.'))  # ignore weird chars but allow decimal point
            if temp_val < 15:
                results['flights_below_15c'] += 1
        except (ValueError, IndexError):
            continue  

    # 6: Average number of British Airways departures per hour (rounded to two decimal places)
    ba_flights = sum(1 for row in data_list if row[1].startswith('BA'))
    results['British_Airway_Flights_per_hour'] = round(ba_flights / 12, 2) 

    # 7: Percentage of British Airways flights
    results['British_Airway_Flights_percentage'] = round((ba_flights / results['total_departure_flights']) * 100, 2)

    # 8: Percentage of Air France flights with a delayed departure (rounded to two decimal places)
    if results['air_france_flights'] > 0:  #To avoid division by zero
        delayed_af = sum(1 for row in data_list if row[1].startswith('AF') and row[3] != row[2])
        results['AirFrance_delayed_percentage'] = round((delayed_af / results['air_france_flights']) * 100, 2) 
    else:
        results['AirFrance_delayed_percentage'] = 0  

    # 9: Total number of hours of rain in the twelve hours (rain values are recorded once every hour).
    rain_hours = set()#Use of a set to avoid duplicate rain hours
    for row in data_list:
        weather = row[10].lower()
        if 'rain' in weather:
            hour = int(row[2].split(':')[0])
            rain_hours.add(hour)

    results['rain_hours'] = len(rain_hours)

    # 10: Full name of the least common destination (or names if more than one).
    for row in data_list:
        destination_code = row[4]
        destination_name = VALID_AIRPORTS.get(destination_code, destination_code)
        destination_count[destination_name] = destination_count.get(destination_name, 0) + 1
    
    #Checking least common destination(s)
    if destination_count:
        min_count = min(destination_count.values())
        least_common = [name for name, count in destination_count.items() if count == min_count]
        results['least_common_destinations'] = least_common
    else:
        results['least_common_destinations'] = []

def display_results(airportcode, year, results):
    """
    This function displays the formated results  
    """   

    #Filename creation
    airport_name = VALID_AIRPORTS[airportcode]
    filename = f"{airportcode}{year}.csv"

    #Displaying the header
    Maintext=(f"{airportcode}{year}.csv selected - Planes departing {VALID_AIRPORTS[airportcode]} {year}") 
    print("*"*len(Maintext)) 
    print(Maintext) 
    print("*"*len(Maintext)) 

    #Displaying the results
    print(f"The total number of flights from this airport was {results['total_departure_flights']}")
    print(f"The total number of flights departing Terminal Two was {results['departure_terminal_2']}")
    print(f"The total number of departures on flights under 600 miles was {results['under_600_miles']}")
    print(f"There were {results['air_france_flights']} Air France flights from this airport")
    print(f"There were {results['flights_below_15c']} flights departing in temperatures below 15 degrees")
    print(f"There was an average of {results['British_Airway_Flights_per_hour']} British Airways flights per hour from this airport")
    print(f"British Airways planes made up {results['British_Airway_Flights_percentage']}% of all departures")
    print(f"{results['AirFrance_delayed_percentage']}% of Air France departures were delayed")
    print(f"There were {results['rain_hours']} hours in which rain fell")
    print(f"The least common destination(s) are {results['least_common_destinations']}")

def save_results_to_csv(airportcode, year, results):
    """
    This function saves the results to a CSV file
    """
    # Appending results to results.txt file

    #Writing the header
    Maintext = f"{airportcode}{year}.csv selected - Planes departing {VALID_AIRPORTS[airportcode]} {year}"
    border = "*" * len(Maintext)

    with open("results.txt", "a") as f:  
        f.write(border + "\n")
        f.write(Maintext + "\n")
        f.write(border + "\n")
    
        f.write(f"The total number of flights from this airport was {results['total_departure_flights']}\n")
        f.write(f"The total number of flights departing Terminal Two was {results['departure_terminal_2']}\n")
        f.write(f"The total number of departures on flights under 600 miles was {results['under_600_miles']}\n")
        f.write(f"There were {results['air_france_flights']} Air France flights from this airport\n")
        f.write(f"There were {results['flights_below_15c']} flights departing in temperatures below 15 degrees\n")
        f.write(f"There was an average of {results['British_Airway_Flights_per_hour']} British Airways flights per hour from this airport\n")
        f.write(f"British Airways planes made up {results['British_Airway_Flights_percentage']}% of all departures\n")
        f.write(f"{results['AirFrance_delayed_percentage']}% of Air France departures were delayed\n")
        f.write(f"There were {results['rain_hours']} hours in which rain fell\n")
        f.write(f"The least common destination(s) are {results['least_common_destinations']}\n\n")
        f.write("\n")

def plot_airline_histogram(airline_code, airportcode, year):
    """
    This Function plots a horizontal histogram of total departing flights per hour

    Reference for Assistance
    1.  The histogram plotting functionality using graphics.py in this program 
        was implemented with guidance and explanation provided by ChatGPT, 
        an AI language model by OpenAI.
    """
    
    # Importing graphics.py
    from graphics import GraphWin, Rectangle, Text, Point

    # Get full airline and airport names
    airline_name = VALID_AIRLINES.get(airline_code, airline_code)
    airport_name = VALID_AIRPORTS.get(airportcode, airportcode)

    # counting the number of flights per hour
    flights_per_hour = [0] * 12 #creating a list with 12 zeros for each hourspo
    for row in data_list:
        if row[1].startswith(airline_code):
            hour=int(row[2].split(":")[0]) #Get the departure hour
            if 0 <= hour <=12:
                flights_per_hour[hour] += 1
    
    # Setting up the graphics window
    width, height = 1000, 850
    win = GraphWin(f"{airline_name} Histogram", width, height)
    win.setBackground("white")


    #Open Graph on foreground
    win.autoflush=True
    win.master.attributes('-topmost', True) #Keeping the window on top

    #Creating the title 

    #Defining the title text
    title_text = f"Departures by hour for {airline_name} from {airport_name} {year}"
    title=Text(Point(width/2,30), title_text)
    title.setSize(16)
    title.setStyle("bold")

    
    title.draw(win)#Drawing the title

    # Bar setup
    max_flights = max(flights_per_hour)
    if max_flights == 0:
        max_flights = 1  # To avoid division by zero

    # Defining bar parameters
    bar_height = 30
    spacing = 15
    x_offset = 150  
    y_offset = 80
    max_bar_length = width - x_offset - 100  # (1000 - 150 - 100 = 750) leave space for flight numbers

    for i, flights in enumerate(flights_per_hour):
        # scale bar length based on max flights
        bar_length = (flights / max_flights) * max_bar_length if max_flights > 0 else 0
        y_pos = y_offset + i * (bar_height + spacing)

        # draw the bar
        bar = Rectangle(Point(x_offset, y_pos), Point(x_offset + bar_length, y_pos + bar_height))
        bar.setFill("pink")
        bar.setOutline("black")
        bar.draw(win)

        # hour label (on left side)
        hour_label = Text(Point(x_offset - 40, y_pos + bar_height / 2), f"{i}:00")
        hour_label.setSize(12)
        hour_label.draw(win)

        # flight count (at end of bar)
        flights_label = Text(Point(x_offset + bar_length + 20, y_pos + bar_height / 2), str(flights))
        flights_label.setSize(12)
        flights_label.draw(win)

    # X-axis label
    x_label = Text(Point(width / 2, height - 30), "Number of Departing Flights")
    x_label.setSize(12)
    x_label.draw(win)

    # Y-axis labels

    center_y = height/2  # middle of window (425)

    y_label1 = Text(Point(50, center_y - 55), "Hours")
    y_label1.setSize(12)
    y_label1.setStyle("bold")
    y_label1.draw(win)

    y_label2 = Text(Point(50, center_y - 20), "00:00")
    y_label2.setSize(12)
    y_label2.draw(win)

    y_label3 = Text(Point(50, center_y + 10), "to")
    y_label3.setSize(12)
    y_label3.draw(win)

    y_label4 = Text(Point(50, center_y + 40), "12:00")
    y_label4.setSize(12)
    y_label4.draw(win)

    # Wait for user to click before closing
    try:
        win.getMouse()  
    except GraphicsError: 
        pass

    win.close()

def main():
    """
    This function is the main function and call other functions to perform tasks A to E
    """
    
    while True:
        # Task A: Input validation and file loading
        airportcode = airportcode_validate()
        year = year_validate()
        
        # Create filename and load data
        selected_data_file = f"{airportcode}{year}.csv"

        #Input validation for file existence
        try:
            load_csv(selected_data_file)
        except FileNotFoundError:
            print(f"Error: File {selected_data_file} not found. Please check the file exists.")
            continue
        
        # Check if data was loaded successfully
        if not data_list:
            print("Error: No data loaded from file or file is empty.")
            continue
        
        # Task B: Analyze data and display results
        analyze_data(airportcode, year)
        display_results(airportcode, year, results)
        
        # Task C: Save results to file
        save_results_to_csv(airportcode, year, results)
        print("\nResults saved to results.txt")
        
        # Task D: Histogram
        airlines_in_csv = get_airlines_from_data() #Get airlines present in the loaded csv
        valid_airline_entered = False #To create a loop for valid airline code entry
        
        while not valid_airline_entered:
            airline_code = validate_airline_code()
            if airline_code in airlines_in_csv:
                valid_airline_entered = True #Exit loop and print the histogram
                plot_airline_histogram(airline_code, airportcode, year)
            else:
                print(f"No flights found for {VALID_AIRLINES[airline_code]} in this dataset. Please try another airline.")
        
        # Task E: Program loop
        while True:
            continue_choice = input("\nDo you want to select a new data file? Y/N: ").strip().upper()
            if continue_choice in ['Y', 'N']:
                break
            print("Please enter Y or N")
        
        if continue_choice == 'N':
            print("End of run")
            break

if __name__ == "__main__":
    main() 
    