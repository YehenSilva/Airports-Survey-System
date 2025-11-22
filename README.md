# Airport Survey System

The **Airport Survey System** is a Python application that allows users to analyze airport flight data from CSV files and visualize airline departures. The system is designed to provide insights into flight patterns, airline activity, and airport operations.

## Features

* **CSV Data Analysis**: Load airport flight data for a selected airport and year.
* **Flight Statistics**:

  * Total departures
  * Departures from Terminal 2
  * Flights under 600 miles
  * Airline-specific departures and delays
  * Flights in temperatures below 15°C
  * Hours with rain
* **Destination Insights**: Identifies least common destinations.
* **Histogram Visualization**: Graphically displays hourly departures for a selected airline using `graphics.py`.
* **Results Logging**: Saves analysis results to a text file (`results.txt`) for record-keeping.

## Technologies Used

* Python 3
* `csv` module for reading CSV data
* `graphics.py` for histogram plotting
* Dictionaries, lists, and sets for efficient data handling

## How to Use

1. Clone the repository.
2. Ensure you have `graphics.py` in the same directory.
3. Prepare CSV files in the format `{AIRPORTCODE}{YEAR}.csv`.
4. Run `python main.py`.
5. Follow prompts to enter:

   * Airport code (e.g., LHR)
   * Year (e.g., 2024)
   * Airline code for histogram (e.g., BA)
6. View results in the console and check `results.txt` for saved summaries.
7. Click on the histogram window to close it after reviewing.

## File Structure

```
Airport-Survey-System/
│
├─ main.py                # Main program with full functionality
├─ graphics.py            # Graphics library for plotting histograms
├─ LHR2024.csv            # Example CSV data file
├─ results.txt            # Generated results file
└─ README.md              # Project description
```

Perfect! You can include the CSV format clearly in your README so users know what data your program expects. Here's an updated **README section** including your CSV format:

---

## CSV File Format

The system expects CSV files in the following structure:

```
AirportCode,FlightNum,ScheduledDepature,ActualDeparture,Destination,Distance miles,ScheduledArrival,ActualArrival,DepartureTerminal,RunwayNum,WeatherConditions
```

* **AirportCode**: 3-letter IATA airport code (e.g., LHR, MAD)
* **FlightNum**: Flight number including airline code (e.g., BA123)
* **ScheduledDepature**: Scheduled departure time (HH:MM)
* **ActualDeparture**: Actual departure time (HH:MM)
* **Destination**: 3-letter IATA code for destination airport
* **Distance miles**: Distance in miles
* **ScheduledArrival**: Scheduled arrival time (HH:MM)
* **ActualArrival**: Actual arrival time (HH:MM)
* **DepartureTerminal**: Terminal number (e.g., 1, 2)
* **RunwayNum**: Runway number used
* **WeatherConditions**: Weather description (e.g., Rain, Cloudy, Clear)

All CSV files should be named using the pattern:

```
<AIRPORTCODE><YEAR>.csv
```

For example: `LHR2024.csv`

---
