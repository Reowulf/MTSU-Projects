Flight Map Itinerary Generator
This project is a C++ application that reads data from provided files to build an alphabetized flight map and process flight requests, generating detailed itineraries along with the total travel cost.

Overview
The program reads city and flight data to construct an internal flight map represented with adjacency lists. It then processes flight requests to determine if a path exists between two specified cities. If a valid itinerary is found, the program displays the flight details (flight number, origin, destination, and cost) and computes the total price for the itinerary.

Features
City Data Processing:
	Reads a list of cities from a file and stores them in alphabetical order.

Flight Map Construction:
	Reads flight records (flight number, origin, destination, price) and builds an adjacency list representing the flight connections.

Flight Itinerary Generation:
	Processes flight requests to determine a valid sequence of flights between an origin and a destination city. It marks cities as visited and prints out the complete itinerary along with the total cost.

Custom Flight Record:
	Uses a flightRec structure with overloaded operators for easy comparison and formatted output.

Files:
flightmap.h / flightmap.cpp:
	Contains the definition and implementation of the FlightMapClass that handles reading cities, building the flight map, searching for itineraries, and displaying results.

type.h / type.cpp:
	Define the flightRec structure and implement overloaded operators (<, ==, and <<) for comparing flight records and output formatting.

main.cpp:
	The main driver that reads input files, builds the flight map, and processes flight requests.

Makefile:
	Provides instructions to compile the project.

Data Files:

	cities.dat: Contains the number of cities and the list of city names.
	flights.dat: Contains flight records in the format:
	flightNumber origin destination price
	requests.dat: Contains flight requests with origin and destination city pairs.

Compilation:
Using the Makefile
	make
This will compile all the source files and generate an executable (e.g., flightmap).

Manual Compilation
If you prefer to compile manually, use a command like the following (ensure you have a C++11-compatible compiler):
	g++ -std=c++11 -o flightmap main.cpp flightmap.cpp type.cpp

Running the Program:
Ensure the data files (cities.dat, flights.dat, and requests.dat) are in the same directory as your executable. Run the program using:
	./flightmap
The program will display the flight map and process each flight request, printing the corresponding itinerary if a valid path exists.

Data File Format
	cities.dat:

The first line is an integer indicating the number of cities.
The following lines list one city name per line.

flights.dat:
Each record consists of:
	flightNumber origin destination price

requests.dat:
Each record contains two city names representing the origin and destination for a flight request.

Program Output:
A formatted table of the flight map, displaying flight connections from each origin city.
For each flight request, an itinerary is printed that includes flight details and the total cost of the journey.
If no valid itinerary is found, an appropriate message is displayed.