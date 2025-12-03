# COSC2976 Assignment 2 - Retail Management System

## Overview
This is a comprehensive retail management system built using Object-Oriented Programming in Python. The system manages customers, products, orders, and provides various analytics features for a department store.

## File Information
- **Program File**: `ProgFunA2_s1234567.py`
- **Student ID**: Replace `s1234567` in the filename with your actual student ID

## Features Implemented

### PASS Level (12 marks)
✅ Customer class hierarchy (Customer, Member, VIPMember)
✅ Product class with stock management
✅ Order class for processing purchases
✅ Records class for data management
✅ Menu-driven operations system
✅ File reading for customers and products
✅ Discount calculations based on customer type
✅ Dynamic customer creation and updates

### CREDIT Level (3 marks)
✅ Bundle class (products sold together at 80% price)
✅ Custom exceptions for validation:
  - InvalidProductError
  - InvalidQuantityError
  - InvalidMembershipAnswerError
  - InvalidMembershipTypeError
  - InvalidFileFormatError
  - InvalidPriceError
✅ Exception handling for all user inputs
✅ Support for product IDs and names in orders

### DI Level (3 marks)
✅ Order class with datetime support
✅ Orders file loading and management
✅ Adjust VIP member discount rates
✅ Adjust VIP threshold for all members
✅ Display all orders functionality
✅ Display orders for specific customer
✅ Comprehensive error handling for file operations

### HD Level (6 marks)
✅ Command-line argument support for file names
✅ Multiple items per order support
✅ Order summary table display
✅ Most valuable customer analysis
✅ Most popular product analysis
✅ File updates on program termination

## Usage

### Running the Program

#### Default files (customers.txt, products.txt, orders.txt):
```bash
python3 ProgFunA2_s1234567.py
```

#### With custom customer and product files:
```bash
python3 ProgFunA2_s1234567.py <customer_file> <product_file>
```

#### With all three files specified:
```bash
python3 ProgFunA2_s1234567.py <customer_file> <product_file> <order_file>
```

### Examples:
```bash
# Test with PASS level files
python3 ProgFunA2_s1234567.py files_PASSlevel/customers.txt files_PASSlevel/products.txt

# Test with CREDIT level files (includes bundles)
python3 ProgFunA2_s1234567.py files_CREDITlevel/customers.txt files_CREDITlevel/products.txt

# Test with DI level files (includes orders)
python3 ProgFunA2_s1234567.py files_DIlevel/customers.txt files_DIlevel/products.txt files_DIlevel/orders.txt

# Test with HD level files (multiple items per order)
python3 ProgFunA2_s1234567.py files_HDlevel/customers.txt files_HDlevel/products.txt files_HDlevel/orders.txt
```

## Menu Options

1. **Place an order** - Process customer orders with discount calculations
2. **Display existing customers** - Show all customers with their details
3. **Display existing products** - Show all products including bundles
4. **Adjust VIP member discount rates** - Modify discount rates for individual VIP members
5. **Adjust VIP threshold** - Change the threshold for all VIP members
6. **Display all orders** - Show complete order history
7. **Display customer orders** - Show orders for a specific customer
8. **Summarize all orders** - Display order summary table
9. **Reveal most valuable customer** - Show customer with highest total spending
10. **Reveal most popular product** - Show product with most orders
0. **Exit the program** - Save data and exit

## File Formats

### customers.txt
Format: `ID, name, discount_rate, value`
- ID starting with 'C': Normal Customer
- ID starting with 'M': Member
- ID starting with 'V': VIP Member (first discount rate)

Example:
```
C1, James, 0, 500.2
M3, Tom, 0.05, 250.0
V5, Harry, 0.125, 600.0
```

### products.txt
Format: `ID, name, price, stock` or `ID, name, component_IDs..., stock` (for bundles)
- ID starting with 'P': Normal Product
- ID starting with 'B': Bundle

Example:
```
P1, shirt, 50.0, 30
P2, towel, 20.0, 20
B8, houseapp, P3, P4, P5, 10
```

### orders.txt (DI & HD levels)
Format: `customer_name/ID, product1, qty1, [product2, qty2, ...], date`

Example:
```
James, P3, 1, 01/09/2021 10:10:00
Lily, shirt, 2, towel, 5, 05/09/2021 14:00:00
```

## Libraries Used
- `sys` - Command-line argument processing
- `datetime` - Order timestamp management
- `copy` - Deep copying objects (if needed)
- `os` - File operations and path checking

## Object-Oriented Design

### Class Hierarchy:
```
Customer (base class)
├── Member (inherits from Customer)
└── VIPMember (inherits from Customer)

Product (base class)
└── Bundle (inherits from Product)

OrderItem (helper class for Order)
Order (manages order processing)

Records (central data repository)
Operations (menu system and user interface)
```

### Key OOP Concepts Demonstrated:
- **Inheritance**: Customer → Member, VIPMember; Product → Bundle
- **Polymorphism**: get_discount() method overridden in subclasses
- **Encapsulation**: Private attributes with getter/setter methods
- **Abstraction**: Clean interfaces for complex operations
- **Class variables**: Shared discount rates and thresholds
- **Instance variables**: Individual customer rates

## Testing

Run the test suite to verify all features:
```bash
python3 test_program.py
```

This will test:
- PASS level: Display customers and products
- CREDIT level: Bundles and exceptions
- DI level: Order management
- HD level: Statistics and summaries

## Important Notes

1. **Weekly Submissions**: Submit code weekly (Week 7-9) with at least 50 lines of new code each week
2. **Final Submission**: Submit the complete program by end of Week 10
3. **File Naming**: File must be named `ProgFunA2_<YourStudentID>.py`
4. **No External Libraries**: Only use sys, datetime, copy, and os
5. **Comments Required**: Include explanatory comments throughout the code
6. **Error Handling**: All user inputs are validated with custom exceptions

## Code Quality Features

✅ Comprehensive documentation with docstrings
✅ Consistent naming conventions
✅ Modular design with clear separation of concerns
✅ DRY principle (Don't Repeat Yourself)
✅ Defensive programming with validation
✅ Clear error messages for users
✅ Graceful handling of edge cases

## Reflection

### Challenges Faced:
1. **Class Design**: Determining the optimal class hierarchy and relationships
2. **File Format Handling**: Supporting both single and multiple items in orders
3. **Exception Handling**: Implementing comprehensive validation without over-complicating
4. **Data Persistence**: Ensuring data is correctly saved when program exits

### Design Decisions:
1. **OrderItem Class**: Created separate class to handle multiple items per order (HD level)
2. **Records Class**: Centralized data management for better organization
3. **Custom Exceptions**: Specific exceptions for each validation scenario
4. **Class vs Instance Variables**: Carefully chosen for discount rates and thresholds

### Potential Improvements:
1. Add data validation for file writes to prevent corruption
2. Implement undo/redo functionality for orders
3. Add reporting features (monthly sales, inventory alerts)
4. Create a graphical user interface
5. Add database support for larger datasets
6. Implement product categories and search filters

## Author
Student ID: s1234567 (Replace with your ID)
Course: COSC2976 Programming Fundamentals
Institution: RMIT University
