Implement the struct type defined in type.h here

#include "type.h"
using namespace std;
// Define the overloaded methods for struct type here
bool flightRec::operator<(const flightRec& otherRec) const {
    return price < otherRec.price;
}
bool flightRec::operator==(const flightRec& otherRec) const {
    return flightNum == otherRec.flightNum && origin == otherRec.origin &&
           destination == otherRec.destination && price == otherRec.price;
}
ostream& operator<<(ostream& os, const flightRec& fr) {
    os << "Flight #" << fr.flightNum << " From " << fr.origin << " To " << fr.destination << " Price $" << fr.price;
    return os;
}