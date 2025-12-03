"""
Test script for Assignment 2
This script tests various features of the program
"""

import subprocess
import os

def test_pass_level():
    """Test PASS level with display options"""
    print("=" * 60)
    print("TESTING PASS LEVEL")
    print("=" * 60)

    # Test displaying customers
    process = subprocess.Popen(
        ['python3', 'ProgFunA2_s1234567.py', 'files_PASSlevel/customers.txt', 'files_PASSlevel/products.txt'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Choose option 2 (display customers) then exit
    output, errors = process.communicate(input='2\n0\n')
    print("Display Customers Test:")
    print(output)
    if errors:
        print("Errors:", errors)
    print()

def test_credit_level():
    """Test CREDIT level with bundles"""
    print("=" * 60)
    print("TESTING CREDIT LEVEL")
    print("=" * 60)

    # Test displaying products with bundles
    process = subprocess.Popen(
        ['python3', 'ProgFunA2_s1234567.py', 'files_CREDITlevel/customers.txt', 'files_CREDITlevel/products.txt'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Choose option 3 (display products) then exit
    output, errors = process.communicate(input='3\n0\n')
    print("Display Products with Bundles Test:")
    print(output)
    if errors:
        print("Errors:", errors)
    print()

def test_di_level():
    """Test DI level with orders"""
    print("=" * 60)
    print("TESTING DI LEVEL")
    print("=" * 60)

    # Test displaying orders
    process = subprocess.Popen(
        ['python3', 'ProgFunA2_s1234567.py', 'files_DIlevel/customers.txt', 'files_DIlevel/products.txt', 'files_DIlevel/orders.txt'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Choose option 6 (display all orders) then exit
    output, errors = process.communicate(input='6\n0\n')
    print("Display All Orders Test:")
    print(output)
    if errors:
        print("Errors:", errors)
    print()

def test_hd_level():
    """Test HD level with summary"""
    print("=" * 60)
    print("TESTING HD LEVEL")
    print("=" * 60)

    # Test order summary
    process = subprocess.Popen(
        ['python3', 'ProgFunA2_s1234567.py', 'files_HDlevel/customers.txt', 'files_HDlevel/products.txt', 'files_HDlevel/orders.txt'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Choose option 8 (summarize orders), 9 (most valuable customer), 10 (most popular product), then exit
    output, errors = process.communicate(input='8\n9\n10\n0\n')
    print("Order Summary, Most Valuable Customer, Most Popular Product Tests:")
    print(output)
    if errors:
        print("Errors:", errors)
    print()

if __name__ == "__main__":
    os.chdir('/Users/tysonnguyen/Downloads/COSC2976_Assignment2')

    print("\n" + "=" * 60)
    print("ASSIGNMENT 2 - COMPREHENSIVE TEST SUITE")
    print("=" * 60 + "\n")

    test_pass_level()
    test_credit_level()
    test_di_level()
    test_hd_level()

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)
