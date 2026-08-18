# CarStruct

A **desktop-based Car Showroom Management System** built with Python and PyQt5. The project was designed to demonstrate the practical use of various **Data Structures and Algorithms (DSA)** in a real-world application.

CarStruct allows users to explore and manage car showroom data, search and sort vehicles, traverse manufacturer relationships, manage test-drive requests, and interact with the system through a graphical user interface.

## Features

### Car Inventory Management

The application manages car showroom data and allows users to:

- Browse available cars
- View car information
- Search for specific cars
- Sort cars based on different attributes
- Explore cars by manufacturer
- Store and load showroom data using CSV files

Car data is persisted in:

```text
Files/car_showroom_data.csv
```

---

### User Authentication

The project includes an authentication system for showroom access.

- Admin credentials are stored locally
- Login functionality is implemented through the GUI
- Hashing is used as part of the authentication/data management approach

Credential data is stored in:

```text
Files/AdminCredentials.csv
```

---

### Car Searching

Different searching techniques are implemented to retrieve car information efficiently.

- Linear Search
- Binary Search

These algorithms are used depending on the type and organization of the data.

---

### Car Sorting

The project implements multiple sorting algorithms for organizing car data based on attributes such as price, mileage, or other available information.

Implemented sorting approaches include:

- Quick Sort
- Merge Sort

---

### Manufacturer and Car Relationships

A graph-based representation is used to model relationships between manufacturers and their car models.

The project implements graph traversal algorithms including:

- Breadth-First Search (BFS)
- Depth-First Search (DFS)

This allows users to explore cars associated with manufacturers in different traversal patterns.

---

### AVL Tree

An AVL Tree is used to organize data efficiently while maintaining a balanced binary search tree structure.

This provides efficient operations for:

- Insertion
- Searching
- Organized data storage

---

### Hash Table

Hashing is used for efficient data access and management.

The implementation includes concepts such as:

- Hash-based storage
- Collision handling
- Dynamic rehashing

This structure is used as part of the system's data management and authentication functionality.

---

### Test Drive Management

The system manages customer test-drive requests using a **Queue**.

This follows the FIFO principle:

```text
First Customer Request
        ↓
     Queue
        ↓
Next Customer Gets Test Drive
```

Test-drive data is stored locally in:

```text
Files/car_testdrive_data.csv
```

---

### User Navigation History

A **Stack** is used to manage user interaction history and navigation.

This follows the LIFO principle:

```text
Latest Action
     ↓
   Stack
     ↓
Previous Actions
```

The stack allows the application to maintain a structured history of user interactions.

## Data Structures and Algorithms

One of the main purposes of CarStruct is to demonstrate the use of DSA concepts in a practical application.

| Concept | Usage |
|---|---|
| Graph | Represents relationships between manufacturers and cars |
| BFS | Breadth-first exploration of graph data |
| DFS | Depth-first exploration of graph data |
| AVL Tree | Balanced organization and searching of data |
| Hash Table | Efficient data storage and lookup |
| Queue | Test-drive request management |
| Stack | User interaction/navigation history |
| Linear Search | Sequential data searching |
| Binary Search | Efficient searching on sorted data |
| Quick Sort | Sorting car data |
| Merge Sort | Sorting car data |
| File Handling | Persistent storage using CSV files |

## Project Structure

```text
CarStruct/
│
├── Components/
│   ├── Data_Structures/
│   │
│   ├── Login.py
│   ├── Our_Showroom.py
│   ├── graphTraversals[DFSBFS].py
│   ├── searchingSorting.py
│   └── untitled.ui
│
├── Files/
│   ├── AdminCredentials.csv
│   ├── car_showroom_data.csv
│   └── car_testdrive_data.csv
│
├── UI/
│   ├── New folder/
│   ├── loginUi4/
│   ├── main.py
│   ├── main.ui
│   └── untitled.ui
│
├── images/
│
├── car_showroom_data.csv
│
├── main.py
│
└── README.md
```

## Technology Stack

### Programming Language

- Python

### User Interface

- PyQt5

### Data Storage

- CSV files
- File handling

### Visualization

- Matplotlib

### Data Processing

- Pandas

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/alit9876/CarStruct.git
```

### 2. Navigate to the project directory

```bash
cd CarStruct
```

### 3. Install the required dependencies

```bash
pip install PyQt5 pandas matplotlib
```

### 4. Run the application

```bash
python main.py
```

## How It Works

The application combines multiple DSA concepts into a car showroom management workflow.

```text
                ┌─────────────────┐
                │   PyQt5 GUI     │
                └────────┬────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     Authentication   Car Inventory   Test Drives
          │              │              │
          ▼              ▼              ▼
       Hashing       Search / Sort     Queue
                         │
                         ▼
                  Graph Traversal
                  BFS / DFS
                         │
                         ▼
                      AVL Tree
```

## Learning Objectives

This project demonstrates the practical implementation of:

- Object-Oriented Programming
- Graph data structures
- BFS and DFS traversal
- AVL Trees
- Hash Tables
- Stacks
- Queues
- Searching algorithms
- Sorting algorithms
- File handling
- GUI development using PyQt5

## Future Improvements

Possible improvements include:

- Database integration instead of CSV-based storage
- More advanced user roles and authentication
- Improved inventory management
- Car booking and purchase management
- Customer management
- Sales reports and analytics
- Better error handling and validation
- Improved UI/UX
- Unit testing for individual data structures
- Packaging the application as a standalone desktop executable

## Author

**Muhammad Ali**

## License

This project was developed for educational purposes as a practical implementation of **Data Structures and Algorithms** concepts.