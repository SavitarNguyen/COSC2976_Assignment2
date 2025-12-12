"""
COSC2976 - Assignment 2 - WEEK 8 SUBMISSION (CREDIT LEVEL)
Author: Student ID s1234567

"""

import sys
import os


# ==================== CUSTOM EXCEPTIONS (CREDIT LEVEL) ====================
# These custom exceptions provide specific error handling for various validation scenarios

class InvalidProductError(Exception):
    """Raised when a product does not exist in the system"""
    pass


class InvalidQuantityError(Exception):
    """Raised when product quantity is invalid (non-integer, negative, zero, or exceeds stock)"""
    pass


class InvalidMembershipAnswerError(Exception):
    """Raised when user enters invalid answer for membership question (not 'y' or 'n')"""
    pass


class InvalidMembershipTypeError(Exception):
    """Raised when user enters invalid membership type (not 'M' or 'V')"""
    pass


class InvalidFileFormatError(Exception):
    """Raised when data files have incorrect format or invalid data"""
    pass


class InvalidDiscountRateError(Exception):
    """Raised when discount rate input is invalid (non-number or negative)"""
    pass


class InvalidThresholdError(Exception):
    """Raised when threshold input is invalid (non-number, zero, or negative)"""
    pass


class InvalidPriceError(Exception):
    """Raised when product price is not set, zero, or negative"""
    pass


class InvalidCustomerError(Exception):
    """Raised when customer does not exist or is not a VIP member"""
    pass


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
        """Display VIP member information"""
        print(f"ID: {self.get_ID()}, Name: {self.get_name()}, Discount: {self.__rate1} (rate1), {self.__rate2} (rate2), Threshold: {self.__threshold}, Value: {self.get_value()}")


# ==================== PRODUCT CLASSES (PASS & CREDIT LEVEL) ====================

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
        """
        Update the product price.
        Args: price (float): New price (must be positive)
        Raises: InvalidPriceError: If price is zero or negative
        """
        if price <= 0:
            raise InvalidPriceError("Product price must be positive.")
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
        Args: quantity (int): Amount to reduce from stock
        """
        self.__stock -= quantity

    def display_info(self):
        """Display product information"""
        print(f"ID: {self.__ID}, Name: {self.__name}, Price: {self.__price}, Stock: {self.__stock}")


class Bundle(Product):
    """
    Represents a product bundle (CREDIT LEVEL).
    A bundle is a collection of products sold together at a discounted price.
    Bundle price is automatically set to 80% of the sum of component prices.
    Attributes: components (list): List of Product objects included in the bundle
    """

    def __init__(self, ID, name, stock, components):
        """
        Initialize a Bundle.
        Args:
            ID (str): Bundle ID starting with 'B'
            name (str): Bundle name
            stock (int): Bundle stock quantity
            components (list): List of Product objects in the bundle
        """
        self.__components = components
        # Calculate bundle price as 80% of component prices
        total_price = sum(component.get_price() for component in components)
        bundle_price = total_price * 0.8
        super().__init__(ID, name, bundle_price, stock)

    def get_components(self):
        """Return the list of component products"""
        return self.__components

    def display_info(self):
        """Display bundle information including components"""
        component_ids = ", ".join([comp.get_ID() for comp in self.__components])
        print(f"ID: {self.get_ID()}, Name: {self.get_name()}, Components: [{component_ids}], Price: {self.get_price()}, Stock: {self.get_stock()}")


# ==================== ORDER CLASS (PASS LEVEL - Single Item) ====================

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

        # Reduce product stock
        self.__product.reduce_stock(self.__quantity)

        return (discount_rate, final_price)


# ==================== RECORDS CLASS (PASS & CREDIT LEVEL) ====================

class Records:
    """
    Central repository for managing customers and products.
    This class handles file I/O and data management operations.
    Attributes: customers (list): List of Customer objects, products (list): List of Product objects
    """

    def __init__(self):
        """Initialize empty records"""
        self.__customers = []
        self.__products = []

    def get_customers(self):
        """Return the list of customers"""
        return self.__customers

    def get_products(self):
        """Return the list of products"""
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
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue

                    parts = [part.strip() for part in line.split(',')]

                    if len(parts) < 4:
                        raise InvalidFileFormatError(f"Line {line_num}: Expected at least 4 fields, got {len(parts)}")

                    customer_id = parts[0]
                    name = parts[1]

                    # Validate discount_rate
                    try:
                        discount_rate = float(parts[2])
                    except ValueError:
                        raise InvalidFileFormatError(f"Line {line_num}: Invalid discount_rate '{parts[2]}' - must be a number")

                    # Validate value is a number
                    try:
                        value = float(parts[3])
                    except ValueError:
                        raise InvalidFileFormatError(f"Line {line_num}: Invalid value '{parts[3]}' - must be a number")

                    # Create appropriate customer type
                    if customer_id.startswith('C'):
                        customer = Customer(customer_id, name, value)
                    elif customer_id.startswith('M'):
                        customer = Member(customer_id, name, value)
                    elif customer_id.startswith('V'):
                        customer = VIPMember(customer_id, name, value, discount_rate)
                    else:
                        raise InvalidFileFormatError(f"Line {line_num}: Invalid customer ID prefix '{customer_id[0]}' - must be C, M, or V")

                    self.add_customer(customer)

        except FileNotFoundError:
            raise InvalidFileFormatError(f"File not found: {filename}")
        except Exception as e:
            if isinstance(e, InvalidFileFormatError):
                raise
            raise InvalidFileFormatError(f"Error reading {filename}: {str(e)}")

    def read_products(self, filename="products.txt"):
        """
        Read products from CSV file and populate product list.

        File format: ID, name, price, stock

        Args: filename (str):
        """
        try:
            # First pass: read all regular products
            bundle_lines = []
            with open(filename, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue

                    parts = [part.strip() for part in line.split(',')]

                    if len(parts) < 4:
                        raise InvalidFileFormatError(f"Line {line_num}: Expected at least 4 fields, got {len(parts)}")

                    product_id = parts[0]
                    name = parts[1]

                    if product_id.startswith('P'):
                        # Regular product: ID, name, price, stock
                        # CREDIT LEVEL: Accept empty/invalid prices, will be validated during order
                        try:
                            if parts[2].strip() == "":
                                price = 0.0  # Empty price allowed
                            else:
                                price = float(parts[2])
                                # Note: Negative/zero prices allowed in file
                        except ValueError:
                            raise InvalidFileFormatError(f"Line {line_num}: Invalid price '{parts[2]}' - must be a number")

                        # Validate stock
                        try:
                            stock = int(parts[3])
                        except ValueError:
                            raise InvalidFileFormatError(f"Line {line_num}: Invalid stock '{parts[3]}' - must be an integer")

                        product = Product(product_id, name, price, stock)
                        self.add_product(product)

                    elif product_id.startswith('B'):
                        # Bundle: ID, name, component1, component2, ..., stock
                        # Save for second pass after all products are loaded
                        bundle_lines.append((line_num, parts))
                    else:
                        raise InvalidFileFormatError(f"Line {line_num}: Invalid product ID prefix '{product_id[0]}' - must be P or B")

            # Second pass: create bundles now that all products exist
            for line_num, parts in bundle_lines:
                product_id = parts[0]
                name = parts[1]

                # Last field is stock
                try:
                    stock = int(parts[-1])
                except ValueError:
                    raise InvalidFileFormatError(f"Line {line_num}: Invalid stock '{parts[-1]}' - must be an integer")

                # Component IDs are everything between name and stock
                component_ids = [cid.strip() for cid in parts[2:-1]]
                if not component_ids:
                    raise InvalidFileFormatError(f"Line {line_num}: Bundle requires at least one component")

                components = []
                for comp_id in component_ids:
                    comp = self.find_product(comp_id)
                    if not comp:
                        raise InvalidFileFormatError(f"Line {line_num}: Component '{comp_id}' not found")
                    if isinstance(comp, Bundle):
                        raise InvalidFileFormatError(f"Line {line_num}: Bundle cannot contain another bundle")
                    components.append(comp)

                bundle = Bundle(product_id, name, stock, components)
                self.add_product(bundle)

        except FileNotFoundError:
            raise InvalidFileFormatError(f"File not found: {filename}")
        except Exception as e:
            if isinstance(e, InvalidFileFormatError):
                raise
            raise InvalidFileFormatError(f"Error reading {filename}: {str(e)}")

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


# ==================== OPERATIONS CLASS (PASS & CREDIT LEVEL) ====================

class Operations:
    """
    Main class for the retail management system operations.
    Handles user interface and business logic for PASS and CREDIT level features.
    """

    def __init__(self, customer_file="customers.txt", product_file="products.txt"):
        """
        Initialize the Operations system.

        Args: customer_file (str), product_file (str)
        """
        self.__records = Records()
        self.__customer_file = customer_file
        self.__product_file = product_file
        self.__next_customer_number = 1

    def initialize(self):
        """
        Initialize the system by loading data from files.
        Returns: bool: True if initialization successful, False otherwise
        """
        try:
            # Check if files exist
            if not os.path.exists(self.__customer_file):
                print(f"Error: {self.__customer_file} is missing.")
                return False
            if not os.path.exists(self.__product_file):
                print(f"Error: {self.__product_file} is missing.")
                return False

            # Read customer file with exception handling
            try:
                self.__records.read_customers(self.__customer_file)
            except InvalidFileFormatError as e:
                print(f"Error in {self.__customer_file}: {e}")
                return False

            # Read product file with exception handling
            try:
                self.__records.read_products(self.__product_file)
            except InvalidFileFormatError as e:
                print(f"Error in {self.__product_file}: {e}")
                return False

            # Determine next customer number
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
        Handle place order operation (CREDIT LEVEL with exception handling).
        Supports single item per order.
        """
        try:
            # Get product identifier
            product_id = input("\nEnter the name or ID of the product you want to buy: ").strip()
            product = self.__records.find_product(product_id)

            if not product:
                raise InvalidProductError(f"Product '{product_id}' does not exist.")

            # Validate product has positive price
            if product.get_price() <= 0:
                raise InvalidPriceError("This product cannot be sold (price not set or invalid).")

            # Get quantity with validation
            quantity_str = input("Enter the quantity: ").strip()
            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    raise InvalidQuantityError("Quantity must be a positive integer.")
                if quantity > product.get_stock():
                    raise InvalidQuantityError(f"Insufficient stock. Available: {product.get_stock()}")
            except ValueError:
                raise InvalidQuantityError("Quantity must be a valid integer.")

            # Ask about existing customer
            existing_answer = input("Are you an existing customer? (y/n): ").strip().lower()
            if existing_answer not in ['y', 'n']:
                raise InvalidMembershipAnswerError("Please answer 'y' or 'n'.")

            customer = None

            if existing_answer == 'y':
                # Existing customer
                customer_id = input("Enter your name or ID: ").strip()
                customer = self.__records.find_customer(customer_id)

                if not customer:
                    raise InvalidCustomerError(f"Customer '{customer_id}' does not exist.")

            else:
                # New customer
                name = input("Enter your name: ").strip()

                # Check if name already exists
                if self.__records.find_customer(name):
                    raise InvalidCustomerError(f"Customer with name '{name}' already exists.")

                # Ask about membership
                membership_answer = input("Do you want to be a member? (y/n): ").strip().lower()
                if membership_answer not in ['y', 'n']:
                    raise InvalidMembershipAnswerError("Please answer 'y' or 'n'.")

                if membership_answer == 'n':
                    # Create normal customer
                    customer_id = f"C{self.__next_customer_number}"
                    customer = Customer(customer_id, name, 0.0)
                    self.__records.add_customer(customer)
                    self.__next_customer_number += 1

                else:
                    # Ask for membership type
                    membership_type = input("Which level of membership do you want? (M/V): ").strip().upper()
                    if membership_type not in ['M', 'V']:
                        raise InvalidMembershipTypeError("Please enter 'M' for Member or 'V' for VIP.")

                    if membership_type == 'M':
                        # Create Member
                        customer_id = f"M{self.__next_customer_number}"
                        customer = Member(customer_id, name, 0.0)
                        self.__records.add_customer(customer)
                        self.__next_customer_number += 1

                    else:
                        # Create VIP Member with custom rate
                        rate_str = input("Enter the first discount rate (e.g., 0.10 for 10%): ").strip()
                        try:
                            rate1 = float(rate_str)
                            if rate1 < 0:
                                raise InvalidDiscountRateError("Discount rate cannot be negative.")
                        except ValueError:
                            raise InvalidDiscountRateError("Discount rate must be a valid number.")

                        customer_id = f"V{self.__next_customer_number}"
                        customer = VIPMember(customer_id, name, 0.0, rate1)
                        self.__records.add_customer(customer)
                        self.__next_customer_number += 1

            # Create and process order
            order = Order(customer, product, quantity)
            discount_rate, final_price = order.process_order()

            # Display order confirmation
            print("\n" + "=" * 60)
            print("Order placed successfully!")
            print(f"Customer: {customer.get_name()} ({customer.get_ID()})")
            print(f"Product: {product.get_name()} ({product.get_ID()})")
            print(f"Quantity: {quantity}")
            print(f"Unit Price: ${product.get_price():.2f}")
            print(f"Subtotal: ${order.calculate_total():.2f}")
            print(f"Discount: {discount_rate * 100:.1f}%")
            print(f"Total Price: ${final_price:.2f}")
            print("=" * 60 + "\n")

        except InvalidProductError as e:
            print(f"\nError: {e}\n")
        except InvalidQuantityError as e:
            print(f"\nError: {e}\n")
        except InvalidMembershipAnswerError as e:
            print(f"\nError: {e}\n")
        except InvalidMembershipTypeError as e:
            print(f"\nError: {e}\n")
        except InvalidCustomerError as e:
            print(f"\nError: {e}\n")
        except InvalidDiscountRateError as e:
            print(f"\nError: {e}\n")
        except InvalidPriceError as e:
            print(f"\nError: {e}\n")
        except Exception as e:
            print(f"\nUnexpected error: {e}\n")

    def display_customers(self):
        """Display all customers"""
        self.__records.list_customers()

    def display_products(self):
        """Display all products"""
        self.__records.list_products()

    def run(self):
        """Main program loop"""
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
    customer_file = "customers.txt"
    product_file = "products.txt"

    # Handle command-line arguments (CREDIT LEVEL - 2 files only)
    if len(sys.argv) == 1:
        # Use default files
        pass
    elif len(sys.argv) == 3:
        customer_file = sys.argv[1]
        product_file = sys.argv[2]
    else:
        print("Usage:")
        print(f"  {sys.argv[0]}                                    # Use default files")
        print(f"  {sys.argv[0]} <customer_file> <product_file>     # Specify files")
        sys.exit(1)

    operations = Operations(customer_file, product_file)

    if operations.initialize():
        operations.run()
    else:
        print("Failed to initialize the system. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
