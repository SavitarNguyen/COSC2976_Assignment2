# Testing Guide for Assignment 2

## Quick Test Commands

### Test PASS Level Features
```bash
cd /Users/tysonnguyen/Downloads/COSC2976_Assignment2

# Test display customers
echo -e "2\n0" | python3 ProgFunA2_s1234567.py files_PASSlevel/customers.txt files_PASSlevel/products.txt

# Test display products
echo -e "3\n0" | python3 ProgFunA2_s1234567.py files_PASSlevel/customers.txt files_PASSlevel/products.txt
```

### Test CREDIT Level Features
```bash
# Test bundles display
echo -e "3\n0" | python3 ProgFunA2_s1234567.py files_CREDITlevel/customers.txt files_CREDITlevel/products.txt
```

### Test DI Level Features
```bash
# Test display all orders
echo -e "6\n0" | python3 ProgFunA2_s1234567.py files_DIlevel/customers.txt files_DIlevel/products.txt files_DIlevel/orders.txt

# Test display orders for specific customer
echo -e "7\nJames\n0" | python3 ProgFunA2_s1234567.py files_DIlevel/customers.txt files_DIlevel/products.txt files_DIlevel/orders.txt
```

### Test HD Level Features
```bash
# Test order summary
echo -e "8\n0" | python3 ProgFunA2_s1234567.py files_HDlevel/customers.txt files_HDlevel/products.txt files_HDlevel/orders.txt

# Test most valuable customer
echo -e "9\n0" | python3 ProgFunA2_s1234567.py files_HDlevel/customers.txt files_HDlevel/products.txt files_HDlevel/orders.txt

# Test most popular product
echo -e "10\n0" | python3 ProgFunA2_s1234567.py files_HDlevel/customers.txt files_HDlevel/products.txt files_HDlevel/orders.txt
```

## Interactive Testing Scenarios

### Scenario 1: Place Order for Existing Customer (PASS Level)
```
1. Run: python3 ProgFunA2_s1234567.py files_PASSlevel/customers.txt files_PASSlevel/products.txt
2. Choose option: 1
3. Enter customer name: James
4. Enter product: shirt
5. Enter quantity: 2
6. Order more products: n
7. Check the order receipt displays correctly
8. Choose option: 2 to verify customer value updated
9. Exit: 0
```

Expected Output:
```
James purchases 2 x shirt.
Unit price: 50.0 (AUD)
James gets a discount of 0 %.
Total price: 100.0 (AUD)
```

### Scenario 2: Place Order for New Customer with Membership (PASS Level)
```
1. Run: python3 ProgFunA2_s1234567.py files_PASSlevel/customers.txt files_PASSlevel/products.txt
2. Choose option: 1
3. Enter customer name: TestUser
4. Enter product: oven
5. Enter quantity: 1
6. Order more products: n
7. Want membership: y
8. Membership type: M
9. Check receipt shows 5% discount
10. Exit: 0
```

Expected Output:
```
TestUser purchases 1 x oven.
Unit price: 300.0 (AUD)
TestUser gets a discount of 5.0 %.
Total price: 285.0 (AUD)
```

### Scenario 3: Place Order for New VIP Customer (PASS Level)
```
1. Run: python3 ProgFunA2_s1234567.py files_PASSlevel/customers.txt files_PASSlevel/products.txt
2. Choose option: 1
3. Enter customer name: VIPTest
4. Enter product: microwave
5. Enter quantity: 1
6. Order more products: n
7. Want membership: y
8. Membership type: V
9. Check receipt shows 10% discount and 200 AUD membership fee
10. Exit: 0
```

Expected Output:
```
VIPTest purchases 1 x microwave.
Unit price: 200.0 (AUD)
Membership price: 200.0 (AUD)
VIPTest gets a discount of 10.0 %.
Total price: 380.0 (AUD)
```

### Scenario 4: Test Exception Handling (CREDIT Level)
```
1. Run: python3 ProgFunA2_s1234567.py files_CREDITlevel/customers.txt files_CREDITlevel/products.txt
2. Choose option: 1
3. Enter customer name: James
4. Enter product: invalidproduct (should show error)
5. Enter product: shirt (valid)
6. Enter quantity: abc (should show error)
7. Enter quantity: -5 (should show error)
8. Enter quantity: 1000 (exceeds stock, should show error)
9. Enter quantity: 2 (valid)
10. Order more: xyz (should show error)
11. Order more: n (valid)
12. Exit: 0
```

### Scenario 5: Order Bundle (CREDIT Level)
```
1. Run: python3 ProgFunA2_s1234567.py files_CREDITlevel/customers.txt files_CREDITlevel/products.txt
2. Choose option: 1
3. Enter customer name: Tom
4. Enter product: B8 (or houseapp)
5. Enter quantity: 1
6. Order more: n
7. Check price is 80% of (oven + kettle + microwave)
8. Exit: 0
```

Expected Bundle Price:
- Oven: 300, Kettle: 90.2, Microwave: 200
- Total: 590.2
- Bundle (80%): 472.16

### Scenario 6: Adjust VIP Discount Rate (DI Level)
```
1. Run: python3 ProgFunA2_s1234567.py files_DIlevel/customers.txt files_DIlevel/products.txt files_DIlevel/orders.txt
2. Choose option: 4
3. Enter VIP member: Harry (or V5)
4. Enter new rate: abc (should show error)
5. Enter new rate: -0.1 (should show error)
6. Enter new rate: 0.20 (valid)
7. Verify: First rate = 20%, Second rate = 25%
8. Exit: 0
```

### Scenario 7: Adjust VIP Threshold (DI Level)
```
1. Run: python3 ProgFunA2_s1234567.py files_DIlevel/customers.txt files_DIlevel/products.txt files_DIlevel/orders.txt
2. Choose option: 5
3. Enter threshold: abc (should show error)
4. Enter threshold: -100 (should show error)
5. Enter threshold: 0 (should show error)
6. Enter threshold: 1500 (valid)
7. Verify threshold updated message
8. Exit: 0
```

### Scenario 8: Multiple Items in Single Order (HD Level)
```
1. Run: python3 ProgFunA2_s1234567.py files_HDlevel/customers.txt files_HDlevel/products.txt files_HDlevel/orders.txt
2. Choose option: 1
3. Enter customer name: James
4. Enter product: shirt
5. Enter quantity: 2
6. Order more: y
7. Enter product: towel
8. Enter quantity: 3
9. Order more: y
10. Enter product: oven
11. Enter quantity: 1
12. Order more: n
13. Check all items appear in receipt
14. Exit: 0
```

Expected Output:
```
James purchases 2 x shirt.
Unit price: 50.0 (AUD)
James purchases 3 x towel.
Unit price: 20.0 (AUD)
James purchases 1 x oven.
Unit price: 300.0 (AUD)
James gets a discount of 0 %.
Total price: 460.0 (AUD)
```

### Scenario 9: Command-Line Arguments (HD Level)
```bash
# No arguments - use defaults
python3 ProgFunA2_s1234567.py

# Two arguments
python3 ProgFunA2_s1234567.py files_PASSlevel/customers.txt files_PASSlevel/products.txt

# Three arguments
python3 ProgFunA2_s1234567.py files_HDlevel/customers.txt files_HDlevel/products.txt files_HDlevel/orders.txt

# Wrong number of arguments (should show usage)
python3 ProgFunA2_s1234567.py file1.txt
```

## Automated Test Script

Run the comprehensive test suite:
```bash
python3 test_program.py
```

This will automatically test:
1. ✅ Customer display (PASS)
2. ✅ Product display with bundles (CREDIT)
3. ✅ Order display (DI)
4. ✅ Order summary (HD)
5. ✅ Most valuable customer (HD)
6. ✅ Most popular product (HD)

## Verification Checklist

### PASS Level (12 marks)
- [ ] Customer class with ID, name, value
- [ ] Member class with 5% flat discount
- [ ] VIPMember class with two-tier discount
- [ ] Product class with ID, name, price, stock
- [ ] Order class processes orders correctly
- [ ] Records class reads customers.txt
- [ ] Records class reads products.txt
- [ ] Menu displays all options
- [ ] Place order option works
- [ ] Display customers option works
- [ ] Display products option works
- [ ] Program exits gracefully

### CREDIT Level (3 marks)
- [ ] Bundle class calculates 80% price
- [ ] InvalidProductError exception defined
- [ ] InvalidQuantityError exception defined
- [ ] InvalidMembershipAnswerError exception defined
- [ ] InvalidMembershipTypeError exception defined
- [ ] InvalidFileFormatError exception defined
- [ ] Exception handling for invalid products
- [ ] Exception handling for invalid quantities
- [ ] Exception handling for invalid membership answers
- [ ] Exception handling for invalid membership types
- [ ] Exception handling for file errors
- [ ] Product price validation (0, negative, empty)
- [ ] Support for both product IDs and names

### DI Level (3 marks)
- [ ] Order class has date attribute
- [ ] Orders.txt file can be loaded
- [ ] Display all orders option works
- [ ] Display customer orders option works
- [ ] Adjust VIP discount rates option works
- [ ] Adjust VIP threshold option works
- [ ] Exception handling for discount rate input
- [ ] Exception handling for threshold input
- [ ] Invalid customer error handling
- [ ] Support for both customer IDs and names

### HD Level (6 marks)
- [ ] Command-line arguments supported (0, 2, or 3 args)
- [ ] Wrong number of arguments shows usage
- [ ] Multiple items per order supported
- [ ] Order summary table displays correctly
- [ ] Most valuable customer option works
- [ ] Most popular product option works
- [ ] Files updated on program exit

### Code Quality (3 marks)
- [ ] Consistent code formatting
- [ ] Meaningful variable/method names
- [ ] No redundant code
- [ ] Proper use of OOP principles
- [ ] Appropriate data types used

### Documentation (3 marks)
- [ ] Comments explain design decisions
- [ ] Docstrings for classes and methods
- [ ] Known issues documented
- [ ] Reflection on implementation

### Weekly Submissions (3 marks)
- [ ] Week 7 submission (50+ lines)
- [ ] Week 8 submission (50+ lines)
- [ ] Week 9 submission (50+ lines)

## Common Issues to Check

1. **File Not Found**: Ensure file paths are correct
2. **Data Format**: Check CSV format matches specification
3. **ID Conflicts**: Customer/product numbers should be unique
4. **Stock Management**: Stock reduces after orders
5. **Discount Calculation**: Verify percentages are correct
6. **Bundle Pricing**: Should be exactly 80% of components
7. **VIP Threshold**: Applies to all VIP members
8. **Date Format**: dd/mm/yyyy HH:MM:SS
9. **File Updates**: Files saved on exit
10. **Exception Messages**: Clear and helpful

## Performance Tips

1. Test with small datasets first
2. Use the test_program.py for quick validation
3. Check output files after program exit
4. Test edge cases (empty files, invalid data)
5. Verify all menu options work

## Submission Checklist

- [ ] File named correctly: ProgFunA2_<StudentID>.py
- [ ] Program is in ONE Python file
- [ ] No external libraries except sys, datetime, copy, os
- [ ] All comments included in the code
- [ ] Code runs without errors
- [ ] All levels implemented (PASS, CREDIT, DI, HD)
- [ ] Weekly submissions completed
- [ ] Tested with provided sample files
- [ ] Final submission before deadline
