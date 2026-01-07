#define _CRT_SECURE_NO_WARNINGS // Fix for Visual Studio safety warnings

#include <iostream>
#include <vector>
#include <string>
#include <limits>
#include <fstream>
#include <ctime>
#include <iomanip> // Required for the grid formatting

// ==========================================
// TITLE IV-D COMPLIANCE & AUDIT TRACKER v2.1
// ==========================================

using namespace std;

string getCurrentTimestamp() {
    time_t now = time(0);
    tm* ltm = localtime(&now);
    char buffer[80];
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", ltm);
    return string(buffer);
}

class Interaction {
private:
    string timestamp;
    string question;
    string dataReceived;
    bool flaggedForReview;

public:
    Interaction(string q, string d, bool flag)
        : question(q), dataReceived(d), flaggedForReview(flag) {
        timestamp = getCurrentTimestamp();
    }

    string getTimestamp() const { return timestamp; }
    string getQuestion() const { return question; }
    string getData() const { return dataReceived; }
    bool isFlagged() const { return flaggedForReview; }
};

class Contact {
private:
    string name;
    string jobTitle;
    vector<Interaction> interactions;

public:
    Contact(string n, string t) : name(n), jobTitle(t) {}

    string getName() const { return name; }
    string getTitle() const { return jobTitle; }
    const vector<Interaction>& getInteractions() const { return interactions; }

    void addInteraction(string q, string d, bool flag) {
        interactions.emplace_back(q, d, flag);
    }
};

class Business {
private:
    string businessName;
    string fundingType;
    vector<Contact> contacts;

public:
    Business(string n, string f) : businessName(n), fundingType(f) {}

    string getName() const { return businessName; }
    string getType() const { return fundingType; }
    const vector<Contact>& getContacts() const { return contacts; }

    void addContact(string name, string title) {
        contacts.emplace_back(name, title);
    }

    Contact* getContact(string contactName) {
        for (auto& contact : contacts) {
            if (contact.getName() == contactName) {
                return &contact;
            }
        }
        return nullptr;
    }
};

class AuditTracker {
private:
    vector<Business> businesses;

public:
    void addBusiness() {
        string name, type;
        cout << "\nEnter Entity/Business Name: ";
        getline(cin, name);
        cout << "Enter Funding Type (ex: Federal Grant, State Contractor, etc): ";
        getline(cin, type);
        businesses.emplace_back(name, type);
        cout << ">> Entity successfully added.\n";
    }

    void addContactToBusiness() {
        if (businesses.empty()) {
            cout << ">> No entities found. Please add an entity first.\n";
            return;
        }

        cout << "\nSelect Entity:\n";
        for (size_t i = 0; i < businesses.size(); ++i) {
            cout << i + 1 << ". " << businesses[i].getName() << endl;
        }

        int choice;
        cout << "Enter Choice: ";
        cin >> choice;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (choice > 0 && choice <= businesses.size()) {
            string name, title;
            cout << "Enter Contact Name: ";
            getline(cin, name);
            cout << "Enter Job Title: ";
            getline(cin, title);
            businesses[choice - 1].addContact(name, title);
            cout << ">> Contact successfully added.\n";
        }
        else {
            cout << ">> Invalid selection.\n";
        }
    }

    void logInteraction() {
        if (businesses.empty()) {
            cout << ">> No entities found in database.\n";
            return;
        }

        cout << "\n--- SELECT ENTITY ---\n";
        for (size_t i = 0; i < businesses.size(); ++i) {
            cout << i + 1 << ". " << businesses[i].getName() << endl;
        }
        int bChoice;
        cout << "Enter Choice: ";
        cin >> bChoice;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (bChoice <= 0 || bChoice > businesses.size()) {
            cout << ">> Invalid selection.\n";
            return;
        }

        Business& selectedBiz = businesses[bChoice - 1];

        string cName;
        cout << "Enter Contact Name: ";
        getline(cin, cName);

        Contact* contact = selectedBiz.getContact(cName);
        if (contact == nullptr) {
            cout << ">> Contact not found. Please verify spelling.\n";
            return;
        }

        // Continuous Question Loop
        bool keepAsking = true;
        while (keepAsking) {
            string q, d;
            char flagInput, continueInput;
            bool flagged = false;

            cout << "\n--- NEW INQUIRY FOR: " << contact->getName() << " ---\n";
            cout << "Enter Question Asked: ";
            getline(cin, q);
            cout << "Enter Response/Data Received: ";
            getline(cin, d);
            cout << "Flag for review/discrepancy? (y/n): ";
            cin >> flagInput;
            cin.ignore(numeric_limits<streamsize>::max(), '\n');

            if (flagInput == 'y' || flagInput == 'Y') flagged = true;

            contact->addInteraction(q, d, flagged);
            cout << ">> Interaction logged.\n";

            cout << ">> Ask another question to this contact? (y/n): ";
            cin >> continueInput;
            cin.ignore(numeric_limits<streamsize>::max(), '\n');

            if (continueInput == 'n' || continueInput == 'N') {
                keepAsking = false;
            }
        }
    }

    void saveToCSV() {
        ofstream myFile;
        string filename = "TitleIVD_Audit_Log.csv";
        myFile.open(filename);

        myFile << "Timestamp,Entity Name,Funding Type,Contact Name,Job Title,Question,Response,Flagged\n";

        for (const auto& biz : businesses) {
            for (const auto& contact : biz.getContacts()) {
                for (const auto& interact : contact.getInteractions()) {
                    myFile << "\"" << interact.getTimestamp() << "\","
                        << "\"" << biz.getName() << "\","
                        << "\"" << biz.getType() << "\","
                        << "\"" << contact.getName() << "\","
                        << "\"" << contact.getTitle() << "\","
                        << "\"" << interact.getQuestion() << "\","
                        << "\"" << interact.getData() << "\","
                        << (interact.isFlagged() ? "YES" : "NO") << "\n";
                }
            }
        }

        myFile.close();
        cout << "\n>> Data successfully exported to " << filename << ".\n";
    }

    void viewGrid() const {
        if (businesses.empty()) {
            cout << ">> Database is empty.\n";
            return;
        }

        cout << "\n";
        // Header
        cout << left << setw(20) << "ENTITY"
            << setw(15) << "CONTACT"
            << setw(30) << "QUESTION"
            << setw(30) << "RESPONSE"
            << setw(10) << "FLAGGED" << endl;

        cout << string(105, '-') << endl;

        for (const auto& biz : businesses) {
            for (const auto& contact : biz.getContacts()) {
                for (const auto& interact : contact.getInteractions()) {

                    // Truncate long strings for display only
                    string qDisp = interact.getQuestion();
                    if (qDisp.length() > 28) qDisp = qDisp.substr(0, 25) + "...";

                    string dDisp = interact.getData();
                    if (dDisp.length() > 28) dDisp = dDisp.substr(0, 25) + "...";

                    cout << left << setw(20) << biz.getName().substr(0, 18)
                        << setw(15) << contact.getName().substr(0, 13)
                        << setw(30) << qDisp
                        << setw(30) << dDisp
                        << setw(10) << (interact.isFlagged() ? "YES" : "-") << endl;
                }
            }
        }
        cout << "\n";
    }
};

int main() {
    AuditTracker tracker;
    int option = 0;

    while (option != 6) { // Updated loop to check for 6
        cout << "\n--- TITLE IV-D FRAUD TRACKER ---\n";
        cout << "1. Add Entity/Business\n";
        cout << "2. Add Contact\n";
        cout << "3. Log Interaction (Q&A)\n";
        cout << "4. View Data Grid\n";       // New dedicated view option
        cout << "5. Export Data to CSV\n";   // New dedicated export option
        cout << "6. Exit\n";
        cout << "Enter Option: ";
        cin >> option;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        switch (option) {
        case 1: tracker.addBusiness(); break;
        case 2: tracker.addContactToBusiness(); break;
        case 3: tracker.logInteraction(); break;
        case 4: tracker.viewGrid(); break;   // View only
        case 5: tracker.saveToCSV(); break;  // Export only
        case 6: cout << ">> Exiting application.\n"; break;
        default: cout << ">> Invalid option. Please try again.\n"; break;
        }
    }

    return 0;
}
