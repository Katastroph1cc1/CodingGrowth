/* 
Brandon Merrell
12/5/2025
Project 3
*/

#include <iostream>
#include <fstream>
#include <string>
#include <map> // Using as recommended by project details
using namespace std;

// Using to keep track of the items
class ItemTracker {
private:
    map<string, int> itemFrequencyMap;

public:
    void readFile(string fileName);
    void backupFile();
    int getItemFrequency(string itemName);
    void printItemFrequencies();
    void printHistogram();
};


// Reads the input file and uses a map to count frequencies to test from the provided file 
void ItemTracker::readFile(string fileName) {
    ifstream inputFile(fileName);
    string currentWord;

    if (!inputFile.is_open()) {
        cout << "Error: Could not open file " << fileName << endl;
        return;
    }

    // If the word exists, it adds 1 to the count
    // If the word does not exist, it creates it and sets count to 1
    while (inputFile >> currentWord) {
        itemFrequencyMap[currentWord]++;
    }

    inputFile.close();
}

// Creates the backup file frequency.dat
void ItemTracker::backupFile() {
    ofstream outputFile("frequency.dat");

    if (!outputFile.is_open()) {
        cout << "Error: Could not create backup file frequency.dat" << endl;
        return;
    }

    // Iterate through the map and write to file
    // "pair.first" is the Name, "pair.second" is the Count
    for (const auto& pair : itemFrequencyMap) {
        outputFile << pair.first << " " << pair.second << endl;
    }

    outputFile.close();
}

// Returns the frequency of a specific item
int ItemTracker::getItemFrequency(string itemName) {
    // Check if the item exists in the map
    if (itemFrequencyMap.count(itemName)) {
        return itemFrequencyMap[itemName];
    }
    else {
        return 0;
    }
}

// Prints all items and their frequencies
void ItemTracker::printItemFrequencies() {
    cout << "\n--- Item Frequency List ---" << endl;

    // Iterate through the map
    for (const auto& pair : itemFrequencyMap) {
        cout << pair.first << ": " << pair.second << endl;
    }
    cout << "---------------------------" << endl;
}

// Prints a histogram using asterisks
void ItemTracker::printHistogram() {
    cout << "\n--- Item Histogram ---" << endl;

    for (const auto& pair : itemFrequencyMap) {
        cout << pair.first << ": ";

        // Printing the asteriks based on the item count
        for (int i = 0; i < pair.second; ++i) {
            cout << "*";
        }
        cout << endl;
    }
    cout << "----------------------" << endl;
}



int main() {
    ItemTracker tracker;
    int userChoice = 0;
    string searchItem;

    // Loading the items from the provided file for testing
    tracker.readFile("Items.txt");

    // Creating a backup file 
    tracker.backupFile();

    // The main menu loop
    while (userChoice != 4) {
        cout << "-------------------------------" << endl;
        cout << "  CORNER GROCER ITEM TRACKING" << endl;
        cout << "-------------------------------" << endl;
        cout << "1. Search for an item frequency" << endl;
        cout << "2. Print list of all item frequencies" << endl;
        cout << "3. Print histogram" << endl;
        cout << "4. Exit" << endl;
        cout << "Please enter a menu option: ";

        // The input validation
        if (!(cin >> userChoice)) {
            cout << "Invalid input. Please enter a number." << endl;
            cin.clear();
            cin.ignore(1000, '\n');
            continue;
        }

        switch (userChoice) {
        case 1:
            cout << "Enter the item name (case sensitive): ";
            cin >> searchItem;
            cout << "Frequency of " << searchItem << ": "
                << tracker.getItemFrequency(searchItem) << endl;
            break;

        case 2:
            tracker.printItemFrequencies();
            break;

        case 3:
            tracker.printHistogram();
            break;

        case 4:
            cout << "Exiting program. Goodbye." << endl;
            break;

        default:
            cout << "Invalid option. Please choose a number 1-4." << endl;
            break;
        }
    }

    return 0;
}
