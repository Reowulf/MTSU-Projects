#include "flightmap.h"
#include "type.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <list>
#include <algorithm>
#include <iomanip>
using namespace std;

//Read cities from a data file
//Pre-condition: Input stream is provided
//Post-condition: Data file is read
//				  Cities are in ascending order
void FlightMapClass::readCities(ifstream& fp) {
    string line;
    if (getline(fp, line)) {
        numberOfCities = stoi(line);
    }
    cities.resize(numberOfCities);
    adjList = new list<flightRec>[numberOfCities];
        
    for (int i = 0; i < numberOfCities; ++i) {
        if (getline(fp, cities[i])) {} 
        else {
            cerr<< "Error reading city names from file."<< endl;
            break;
        }
    }
    sort(cities.begin(), cities.end());
}

//Displays the flight map in a formatted table
// using overloaded << opererator
//Pre-condition: none
//Post-condition: Flight map is displayed
ostream& operator<<(ostream& os, const FlightMapClass& fmc) {
    cout<< left<< setw(20)<< "\n    Origin"
        << setw(15) << "Destination"
        << setw(7)<< "Flight"<< setw(8)
        << "   Price\n===================================================\n"<< endl;
    for (int i = 0; i < fmc.numberOfCities; ++i) {
        if (!fmc.adjList[i].empty()){
            os << "From " << fmc.cities[i] << " to:" << endl;
            for (const auto& flight : fmc.adjList[i]) {
                os << setw(20) << " "
                    << setw(15) << flight.destination 
                    << setw(6) << flight.flightNum
                    << setw(6) << right<< "$" << left<< flight.price
                    << endl;
                }
            }
        }
        return os;
    }

// Clears marks on all cities
// Pre-condition: there are > 0 cities in a cities array
// Post-condition: all cities marked as unvisited
void FlightMapClass::UnvisitAll(){
    for (size_t i = 0; i < visited.size(); i++) {
        visited[i] = false;
    }
}

// Determines whether a city was visited
// Pre-condition: city is provided
// Post-condition: return true if city has been visited
//              otherwise return false
bool FlightMapClass::IsVisited(int city) const{
    if (city >= 0 && city < visited.size()) {
        return visited[city];
    } else {
        cerr << "City index out of bounds." << endl;
        return false;
    }
}

// Determines the next unvisited city, if any,
// that is adjacent to a given city.
// success indicates whether an unvisited adjacent city was found
// Pre-condition: topCity and nextCity provided
// Post-condition: return true if an unvisited adjacent city was found
//              otherwise return false
bool FlightMapClass::GetNextCity(string fromCity, string &nextCity){
    int cityIndex = GetCityNumber(fromCity);
    if (cityIndex == -1) return false;

    for (const auto& flight : adjList[cityIndex]) {
        int nextCityIndex = GetCityNumber(flight.destination);
        if (!IsVisited(nextCityIndex)) {
            nextCity = flight.destination;
            return true;
        }
    }
    return false;
}

// returns the integer index corresponding to a city name
// Pre-condition: name of a city is provided
// Post-condition: returns the index number corresponding to a city name
int FlightMapClass::GetCityNumber(string cityName) const{
    auto it = find(cities.begin(), cities.end(), cityName);
    if (it != cities.end()) {
        return distance(cities.begin(), it);
    } else {
        return -1;
    }
}

// returns the name of a city given its corresponding index
// Pre-condition: number of a city is provided
// Post-condition: returns the city's name
string FlightMapClass::GetCityName(int cityNumber) const{
    if (cityNumber >= 0 && cityNumber < cities.size()) {
        return cities[cityNumber];
    } else {
        return "";
    }
}

// Determines whether a sequence of flights between two cities exists.
// Pre-condition: originCity and destinationCity are the origin and destination city, respectively
// Post-condition: returns true if a sequence of flights exists
//              from origin to destination; otherwise return false.
//              Cities visited during the search are marked as visited
//              in the flight map.
bool FlightMapClass::FindPath(string originCity, string destinationCity) {
    if (!CheckCity(originCity) || !CheckCity(destinationCity)) {
        cout << "Sorry, BlueSky airline does not serve ";
        if (!CheckCity(originCity)) cout << originCity;
        else cout << destinationCity;
        cout << "." << endl;
        return false;
    }

    stack<int> cityStack;
    UnvisitAll();
    vector<int> path;
    
    int currentCityIndex = GetCityNumber(originCity);
    cityStack.push(currentCityIndex);
    MarkVisited(currentCityIndex);

    while (!cityStack.empty()) {
        int cityIndex = cityStack.top();
        string cityName = GetCityName(cityIndex);

        if (cityName == destinationCity) {
            BuildItinerary(cityStack);
            return true;
        }
        
        string nextCity;
        if (GetNextCity(cityName, nextCity)) {
            int nextCityIndex = GetCityNumber(nextCity);
            cityStack.push(nextCityIndex);
            MarkVisited(nextCityIndex);
            path.push_back(nextCityIndex);
        } else {
            cityStack.pop();
            if (!path.empty()) path.pop_back();
        }
    }
    cout << "Sorry, BlueSky airline does not fly from " << originCity << " to " << destinationCity << "." << endl;
    return false;
}

//Reads flight information and build the adjacency list
//Pre-condition: list of the flight information is provided
//Post-condition: Flight map is built
void FlightMapClass::BuildMap(ifstream& fp) {
    flightRec flight;
    string origin, destination;
    while (fp>> flight.flightNum>> origin>> destination>> flight.price) {
        flight.origin = origin;
        flight.destination = destination;
//Finds the index for the origin city
        auto it = find(cities.begin(), cities.end(), origin);
        if (it != cities.end()) {
            int index = distance(cities.begin(), it);
            adjList[index].push_back(flight);
        }
    }
//Sorts destinations
    for (int i = 0; i < numberOfCities; ++i) {
        adjList[i].sort([](const flightRec& a, const flightRec& b) {
            return a.destination < b.destination;
        });
    }
}

// Displays the flight map in a formatted table
// Pre-condition: none
// Post-condition: Flight map is displayed
void FlightMapClass::DisplayMap(list<flightRec>* flightMap){
    cout << flightMap;
}

// Check whether a city is in the cities that EastWest airline serves.
// Pre-condition: cityNumber to be checked is provided
// Post-condition: return true if the city is in the cities array
//              otherwise return false
bool FlightMapClass::CheckCity(string cityName) const{
    // Use find algorithm to search for the city in the cities vector.
    return find(cities.begin(), cities.end(), cityName) != cities.end();
}

// Marks a city as visited
// Pre-condition: city to be marked as visited is provided
// Post-condition: a city is marked as visited
void FlightMapClass::MarkVisited(int city){
    if(city >= 0 && city < visited.size()) {
        visited[city] = true;
    } else {
        cerr << "Invalid city index in MarkVisited." << endl;
    }
}

// Displays all of the cities
void FlightMapClass::DisplayAllCities() const{
    cout << "Cities served by BlueSky Airlines:" << endl;
    for (const auto& city : cities) {
        cout << city << endl;
    }
}

void FlightMapClass::BuildItinerary(stack<int> cityStack) {
    int totalCost = 0;
    cout << "The flight itinerary is:" << endl;
    cout << setw(10)<< "Flight#"<< setw(10)<< "From"<< setw(10)<<"To" setw(6)<< "Cost" << endl;

    int prevCityIndex = -1;
    while (!cityStack.empty()) {
        int currentCityIndex = cityStack.top();
        cityStack.pop();

        if (prevCityIndex != -1) {
            for (const auto& flight : adjList[prevCityIndex]) {
                if (GetCityNumber(flight.destination) == currentCityIndex) {
                    cout << setw(10)<< flight.flightNum<< setw(10)<< GetCityName(prevCityIndex)<< setw(10)<< flight.destination << setw(6)<< "$"<< flight.price<< endl;
                    totalCost += flight.price;
                    break;
                }
            }
        }
        prevCityIndex = currentCityIndex;
    }

    cout << "Total: $" << totalCost << endl;
}
