"""
COSC2976 Programming Fundamentals - Assignment 2
Retail Management System using Object-Oriented Programming

This program implements a comprehensive retail management system for a department store.
It supports customer management (normal customers, members, VIP members), product management
(regular products and bundles), and order processing with discount calculations.

Author: Student ID s4134316
Libraries used: sys (command-line arguments), datetime (order timestamps), copy (deep copying objects), os (file operations)
"""

import sys
from datetime import datetime
import copy
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
    Base class representing a normal customer without membership.
    This class stores basic customer information and provides foundation for Member and VIPMember subclasses.

    Attributes:
        ID (str): Unique customer identifier starting with 'C'
        name (str): Customer name (unique, no digits)
        value (float): Total money customer has spent to date
    """

    def __init__(self, ID, name, value):
        """Initialize a Customer with ID, name, and total value spent"""
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
        Calculate discount for normal customers.
        Normal customers receive no discount (0%).

        Args:
            price (float): Original price before discount

        Returns:
            tuple: (discount_rate, price_after_discount)
        """
        return (0, price)

    def display_info(self):
        """Display customer information including ID, name, discount rate, and total value spent"""
        discount_rate, _ = self.get_discount(0)
        print(f"ID: {self.__ID}, Name: {self.__name}, Discount: {discount_rate}, Value: {self.__value}")


class Member(Customer):
    """
    Represents a customer with normal membership.
    Members receive a flat discount rate on all orders (default 5%).

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

        Args:
            rate (float): New discount rate (e.g., 0.05 for 5%)
        """
        cls.__discount_rate = rate

    def get_discount(self, price):
        """
        Calculate discount for members with flat rate.

        Args:
            price (float): Original price before discount

        Returns:
            tuple: (discount_rate, price_after_discount)
        """
        discounted_price = price * (1 - self.__discount_rate)
        return (self.__discount_rate, discounted_price)

    def display_info(self):
        """Display member information"""
        print(f"ID: {self.get_ID()}, Name: {self.get_name()}, Discount: {self.__discount_rate}, Value: {self.get_value()}")


class VIPMember(Customer):
    """
    Represents a customer with VIP membership.
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

        Args:
            rate1 (float): New first discount rate
        """
        self.__rate1 = rate1
        self.__rate2 = rate1 + 0.05

    def get_discount(self, price):
        """
        Calculate discount for VIP members based on two-tier system.

        Args:
            price (float): Original price before discount

        Returns:
            tuple: (applicable_discount_rate, price_after_discount)
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


class Bundle(Product):
    """
    Represents a bundle of products sold together as one unit (CREDIT LEVEL).

    A bundle consists of multiple existing products offered at a discounted price.
    Bundle price is 80% of the total price of all component products.

    Attributes:
        components (list): List of Product objects that make up the bundle
    """

    def __init__(self, ID, name, components, stock):
        """
        Initialize a Bundle.

        Args:
            ID (str): Bundle ID starting with 'B'
            name (str): Bundle name
            components (list): List of Product objects in the bundle
            stock (int): Bundle stock quantity
        """
        # Calculate bundle price as 80% of sum of component prices
        total_price = sum(comp.get_price() for comp in components)
        bundle_price = total_price * 0.8

        super().__init__(ID, name, bundle_price, stock)
        self.__components = components

    def get_components(self):
        """Return the list of component products"""
        return self.__components

    def display_info(self):
        """Display bundle information including component IDs"""
        component_ids = ', '.join([comp.get_ID() for comp in self.__components])
        print(f"ID: {self.get_ID()}, Name: {self.get_name()}, Components: [{component_ids}], Price: {self.get_price()}, Stock: {self.get_stock()}")


# ==================== ORDER CLASSES (PASS & DI LEVEL) ====================

class OrderItem:
    """
    Represents a single item in an order (HD LEVEL - for multiple items per order).

    This class encapsulates product and quantity information for one item within an order.
    """

    def __init__(self, product, quantity):
        """
        Initialize an OrderItem.

        Args:
            product (Product): The product being ordered
            quantity (int): Quantity of the product
        """
        self.__product = product
        self.__quantity = quantity

    def get_product(self):
        """Return the product"""
        return self.__product

    def get_quantity(self):
        """Return the quantity"""
        return self.__quantity

    def get_subtotal(self):
        """Calculate subtotal for this item (price * quantity)"""
        return self.__product.get_price() * self.__quantity


class Order:
    """
    Represents a customer order.

    This class handles order processing, including:
    - Customer information
    - Ordered items (single or multiple)
    - Discount calculation
    - Stock updates
    - Order timestamp (DI LEVEL)
    """

    def __init__(self, customer, items, date=None):
        """
        Initialize an Order.

        Args:
            customer (Customer): The customer placing the order
            items (list): List of OrderItem objects
            date (datetime): Order timestamp (defaults to current time)
        """
        self.__customer = customer
        self.__items = items  # List of OrderItem objects
        self.__date = date if date else datetime.now()

    def get_customer(self):
        """Return the customer"""
        return self.__customer

    def get_items(self):
        """Return the list of order items"""
        return self.__items

    def get_date(self):
        """Return the order date"""
        return self.__date

    def calculate_total(self):
        """
        Calculate the total price before discount.

        Returns:
            float: Total price of all items
        """
        return sum(item.get_subtotal() for item in self.__items)

    def process_order(self):
        """
        Process the order:
        1. Calculate total price
        2. Apply discount based on customer type
        3. Update customer's total value
        4. Reduce product stock

        Returns:
            tuple: (discount_rate, total_price_after_discount)
        """
        total_price = self.calculate_total()

        # Apply customer discount
        discount_rate, final_price = self.__customer.get_discount(total_price)

        # Update customer value
        self.__customer.set_value(self.__customer.get_value() + final_price)

        # Reduce stock for all items
        for item in self.__items:
            product = item.get_product()
            product.reduce_stock(item.get_quantity())

        return (discount_rate, final_price)


# ==================== RECORDS CLASS (PASS & DI LEVEL) ====================

class Records:
    """
    Central data repository for the retail management system.

    This class manages:
    - Customer list (Customer, Member, VIPMember objects)
    - Product list (Product and Bundle objects)
    - Order history (Order objects) - DI LEVEL

    It provides methods for:
    - Reading data from CSV files
    - Searching for customers and products
    - Displaying information
    """

    def __init__(self):
        """Initialize empty lists for customers, products, and orders"""
        self.__customers = []  # List of Customer/Member/VIPMember objects
        self.__products = []   # List of Product/Bundle objects
        self.__orders = []     # List of Order objects (DI LEVEL)

    def get_customers(self):
        """Return the list of all customers"""
        return self.__customers

    def get_products(self):
        """Return the list of all products"""
        return self.__products

    def get_orders(self):
        """Return the list of all orders"""
        return self.__orders

    def add_customer(self, customer):
        """Add a customer to the records"""
        self.__customers.append(customer)

    def add_product(self, product):
        """Add a product to the records"""
        self.__products.append(product)

    def add_order(self, order):
        """Add an order to the records (DI LEVEL)"""
        self.__orders.append(order)

    def read_customers(self, filename="customers.txt"):
        """
        Read customers from CSV file and populate customer list.

        File format: ID, name, discount_rate, value
        - ID starting with 'C': Normal Customer
        - ID starting with 'M': Member
        - ID starting with 'V': VIP Member (first discount rate stored)

        Args:
            filename (str): Name of customer file

        Raises:
            InvalidFileFormatError: If file has incorrect format or invalid data
        """
        try:
            with open(filename, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    try:
                        parts = [part.strip() for part in line.strip().split(',')]

                        if len(parts) != 4:
                            raise InvalidFileFormatError(f"Line {line_num}: Expected 4 fields, got {len(parts)}")

                        ID, name, discount_str, value_str = parts

                        # Validate ID format
                        if not ID or ID[0] not in ['C', 'M', 'V']:
                            raise InvalidFileFormatError(f"Line {line_num}: Invalid customer ID '{ID}'")

                        # Validate name (no digits)
                        if any(char.isdigit() for char in name):
                            raise InvalidFileFormatError(f"Line {line_num}: Customer name contains digits")

                        # Parse discount and value
                        try:
                            discount_rate = float(discount_str)
                            value = float(value_str)
                        except ValueError:
                            raise InvalidFileFormatError(f"Line {line_num}: Invalid number format")

                        # Create appropriate customer type based on ID prefix
                        if ID[0] == 'C':
                            customer = Customer(ID, name, value)
                        elif ID[0] == 'M':
                            customer = Member(ID, name, value)
                        elif ID[0] == 'V':
                            customer = VIPMember(ID, name, value, discount_rate)

                        self.__customers.append(customer)

                    except InvalidFileFormatError:
                        raise
                    except Exception as e:
                        raise InvalidFileFormatError(f"Line {line_num}: {str(e)}")

        except FileNotFoundError:
            raise
        except InvalidFileFormatError:
            raise
        except Exception as e:
            raise InvalidFileFormatError(f"Error reading customers file: {str(e)}")

    def read_products(self, filename="products.txt"):
        """
        Read products from CSV file and populate product list.

        File format:
        - Normal product: ID, name, price, stock
        - Bundle: ID, name, component_IDs..., stock

        Args:
            filename (str): Name of product file

        Raises:
            InvalidFileFormatError: If file has incorrect format or invalid data
        """
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            # First pass: read all normal products
            for line_num, line in enumerate(lines, 1):
                try:
                    parts = [part.strip() for part in line.strip().split(',')]

                    if len(parts) < 4:
                        raise InvalidFileFormatError(f"Line {line_num}: Not enough fields")

                    ID = parts[0]
                    name = parts[1]

                    # Validate ID
                    if not ID or ID[0] not in ['P', 'B']:
                        raise InvalidFileFormatError(f"Line {line_num}: Invalid product ID '{ID}'")

                    # Validate name (no digits)
                    if any(char.isdigit() for char in name):
                        raise InvalidFileFormatError(f"Line {line_num}: Product name contains digits")

                    # Handle normal products (P prefix)
                    if ID[0] == 'P':
                        if len(parts) != 4:
                            raise InvalidFileFormatError(f"Line {line_num}: Product should have 4 fields")

                        price_str = parts[2]
                        stock_str = parts[3]

                        # Handle empty or invalid price
                        if price_str == '':
                            price = None  # Mark as unset price
                        else:
                            try:
                                price = float(price_str)
                            except ValueError:
                                raise InvalidFileFormatError(f"Line {line_num}: Invalid price format")

                        try:
                            stock = int(stock_str)
                        except ValueError:
                            raise InvalidFileFormatError(f"Line {line_num}: Invalid stock format")

                        product = Product(ID, name, price, stock)
                        self.__products.append(product)

                except InvalidFileFormatError:
                    raise
                except Exception as e:
                    raise InvalidFileFormatError(f"Line {line_num}: {str(e)}")

            # Second pass: read bundles (after all products are loaded)
            for line_num, line in enumerate(lines, 1):
                try:
                    parts = [part.strip() for part in line.strip().split(',')]
                    ID = parts[0]

                    # Handle bundles (B prefix)
                    if ID[0] == 'B':
                        name = parts[1]
                        component_ids = parts[2:-1]  # All parts between name and stock
                        stock = int(parts[-1])

                        # Find component products
                        components = []
                        for comp_id in component_ids:
                            comp_product = self.find_product(comp_id)
                            if comp_product is None:
                                raise InvalidFileFormatError(f"Line {line_num}: Component '{comp_id}' not found")
                            if isinstance(comp_product, Bundle):
                                raise InvalidFileFormatError(f"Line {line_num}: Bundles cannot contain other bundles")
                            components.append(comp_product)

                        bundle = Bundle(ID, name, components, stock)
                        self.__products.append(bundle)

                except InvalidFileFormatError:
                    raise
                except Exception as e:
                    raise InvalidFileFormatError(f"Line {line_num}: {str(e)}")

        except FileNotFoundError:
            raise
        except InvalidFileFormatError:
            raise
        except Exception as e:
            raise InvalidFileFormatError(f"Error reading products file: {str(e)}")

    def read_orders(self, filename="orders.txt"):
        """
        Read orders from CSV file and populate order history (DI LEVEL).

        File formats:
        - Single item: customer_name/ID, product_name/ID, quantity, date
        - Multiple items (HD): customer_name/ID, product1, qty1, product2, qty2, ..., date

        Args:
            filename (str): Name of order file

        Raises:
            InvalidFileFormatError: If file has incorrect format or invalid data
        """
        try:
            with open(filename, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    try:
                        parts = [part.strip() for part in line.strip().split(',')]

                        if len(parts) < 4:
                            raise InvalidFileFormatError(f"Line {line_num}: Not enough fields")

                        # Extract customer and date
                        customer_identifier = parts[0]
                        date_str = parts[-1]

                        # Find customer
                        customer = self.find_customer(customer_identifier)
                        if customer is None:
                            raise InvalidFileFormatError(f"Line {line_num}: Customer '{customer_identifier}' not found")

                        # Parse date
                        try:
                            order_date = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
                        except ValueError:
                            raise InvalidFileFormatError(f"Line {line_num}: Invalid date format")

                        # Extract items (product-quantity pairs)
                        item_parts = parts[1:-1]  # Everything between customer and date

                        if len(item_parts) % 2 != 0:
                            raise InvalidFileFormatError(f"Line {line_num}: Odd number of item fields")

                        # Create OrderItem objects
                        order_items = []
                        for i in range(0, len(item_parts), 2):
                            product_identifier = item_parts[i]
                            quantity_str = item_parts[i + 1]

                            # Find product
                            product = self.find_product(product_identifier)
                            if product is None:
                                raise InvalidFileFormatError(f"Line {line_num}: Product '{product_identifier}' not found")

                            # Parse quantity
                            try:
                                quantity = int(quantity_str)
                            except ValueError:
                                raise InvalidFileFormatError(f"Line {line_num}: Invalid quantity format")

                            order_items.append(OrderItem(product, quantity))

                        # Create and add order
                        order = Order(customer, order_items, order_date)
                        self.__orders.append(order)

                    except InvalidFileFormatError:
                        raise
                    except Exception as e:
                        raise InvalidFileFormatError(f"Line {line_num}: {str(e)}")

        except FileNotFoundError:
            # If orders file doesn't exist, that's okay (optional file)
            pass
        except InvalidFileFormatError:
            raise
        except Exception as e:
            raise InvalidFileFormatError(f"Error reading orders file: {str(e)}")

    def find_customer(self, identifier):
        """
        Search for a customer by ID or name.

        Args:
            identifier (str): Customer ID or name

        Returns:
            Customer object if found, None otherwise
        """
        for customer in self.__customers:
            if customer.get_ID() == identifier or customer.get_name() == identifier:
                return customer
        return None

    def find_product(self, identifier):
        """
        Search for a product by ID or name.

        Args:
            identifier (str): Product ID or name

        Returns:
            Product object if found, None otherwise
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

    def list_orders(self):
        """Display all orders (DI LEVEL)"""
        print("\n========== ORDER LIST ==========")
        if not self.__orders:
            print("No orders found.")
        else:
            for order in self.__orders:
                customer = order.get_customer()
                items = order.get_items()
                date = order.get_date()

                # Format: customer_name, product1, qty1, product2, qty2, ..., date
                item_strs = []
                for item in items:
                    item_strs.append(f"{item.get_product().get_name()}, {item.get_quantity()}")

                items_str = ', '.join(item_strs)
                date_str = date.strftime("%d/%m/%Y %H:%M:%S")

                print(f"{customer.get_name()}, {items_str}, {date_str}")
        print("================================\n")

    def list_customer_orders(self, identifier):
        """
        Display all orders for a specific customer (DI LEVEL).

        Args:
            identifier (str): Customer ID or name
        """
        customer = self.find_customer(identifier)
        if customer is None:
            raise InvalidCustomerError("Invalid customer!")

        print(f"\n========== ORDERS FOR {customer.get_name()} ==========")
        customer_orders = [order for order in self.__orders if order.get_customer() == customer]

        if not customer_orders:
            print("No orders found for this customer.")
        else:
            for order in customer_orders:
                items = order.get_items()
                date = order.get_date()

                item_strs = []
                for item in items:
                    item_strs.append(f"{item.get_product().get_name()}, {item.get_quantity()}")

                items_str = ', '.join(item_strs)
                date_str = date.strftime("%d/%m/%Y %H:%M:%S")

                print(f"{customer.get_name()}, {items_str}, {date_str}")
        print("=" * 50 + "\n")

    def summarize_orders(self):
        """
        Display a summary table of all orders (HD LEVEL).

        Format:
        - Rows: Customer names
        - Columns: Product IDs
        - Values: Number of times product was ordered by customer
        - Last rows: Total order count and quantity per product
        """
        print("\n========== ORDER SUMMARY ==========")

        if not self.__orders:
            print("No orders to summarize.")
            print("===================================\n")
            return

        # Create matrix: customer -> product -> order count
        customer_product_orders = {}
        product_order_count = {}
        product_order_qty = {}

        # Initialize counters
        for customer in self.__customers:
            customer_product_orders[customer.get_name()] = {}
            for product in self.__products:
                customer_product_orders[customer.get_name()][product.get_ID()] = 0

        for product in self.__products:
            product_order_count[product.get_ID()] = 0
            product_order_qty[product.get_ID()] = 0

        # Count orders
        for order in self.__orders:
            customer_name = order.get_customer().get_name()
            for item in order.get_items():
                product_id = item.get_product().get_ID()
                quantity = item.get_quantity()

                # Increment order count for this customer-product pair
                customer_product_orders[customer_name][product_id] += 1

                # Increment total order count and quantity
                product_order_count[product_id] += 1
                product_order_qty[product_id] += quantity

        # Print header
        product_ids = [p.get_ID() for p in self.__products]
        header = "\t" + "\t".join(product_ids)
        print(header)

        # Print customer rows
        for customer in self.__customers:
            row = customer.get_name()
            for product_id in product_ids:
                count = customer_product_orders[customer.get_name()][product_id]
                row += f"\t{count}"
            print(row)

        # Print separator
        print("-" * len(header))

        # Print OrderNum row
        order_num_row = "OrderNum"
        for product_id in product_ids:
            order_num_row += f"\t{product_order_count[product_id]}"
        print(order_num_row)

        # Print OrderQty row
        order_qty_row = "OrderQty"
        for product_id in product_ids:
            order_qty_row += f"\t{product_order_qty[product_id]}"
        print(order_qty_row)

        print("===================================\n")

    def get_most_valuable_customer(self):
        """
        Find the customer who has spent the most money (HD LEVEL).

        Returns:
            Customer object with highest total value, or None if no customers
        """
        if not self.__customers:
            return None

        max_customer = self.__customers[0]
        for customer in self.__customers[1:]:
            if customer.get_value() > max_customer.get_value():
                max_customer = customer

        return max_customer

    def get_most_popular_product(self):
        """
        Find the product with the highest number of orders (HD LEVEL).

        Returns:
            Product object with most orders, or None if no orders
        """
        if not self.__orders:
            return None

        # Count orders per product
        product_order_count = {}
        for product in self.__products:
            product_order_count[product.get_ID()] = 0

        for order in self.__orders:
            for item in order.get_items():
                product_id = item.get_product().get_ID()
                product_order_count[product_id] += 1

        # Find product with max count
        max_product_id = max(product_order_count, key=product_order_count.get)
        max_count = product_order_count[max_product_id]

        if max_count == 0:
            return None

        return self.find_product(max_product_id)

    def write_customers(self, filename="customers.txt"):
        """
        Write all customers to file (HD LEVEL).

        Args:
            filename (str): Output file name
        """
        try:
            with open(filename, 'w') as file:
                for customer in self.__customers:
                    if isinstance(customer, VIPMember):
                        rate = customer.get_rate1()
                    elif isinstance(customer, Member):
                        rate = Member.get_discount_rate()
                    else:
                        rate = 0

                    line = f"{customer.get_ID()}, {customer.get_name()}, {rate}, {customer.get_value()}\n"
                    file.write(line)
        except Exception as e:
            print(f"Error writing customers file: {e}")

    def write_products(self, filename="products.txt"):
        """
        Write all products to file (HD LEVEL).

        Args:
            filename (str): Output file name
        """
        try:
            with open(filename, 'w') as file:
                for product in self.__products:
                    if isinstance(product, Bundle):
                        component_ids = ', '.join([comp.get_ID() for comp in product.get_components()])
                        line = f"{product.get_ID()}, {product.get_name()}, {component_ids}, {product.get_stock()}\n"
                    else:
                        price = product.get_price() if product.get_price() is not None else ''
                        line = f"{product.get_ID()}, {product.get_name()}, {price}, {product.get_stock()}\n"
                    file.write(line)
        except Exception as e:
            print(f"Error writing products file: {e}")

    def write_orders(self, filename="orders.txt"):
        """
        Write all orders to file (HD LEVEL).

        Args:
            filename (str): Output file name
        """
        try:
            with open(filename, 'w') as file:
                for order in self.__orders:
                    customer = order.get_customer()
                    items = order.get_items()
                    date = order.get_date()

                    # Format: customer_name, product1, qty1, product2, qty2, ..., date
                    line_parts = [customer.get_name()]

                    for item in items:
                        line_parts.append(item.get_product().get_name())
                        line_parts.append(str(item.get_quantity()))

                    line_parts.append(date.strftime("%d/%m/%Y %H:%M:%S"))

                    line = ', '.join(line_parts) + '\n'
                    file.write(line)
        except Exception as e:
            print(f"Error writing orders file: {e}")


# ==================== OPERATIONS CLASS (PASS, CREDIT, DI, HD LEVELS) ====================

class Operations:
    """
    Main class for the retail management system operations.

    This class provides the menu-driven interface for:
    - Placing orders
    - Displaying customers, products, and orders
    - Adjusting discount rates and thresholds (DI LEVEL)
    - Viewing statistics (HD LEVEL)
    - Managing data files (HD LEVEL)
    """

    def __init__(self, customer_file="customers.txt", product_file="products.txt", order_file="orders.txt"):
        """
        Initialize the Operations system.

        Args:
            customer_file (str): Customer data file
            product_file (str): Product data file
            order_file (str): Order history file (optional)
        """
        self.__records = Records()
        self.__customer_file = customer_file
        self.__product_file = product_file
        self.__order_file = order_file

        # Generate next customer ID
        self.__next_customer_number = 1

    def initialize(self):
        """
        Initialize the system by loading data from files.

        Returns:
            bool: True if initialization successful, False otherwise
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
            try:
                self.__records.read_customers(self.__customer_file)
            except InvalidFileFormatError as e:
                print(f"Error in {self.__customer_file}: {e}")
                return False

            try:
                self.__records.read_products(self.__product_file)
            except InvalidFileFormatError as e:
                print(f"Error in {self.__product_file}: {e}")
                return False

            # Calculate next customer ID number
            customers = self.__records.get_customers()
            if customers:
                max_num = 0
                for customer in customers:
                    customer_id = customer.get_ID()
                    # Extract number from ID (e.g., "C1" -> 1)
                    num_str = customer_id[1:]
                    try:
                        num = int(num_str)
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        pass
                self.__next_customer_number = max_num + 1

            # Read order file (optional) - DI LEVEL
            if os.path.exists(self.__order_file):
                try:
                    self.__records.read_orders(self.__order_file)
                except InvalidFileFormatError as e:
                    print(f"Cannot load the order file. Run as if there is no order previously.")
                    print(f"Reason: {e}")

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
        print("4: Adjust the discount rates of a VIP member")
        print("5: Adjust the threshold limit of all VIP members")
        print("6: Display all orders")
        print("7: Display all orders of a customer")
        print("8: Summarize all orders")
        print("9: Reveal the most valuable customer")
        print("10: Reveal the most popular product")
        print("0: Exit the program")
        print("=" * 60)

    def place_order(self):
        """
        Handle the place order operation (PASS, CREDIT, HD LEVELS).

        Process:
        1. Get customer name
        2. Check if customer exists or create new customer
        3. Get products and quantities (supports multiple items - HD LEVEL)
        4. Validate products and quantities (CREDIT LEVEL exceptions)
        5. Process order and display receipt
        """
        try:
            # Get customer name
            customer_name = input("\nEnter the name of the customer [e.g. Huong]: ").strip()

            # Find or create customer
            customer = self.__records.find_customer(customer_name)
            is_new_customer = (customer is None)

            # Get order items (HD LEVEL - multiple items support)
            order_items = []

            while True:
                # Get product
                while True:
                    try:
                        product_input = input("\nEnter the product [enter a valid product only, e.g. shirt, towel, oven, kettle]: ").strip()

                        product = self.__records.find_product(product_input)
                        if product is None:
                            raise InvalidProductError("Product is invalid. Please enter a valid product!")

                        # Check if product price is set (CREDIT LEVEL)
                        if product.get_price() is None or product.get_price() <= 0:
                            raise InvalidPriceError(f"Product '{product.get_name()}' does not have a valid price set.")

                        break  # Valid product

                    except InvalidProductError as e:
                        print(str(e))
                    except InvalidPriceError as e:
                        print(str(e))
                        return  # Go back to main menu

                # Get quantity
                while True:
                    try:
                        quantity_input = input("\nEnter the product quantity [enter a positive integer only, e.g. 1, 2, 3]: ").strip()

                        # Validate quantity
                        try:
                            quantity = int(quantity_input)
                        except ValueError:
                            raise InvalidQuantityError("Product quantity is not a number, negative or larger than the stock quantity!")

                        if quantity <= 0:
                            raise InvalidQuantityError("Product quantity is not a number, negative or larger than the stock quantity!")

                        if quantity > product.get_stock():
                            raise InvalidQuantityError("Product quantity is not a number, negative or larger than the stock quantity!")

                        break  # Valid quantity

                    except InvalidQuantityError as e:
                        print(str(e))

                # Add item to order
                order_items.append(OrderItem(product, quantity))

                # Ask if customer wants to order more products (HD LEVEL)
                while True:
                    more_input = input("\nDoes the customer want to order more products? ").strip().lower()
                    if more_input in ['y', 'n']:
                        break
                    print("Invalid input. Please enter 'y' or 'n'.")

                if more_input == 'n':
                    break

            # Handle new customer
            if is_new_customer:
                # Ask about membership
                while True:
                    try:
                        membership_input = input("\nThis is a new customer. Does the customer want to have a membership [enter y or n]? ").strip().lower()

                        if membership_input not in ['y', 'n']:
                            raise InvalidMembershipAnswerError("Invalid input. Please enter 'y' or 'n'.")

                        break
                    except InvalidMembershipAnswerError as e:
                        print(str(e))

                # Create customer based on membership choice
                if membership_input == 'n':
                    # Normal customer
                    customer_id = f"C{self.__next_customer_number}"
                    customer = Customer(customer_id, customer_name, 0)
                    self.__records.add_customer(customer)
                    self.__next_customer_number += 1
                    membership_fee = 0
                else:
                    # Ask membership type
                    while True:
                        try:
                            membership_type = input("\nWhat kind of membership the customer wants? ").strip().upper()

                            if membership_type not in ['M', 'V']:
                                raise InvalidMembershipTypeError("Invalid membership type. Please enter 'M' or 'V'.")

                            break
                        except InvalidMembershipTypeError as e:
                            print(str(e))

                    if membership_type == 'M':
                        # Normal member
                        customer_id = f"M{self.__next_customer_number}"
                        customer = Member(customer_id, customer_name, 0)
                        self.__records.add_customer(customer)
                        self.__next_customer_number += 1
                        membership_fee = 0
                    else:
                        # VIP member
                        customer_id = f"V{self.__next_customer_number}"
                        customer = VIPMember(customer_id, customer_name, 0)
                        self.__records.add_customer(customer)
                        self.__next_customer_number += 1
                        membership_fee = 200.0
            else:
                membership_fee = 0

            # Create and process order
            order = Order(customer, order_items)
            discount_rate, total_after_discount = order.process_order()

            # Add membership fee if applicable
            if membership_fee > 0:
                customer.set_value(customer.get_value() + membership_fee)

            # Add order to records (DI LEVEL)
            self.__records.add_order(order)

            # Display receipt
            print("\n" + "-" * 50)

            # Display each item
            for item in order_items:
                product = item.get_product()
                quantity = item.get_quantity()
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

        except Exception as e:
            print(f"Unexpected error: {e}")

    def display_customers(self):
        """Display all customers (PASS LEVEL)"""
        self.__records.list_customers()

    def display_products(self):
        """Display all products (PASS LEVEL)"""
        self.__records.list_products()

    def adjust_vip_discount(self):
        """
        Adjust discount rates for a specific VIP member (DI LEVEL).

        Process:
        1. Get VIP member identifier (ID or name)
        2. Validate that customer is a VIP member
        3. Get new first discount rate
        4. Update rates (second rate = first rate + 5%)
        """
        try:
            identifier = input("\nEnter the name or ID of the VIP member: ").strip()

            # Find customer
            customer = self.__records.find_customer(identifier)

            if customer is None or not isinstance(customer, VIPMember):
                raise InvalidCustomerError("Invalid customer!")

            # Get new discount rate
            while True:
                try:
                    rate_input = input("Enter the new first discount rate (e.g., 0.10 for 10%): ").strip()

                    try:
                        new_rate = float(rate_input)
                    except ValueError:
                        raise InvalidDiscountRateError("Invalid discount rate. Please enter a valid number.")

                    if new_rate < 0:
                        raise InvalidDiscountRateError("Invalid discount rate. Please enter a non-negative number.")

                    break
                except InvalidDiscountRateError as e:
                    print(str(e))

            # Update rate
            customer.set_rate(new_rate)
            print(f"\nDiscount rates updated for {customer.get_name()}:")
            print(f"First rate: {customer.get_rate1() * 100}%")
            print(f"Second rate: {customer.get_rate2() * 100}%")

        except InvalidCustomerError as e:
            print(str(e))
        except Exception as e:
            print(f"Unexpected error: {e}")

    def adjust_vip_threshold(self):
        """
        Adjust threshold for all VIP members (DI LEVEL).

        Process:
        1. Get new threshold value
        2. Validate threshold (must be positive number)
        3. Update threshold for all VIP members
        """
        try:
            while True:
                try:
                    threshold_input = input("\nEnter the new threshold limit for all VIP members: ").strip()

                    try:
                        new_threshold = float(threshold_input)
                    except ValueError:
                        raise InvalidThresholdError("Invalid threshold. Please enter a valid number.")

                    if new_threshold <= 0:
                        raise InvalidThresholdError("Invalid threshold. Please enter a positive number.")

                    break
                except InvalidThresholdError as e:
                    print(str(e))

            # Update threshold
            VIPMember.set_threshold(new_threshold)
            print(f"\nThreshold updated to {new_threshold} for all VIP members.")

        except Exception as e:
            print(f"Unexpected error: {e}")

    def display_all_orders(self):
        """Display all orders (DI LEVEL)"""
        self.__records.list_orders()

    def display_customer_orders(self):
        """Display orders for a specific customer (DI LEVEL)"""
        try:
            identifier = input("\nEnter the name or ID of the customer: ").strip()
            self.__records.list_customer_orders(identifier)
        except InvalidCustomerError as e:
            print(str(e))
        except Exception as e:
            print(f"Unexpected error: {e}")

    def summarize_orders(self):
        """Display order summary table (HD LEVEL)"""
        self.__records.summarize_orders()

    def reveal_most_valuable_customer(self):
        """Display the customer with highest total spending (HD LEVEL)"""
        customer = self.__records.get_most_valuable_customer()

        if customer is None:
            print("\nNo customers found.")
        else:
            print(f"\nMost valuable customer: {customer.get_name()}")
            print(f"Total spent: {customer.get_value()} (AUD)")

    def reveal_most_popular_product(self):
        """Display the product with most orders (HD LEVEL)"""
        product = self.__records.get_most_popular_product()

        if product is None:
            print("\nNo orders found.")
        else:
            print(f"\nMost popular product: {product.get_name()} (ID: {product.get_ID()})")

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
            elif choice == '4':
                self.adjust_vip_discount()
            elif choice == '5':
                self.adjust_vip_threshold()
            elif choice == '6':
                self.display_all_orders()
            elif choice == '7':
                self.display_customer_orders()
            elif choice == '8':
                self.summarize_orders()
            elif choice == '9':
                self.reveal_most_valuable_customer()
            elif choice == '10':
                self.reveal_most_popular_product()
            elif choice == '0':
                print("\nThank you for using the RMIT retail management system. Goodbye!")
                # Write data back to files (HD LEVEL)
                self.__records.write_customers(self.__customer_file)
                self.__records.write_products(self.__product_file)
                self.__records.write_orders(self.__order_file)
                break
            else:
                print("\nInvalid option. Please try again.")


# ==================== MAIN PROGRAM (HD LEVEL - Command-line Arguments) ====================

def main():
    """
    Main entry point for the program.

    Supports command-line arguments (HD LEVEL):
    - No arguments: Use default file names (customers.txt, products.txt, orders.txt)
    - 2 arguments: python program.py <customer_file> <product_file>
    - 3 arguments: python program.py <customer_file> <product_file> <order_file>

    Any other number of arguments will display usage message and exit.
    """

    # Default file names
    customer_file = "customers.txt"
    product_file = "products.txt"
    order_file = "orders.txt"

    # Parse command-line arguments (HD LEVEL)
    if len(sys.argv) == 1:
        # No arguments - use defaults
        pass
    elif len(sys.argv) == 3:
        # Two arguments: customer and product files (order file optional)
        customer_file = sys.argv[1]
        product_file = sys.argv[2]
    elif len(sys.argv) == 4:
        # Three arguments: customer, product, and order files
        customer_file = sys.argv[1]
        product_file = sys.argv[2]
        order_file = sys.argv[3]
    else:
        # Wrong number of arguments
        print("Usage:")
        print(f"  {sys.argv[0]}                                    # Use default files")
        print(f"  {sys.argv[0]} <customer_file> <product_file>     # Specify customer and product files")
        print(f"  {sys.argv[0]} <customer_file> <product_file> <order_file>  # Specify all files")
        sys.exit(1)

    # Create and initialize operations
    operations = Operations(customer_file, product_file, order_file)

    if operations.initialize():
        operations.run()
    else:
        print("Failed to initialize the system. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
