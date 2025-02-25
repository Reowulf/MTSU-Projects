// DAC due date extension 
// PROGRAMMER: Raymond Green
/* Program Description: Program reads from provided city and flight data to create an alphabetized flight map. Then the request data is processed to produce itineraries.*/

#include "type.h"
#include "flightmap.h"
#include <iostream>
#include <string>
using namespace std;

int main() {
    FlightMapClass flightMap;
    
    ifstream citiesFile("cities.dat");
    ifstream flightsFile("flights.dat");
    ifstream requestsFile("requests.dat");
    
    if (!citiesFile.is_open() || !flightsFile.is_open()) {
        cerr<< "Error opening files."<< endl;
        return 1;
    }

    flightMap.readCities(citiesFile);
    flightMap.BuildMap(flightsFile);

    citiesFile.close();
    flightsFile.close();

    string origin, destination;
    cout << "Processing flight requests:" << endl;
    while (requestsFile >> origin >> destination) {
        cout << "Request is to fly from " << origin << " to " << destination << "." << endl;
        (flightMap.FindPath(origin, destination));

    requestsFile.close();
    return 0;
    }
}