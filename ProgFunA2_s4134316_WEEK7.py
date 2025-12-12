"""
COSC2976 - Assignment 2 - WEEK 7 SUBMISSION (PASS LEVEL)
Author: Student ID s1234567
"""

import sys
import os
# ==================== CUSTOMER CLASSES (PASS LEVEL) ====================

class Customer:
    """
    Showing a normal customer without membership and also a foundation for Member and VIPMember subclasses.
    Attributes: ID (str, starts with C), name (str), Customer name (unique, no digits), value (float): Total money customer has spent to date
    """

    def __init__(self, ID, name, value):
        """Create a Customer with ID, name, and total value spent"""
        self.__ID = ID
        self.__name = name
        self.__value = value

    def get_ID(self):
        """Return the customer ID"""
        return self.__ID

    def get_name(self):
        """Return the customer name"""
        return self.__name

    def get_value(self):
        """Return the total value spent by customer"""
        return self.__value

    def set_value(self, value):
        """Update the total value spent by customer"""
        self.__value = value

    def get_discount(self, price):
        """
        Calculate discount for normal customers (0% for normal customers).
        Args: price (float): Original price before discount
        Returns: tuple: (discount_rate, price_after_discount)
        """
        return (0, price)

    def display_info(self):
        """Display customer information including ID, name, discount rate, and total value spent"""
        discount_rate, _ = self.get_discount(0)
        print(f"ID: {self.__ID}, Name: {self.__name}, Discount: {discount_rate}, Value: {self.__value}")


class Member(Customer):
    """
    Showing a customer with normal membership (with a flat discount rate on all orders (default 5%).
    The flat rate is a class variable shared by all Member instances,
    allowing store-wide discount adjustments.
    """

    # Class variable: discount rate shared by all members
    __discount_rate = 0.05  # Default 5%
    def __init__(self, ID, name, value):
        """Initialize a Member - ID starts with 'M'"""
        super().__init__(ID, name, value)

    @classmethod
    def get_discount_rate(cls):
        """Return the current flat discount rate for all members"""
        return cls.__discount_rate

    @classmethod
    def set_rate(cls, rate):
        """
        Adjust the flat discount rate for all members.
        This is a class method that affects all Member instances.
        Args: rate (float): New discount rate (e.g., 0.05 for 5%)
        """
        cls.__discount_rate = rate

    def get_discount(self, price):
        """
        Calculate discount for members with flat rate.
        Args: price (float): Original price before discount
        Returns: tuple: (discount_rate, price_after_discount)
        """
        discounted_price = price * (1 - self.__discount_rate)
        return (self.__discount_rate, discounted_price)

    def display_info(self):
        """Display member information"""
        print(f"ID: {self.get_ID()}, Name: {self.get_name()}, Discount: {self.__discount_rate}, Value: {self.get_value()}")


class VIPMember(Customer):
    """
    Shows a customer with VIP membership.
    VIP members have two-tier discount rates based on order price threshold.
    - First discount rate: applies when order price <= threshold
    - Second discount rate: applies when order price > threshold
    - Second rate is always 5% higher than first rate
    - Threshold is shared by all VIP members (class variable)
    - Discount rates are individual per VIP member (instance variables)
    """

    # Class variable: threshold shared by all VIP members
    __threshold = 1000.0  # Default threshold

    def __init__(self, ID, name, value, rate1=0.10):
        """
        Initialize a VIP Member.
        Args:
            ID (str): Customer ID starting with 'V'
            name (str): Customer name
            value (float): Total value spent
            rate1 (float): First discount rate (default 10%)
        """
        super().__init__(ID, name, value)
        self.__rate1 = rate1  # Instance variable - can be different for each VIP member
        self.__rate2 = rate1 + 0.05  # Second rate is always 5% higher

    def get_rate1(self):
        """Return the first discount rate"""
        return self.__rate1

    def get_rate2(self):
        """Return the second discount rate"""
        return self.__rate2

    @classmethod
    def get_threshold(cls):
        """Return the threshold that applies to all VIP members"""
        return cls.__threshold

    @classmethod
    def set_threshold(cls, threshold):
        """
        Adjust the threshold for all VIP members.
        Args:
            threshold (float): New threshold value
        """
        cls.__threshold = threshold

    def set_rate(self, rate1):
        """
        Adjust the discount rates for this individual VIP member.
        Args: rate1 (float): New first discount rate
        """
        self.__rate1 = rate1
        self.__rate2 = rate1 + 0.05

    def get_discount(self, price):
        """
        Calculate discount for VIP members based on two-tier system.
        Args: price (float): Original price before discount
        Returns: tuple: (applicable_discount_rate, price_after_discount)
        """
        if price <= self.__threshold:
            # Use first rate for orders at or below threshold
            discounted_price = price * (1 - self.__rate1)
            return (self.__rate1, discounted_price)
        else:
            # Use second rate for orders exceeding threshold
            discounted_price = price * (1 - self.__rate2)
            return (self.__rate2, discounted_price)

    def display_info(self):
        """Display VIP member information including both rates and threshold"""
        print(f"ID: {self.get_ID()}, Name: {self.get_name()}, Discount: {self.__rate1} (rate1), {self.__rate2} (rate2), Threshold: {self.__threshold}, Value: {self.get_value()}")


# ==================== PRODUCT CLASS (PASS LEVEL) ====================

class Product:
    """
    Represents a product sold in the store.
    Attributes:
        ID (str): Unique product identifier starting with 'P'
        name (str): Product name (unique, no digits)
        price (float): Unit price per product
        stock (int): Quantity available in stock
    """

    def __init__(self, ID, name, price, stock):
        """Initialize a Product with ID, name, price, and stock quantity"""
        self.__ID = ID
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_ID(self):
        """Return the product ID"""
        return self.__ID

    def get_name(self):
        """Return the product name"""
        return self.__name

    def get_price(self):
        """Return the product price"""
        return self.__price

    def set_price(self, price):
        """Update the product price"""
        self.__price = price

    def get_stock(self):
        """Return the current stock quantity"""
        return self.__stock

    def set_stock(self, stock):
        """Update the stock quantity"""
        self.__stock = stock

    def reduce_stock(self, quantity):
        """
        Reduce stock by specified quantity after an order.

        Args:
            quantity (int): Amount to reduce from stock
        """
        self.__stock -= quantity

    def display_info(self):
        """Display product information"""
        print(f"ID: {self.__ID}, Name: {self.__name}, Price: {self.__price}, Stock: {self.__stock}")


# ==================== ORDER CLASS (PASS LEVEL) ====================

class Order:
    """
    Represents a customer order.
    This class handles order processing, including:
    - Customer information
    - Single product per order
    - Discount calculation
    - Stock updates
    """

    def __init__(self, customer, product, quantity):
        """
        Initialize an Order.

        Args:
            customer (Customer): The customer placing the order
            product (Product): The product being ordered
            quantity (int): Quantity of the product
        """
        self.__customer = customer
        self.__product = product
        self.__quantity = quantity

    def get_customer(self):
        """Return the customer"""
        return self.__customer

    def get_product(self):
        """Return the product"""
        return self.__product

    def get_quantity(self):
        """Return the quantity"""
        return self.__quantity

    def calculate_total(self):
        """
        Calculate the total price before discount.

        Returns: float: Total price (price * quantity)
        """
        return self.__product.get_price() * self.__quantity

    def process_order(self):
        """
        Process the order:
        1. Calculate total price
        2. Apply discount based on customer type
        3. Update customer's total value
        4. Reduce product stock

        Returns: tuple: (discount_rate, total_price_after_discount)
        """
        total_price = self.calculate_total()

        # Apply customer discount
        discount_rate, final_price = self.__customer.get_discount(total_price)

        # Update customer value
        self.__customer.set_value(self.__customer.get_value() + final_price)

        # Reduce stock
        self.__product.reduce_stock(self.__quantity)

        return (discount_rate, final_price)


# ==================== RECORDS CLASS (PASS LEVEL) ====================

class Records:
    """
    Central data repository for the retail management system.

    This class manages:
    - Customer list (Customer, Member, VIPMember objects)
    - Product list (Product objects)

    It provides methods for:
    - Reading data from CSV files
    - Searching for customers and products
    - Displaying information
    """

    def __init__(self):
        """Initialize empty lists for customers and products"""
        self.__customers = []  # List of Customer/Member/VIPMember objects
        self.__products = []   # List of Product objects

    def get_customers(self):
        """Return the list of all customers"""
        return self.__customers

    def get_products(self):
        """Return the list of all products"""
        return self.__products

    def add_customer(self, customer):
        """Add a customer to the records"""
        self.__customers.append(customer)

    def add_product(self, product):
        """Add a product to the records"""
        self.__products.append(product)

    def read_customers(self, filename="customers.txt"):
        """
        Read customers from CSV file and populate customer list.

        File format: ID, name, discount_rate, value
        - ID starting with 'C': Normal Customer
        - ID starting with 'M': Member
        - ID starting with 'V': VIP Member (first discount rate stored)

        Args: filename (str)
        """
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue

                    parts = [part.strip() for part in line.split(',')]
                    if len(parts) < 4:  # Skip malformed lines
                        continue

                    ID, name, discount_str, value_str = parts[0], parts[1], parts[2], parts[3]

                    discount_rate = float(discount_str) if discount_str else 0.0
                    value = float(value_str) if value_str else 0.0

                    # Create appropriate customer type based on ID prefix
                    if ID[0] == 'C':
                        customer = Customer(ID, name, value)
                    elif ID[0] == 'M':
                        customer = Member(ID, name, value)
                    elif ID[0] == 'V':
                        customer = VIPMember(ID, name, value, discount_rate)

                    self.__customers.append(customer)

        except FileNotFoundError:
            raise

    def read_products(self, filename="products.txt"):
        """
        Read products from CSV file and populate product list.

        File format: ID, name, price, stock

        Args: filename (str):
        """
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue

                    parts = [part.strip() for part in line.split(',')]
                    if parts[0].startswith('B'):
                        continue
                    if len(parts) < 4:  # Skip malformed lines
                        continue

                    ID, name, price_str, stock_str = parts[0], parts[1], parts[2], parts[3]
                    try:
                        price = float(price_str) if price_str.strip() != "" else 0.0
                    except ValueError:
                        price = 0.0
                    try:
                        stock = int(stock_str) if stock_str.strip() != "" else 0
                    except ValueError:
                        stock = 0

                    product = Product(ID, name, price, stock)
                    self.__products.append(product)

        except FileNotFoundError:
            raise

    def find_customer(self, identifier):
        """
        Search for a customer by ID or name.

        Args: identifier (str): Customer ID or name

        Returns: Customer object if found, None otherwise
        """
        for customer in self.__customers:
            if customer.get_ID() == identifier or customer.get_name() == identifier:
                return customer
        return None

    def find_product(self, identifier):
        """
        Search for a product by ID or name.
        Args: identifier (str): Product ID or name

        Returns: Product object if found, None otherwise
        """
        for product in self.__products:
            if product.get_ID() == identifier or product.get_name() == identifier:
                return product
        return None

    def list_customers(self):
        """Display all customers with their information"""
        print("\n========== CUSTOMER LIST ==========")
        for customer in self.__customers:
            customer.display_info()
        print("===================================\n")

    def list_products(self):
        """Display all products with their information"""
        print("\n========== PRODUCT LIST ==========")
        for product in self.__products:
            product.display_info()
        print("==================================\n")


# ==================== OPERATIONS CLASS (PASS LEVEL) ====================

class Operations:
    """
    Main class for the retail management system operations.

    This class provides the menu-driven interface for:
    - Placing orders
    - Displaying customers and products
    - Managing data files
    """

    def __init__(self, customer_file="customers.txt", product_file="products.txt"):
        """
        Initialize the Operations system.

        Args: customer_file (str), product_file (str)
        """
        self.__records = Records()
        self.__customer_file = customer_file
        self.__product_file = product_file

        # Generate next customer ID
        self.__next_customer_number = 1

    def initialize(self):
        """
        Initialize the system by loading data from files.
        Returns: bool: True if initialization successful, False otherwise
        """
        try:
            # Check if customer and product files exist (mandatory)
            if not os.path.exists(self.__customer_file):
                print(f"Error: {self.__customer_file} is missing.")
                return False

            if not os.path.exists(self.__product_file):
                print(f"Error: {self.__product_file} is missing.")
                return False

            # Read customer and product files
            self.__records.read_customers(self.__customer_file)
            self.__records.read_products(self.__product_file)

            # Calculate next customer ID number
            customers = self.__records.get_customers()
            if customers:
                max_num = 0
                for customer in customers:
                    customer_id = customer.get_ID()
                    num_str = customer_id[1:]
                    try:
                        num = int(num_str)
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        pass
                self.__next_customer_number = max_num + 1

            return True

        except Exception as e:
            print(f"Unexpected error during initialization: {e}")
            return False

    def display_menu(self):
        """Display the main menu"""
        print("\nWelcome to the RMIT retail management system!")
        print("\n" + "=" * 60)
        print("You can choose from the following options:")
        print("1: Place an order")
        print("2: Display existing customers")
        print("3: Display existing products")
        print("0: Exit the program")
        print("=" * 60)

    def place_order(self):
        """
        Handle the place order operation (PASS LEVEL).
        Process:
        1. Get customer name
        2. Check if customer exists or create new customer
        3. Get product and quantity
        4. Process order and display receipt
        """
        # Get customer name
        customer_name = input("\nEnter the name of the customer [e.g. Huong]: ").strip()

        # Find or create customer
        customer = self.__records.find_customer(customer_name)
        is_new_customer = (customer is None)

        # Get product (PASS LEVEL: assume valid input)
        product_input = input("\nEnter the product [enter a valid product only, e.g. shirt, towel, oven, kettle]: ").strip()
        product = self.__records.find_product(product_input)

        # Get quantity (PASS LEVEL: assume valid input)
        quantity_input = input("\nEnter the product quantity [enter a positive integer only, e.g. 1, 2, 3]: ").strip()
        quantity = int(quantity_input)

        # Handle new customer
        if is_new_customer:
            # Ask about membership (PASS LEVEL: assume valid y/n input)
            membership_input = input("\nThis is a new customer. Does the customer want to have a membership [enter y or n]? ").strip().lower()

            # Create customer based on membership choice
            if membership_input == 'n':
                # Normal customer
                customer_id = f"C{self.__next_customer_number}"
                customer = Customer(customer_id, customer_name, 0)
                self.__records.add_customer(customer)
                self.__next_customer_number += 1
                membership_fee = 0
            else:  # membership_input == 'y' (PASS LEVEL: assume valid input)
                # Ask membership type (PASS LEVEL: assume valid M/V input)
                membership_type = input("\nWhat kind of membership the customer wants? ").strip().upper()

                if membership_type == 'M':
                    # Normal member
                    customer_id = f"M{self.__next_customer_number}"
                    customer = Member(customer_id, customer_name, 0)
                    self.__records.add_customer(customer)
                    self.__next_customer_number += 1
                    membership_fee = 0
                else:  # membership_type == 'V' (PASS LEVEL: assume valid input)
                    # VIP member
                    customer_id = f"V{self.__next_customer_number}"
                    customer = VIPMember(customer_id, customer_name, 0)
                    self.__records.add_customer(customer)
                    self.__next_customer_number += 1
                    membership_fee = 200.0
        else:
            membership_fee = 0

        # Create and process order
        order = Order(customer, product, quantity)
        discount_rate, total_after_discount = order.process_order()

        # Add membership fee if applicable
        if membership_fee > 0:
            customer.set_value(customer.get_value() + membership_fee)

        # Display receipt
        print("\n" + "-" * 50)
        print(f"{customer_name} purchases {quantity} x {product.get_name()}.")
        print(f"Unit price: {product.get_price()} (AUD)")

        # Display membership fee if applicable
        if membership_fee > 0:
            print(f"Membership price: {membership_fee} (AUD)")

        # Display discount and total
        print(f"{customer_name} gets a discount of {discount_rate * 100} %.")

        final_total = total_after_discount + membership_fee
        print(f"Total price: {final_total} (AUD)")
        print("-" * 50)

    def display_customers(self):
        """Display all customers (PASS LEVEL)"""
        self.__records.list_customers()

    def display_products(self):
        """Display all products (PASS LEVEL)"""
        self.__records.list_products()

    def run(self):
        """
        Main program loop.

        Displays menu and processes user choices until exit.
        """
        while True:
            self.display_menu()

            choice = input("\nChoose one option: ").strip()

            if choice == '1':
                self.place_order()
            elif choice == '2':
                self.display_customers()
            elif choice == '3':
                self.display_products()
            elif choice == '0':
                print("\nThank you for using the RMIT retail management system. Goodbye!")
                break
            else:
                print("\nInvalid option. Please try again.")


# ==================== MAIN PROGRAM ====================

def main():
    """
    Main entry point for the program.
    """
    # Default file names
    customer_file = "customers.txt"
    product_file = "products.txt"

    # Parse command-line arguments
    if len(sys.argv) == 1:
        # No arguments - use defaults
        pass
    elif len(sys.argv) == 3:
        # Two arguments: customer and product files
        customer_file = sys.argv[1]
        product_file = sys.argv[2]
    else:
        # Wrong number of arguments
        print("Usage:")
        print(f"  {sys.argv[0]}                                    # Use default files")
        print(f"  {sys.argv[0]} <customer_file> <product_file>     # Specify files")
        sys.exit(1)

    # Create and initialize operations
    operations = Operations(customer_file, product_file)

    if operations.initialize():
        operations.run()
    else:
        print("Failed to initialize the system. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
