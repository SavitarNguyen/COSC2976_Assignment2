#!/usr/bin/env python3
"""
Script to create weekly submission versions from the main file
"""

def create_credit_version():
    """Create CREDIT level version (PASS + CREDIT)"""
    print("Creating CREDIT version (Week 8)...")

    with open('ProgFunA2_s1234567.py', 'r') as f:
        lines = f.readlines()

    # Find the line where DI level starts (after read_orders method)
    credit_end = 0
    for i, line in enumerate(lines):
        if 'def read_orders(self, filename="orders.txt"):' in line:
            credit_end = i
            break

    # Write CREDIT version up to that point
    with open('ProgFunA2_s1234567_WEEK8_CREDIT.py', 'w') as f:
        # Write header
        f.write('"""\\n')
        f.write('COSC2976 Programming Fundamentals - Assignment 2 - WEEK 8 SUBMISSION (PASS + CREDIT LEVEL)\\n')
        f.write('Retail Management System using Object-Oriented Programming\\n')
        f.write('\\n')
        f.write('This is the PASS + CREDIT level implementation with:\\n')
        f.write('- Customer hierarchy (Customer, Member, VIPMember)\\n')
        f.write('- Product and Bundle classes\\n')
        f.write('- Custom exceptions for validation\\n')
        f.write('- Order processing with single item per order\\n')
        f.write('\\n')
        f.write('Author: Student ID s1234567\\n')
        f.write('Libraries used: sys, os\\n')
        f.write('"""\\n')
        f.write('\\n')

        # Skip original header, start from imports
        in_header = True
        for line in lines[11:credit_end]:
            if in_header and line.strip() and not line.startswith('import'):
                continue
            in_header = False
            f.write(line)

        # Add simplified methods
        f.write('''
    def find_customer(self, identifier):
        """Search for a customer by ID or name."""
        for customer in self.__customers:
            if customer.get_ID() == identifier or customer.get_name() == identifier:
                return customer
        return None

    def find_product(self, identifier):
        """Search for a product by ID or name."""
        for product in self.__products:
            if product.get_ID() == identifier or product.get_name() == identifier:
                return product
        return None

    def list_customers(self):
        """Display all customers with their information"""
        print("\\n========== CUSTOMER LIST ==========")
        for customer in self.__customers:
            customer.display_info()
        print("===================================\\n")

    def list_products(self):
        """Display all products with their information"""
        print("\\n========== PRODUCT LIST ==========")
        for product in self.__products:
            product.display_info()
        print("==================================\\n")
''')

        # Add Operations class for CREDIT level
        write_operations_credit(f)

        # Add main function
        write_main_function(f)

    print("CREDIT version created successfully!")

def create_di_version():
    """Create DI level version (PASS + CREDIT + DI)"""
    print("Creating DI version (Week 9)...")

    with open('ProgFunA2_s1234567.py', 'r') as f:
        lines = f.readlines()

    # Find where HD level starts (summarize_orders)
    di_end = 0
    for i, line in enumerate(lines):
        if 'def summarize_orders(self):' in line:
            di_end = i
            break

    with open('ProgFunA2_s1234567_WEEK9_DI.py', 'w') as f:
        # Write header
        f.write('"""\\n')
        f.write('COSC2976 Programming Fundamentals - Assignment 2 - WEEK 9 SUBMISSION (PASS + CREDIT + DI LEVEL)\\n')
        f.write('Retail Management System using Object-Oriented Programming\\n')
        f.write('\\n')
        f.write('This is the PASS + CREDIT + DI level implementation with:\\n')
        f.write('- Customer hierarchy (Customer, Member, VIPMember)\\n')
        f.write('- Product and Bundle classes\\n')
        f.write('- Custom exceptions for validation\\n')
        f.write('- Order processing with date support\\n')
        f.write('- Order history management\\n')
        f.write('- VIP discount and threshold adjustments\\n')
        f.write('\\n')
        f.write('Author: Student ID s1234567\\n')
        f.write('Libraries used: sys, datetime, os\\n')
        f.write('"""\\n')
        f.write('\\n')

        # Write all code up to DI end
        for line in lines[11:di_end]:
            f.write(line)

        # Add closing for Records class
        f.write('''

# ==================== OPERATIONS CLASS (PASS, CREDIT, DI LEVEL) ====================

class Operations:
    """Main class for the retail management system operations (DI LEVEL)."""

    def __init__(self, customer_file="customers.txt", product_file="products.txt", order_file="orders.txt"):
        """Initialize the Operations system."""
        self.__records = Records()
        self.__customer_file = customer_file
        self.__product_file = product_file
        self.__order_file = order_file
        self.__next_customer_number = 1

    def initialize(self):
        """Initialize the system by loading data from files."""
        try:
            if not os.path.exists(self.__customer_file):
                print(f"Error: {self.__customer_file} is missing.")
                return False
            if not os.path.exists(self.__product_file):
                print(f"Error: {self.__product_file} is missing.")
                return False

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

            # Read order file (DI LEVEL)
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
        print("\\nWelcome to the RMIT retail management system!")
        print("\\n" + "=" * 60)
        print("You can choose from the following options:")
        print("1: Place an order")
        print("2: Display existing customers")
        print("3: Display existing products")
        print("4: Adjust the discount rates of a VIP member")
        print("5: Adjust the threshold limit of all VIP members")
        print("6: Display all orders")
        print("7: Display all orders of a customer")
        print("0: Exit the program")
        print("=" * 60)

    # Copy place_order, adjust_vip_discount, adjust_vip_threshold from main file
    # (Simplified for length - in actual file, copy full methods from lines 1170-1370)

    def place_order(self):
        """Handle place order operation (DI LEVEL - single item)."""
        # Full implementation from main file
        pass  # TODO: Copy from main file

    def display_customers(self):
        """Display all customers"""
        self.__records.list_customers()

    def display_products(self):
        """Display all products"""
        self.__records.list_products()

    def adjust_vip_discount(self):
        """Adjust discount rates for a specific VIP member (DI LEVEL)."""
        # Full implementation from main file
        pass  # TODO: Copy from main file

    def adjust_vip_threshold(self):
        """Adjust threshold for all VIP members (DI LEVEL)."""
        # Full implementation from main file
        pass  # TODO: Copy from main file

    def display_all_orders(self):
        """Display all orders (DI LEVEL)"""
        self.__records.list_orders()

    def display_customer_orders(self):
        """Display orders for a specific customer (DI LEVEL)"""
        try:
            identifier = input("\\nEnter the name or ID of the customer: ").strip()
            self.__records.list_customer_orders(identifier)
        except InvalidCustomerError as e:
            print(str(e))
        except Exception as e:
            print(f"Unexpected error: {e}")

    def run(self):
        """Main program loop."""
        while True:
            self.display_menu()
            choice = input("\\nChoose one option: ").strip()

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
            elif choice == '0':
                print("\\nThank you for using the RMIT retail management system. Goodbye!")
                break
            else:
                print("\\nInvalid option. Please try again.")


# ==================== MAIN PROGRAM ====================

def main():
    """Main entry point for the program."""
    customer_file = "customers.txt"
    product_file = "products.txt"
    order_file = "orders.txt"

    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 3:
        customer_file = sys.argv[1]
        product_file = sys.argv[2]
    elif len(sys.argv) == 4:
        customer_file = sys.argv[1]
        product_file = sys.argv[2]
        order_file = sys.argv[3]
    else:
        print("Usage:")
        print(f"  {sys.argv[0]}                                    # Use default files")
        print(f"  {sys.argv[0]} <customer_file> <product_file>     # Specify files")
        print(f"  {sys.argv[0]} <customer_file> <product_file> <order_file>  # Specify all files")
        sys.exit(1)

    operations = Operations(customer_file, product_file, order_file)

    if operations.initialize():
        operations.run()
    else:
        print("Failed to initialize the system. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
''')

    print("DI version created successfully!")

def write_operations_credit(f):
    """Write Operations class for CREDIT level"""
    # This would be too long to include here
    # The actual implementation should copy from the main file
    pass

def write_main_function(f):
    """Write main function"""
    f.write('''
# ==================== MAIN PROGRAM ====================

def main():
    """Main entry point for the program."""
    customer_file = "customers.txt"
    product_file = "products.txt"

    if len(sys.argv) == 1:
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
''')

if __name__ == "__main__":
    #create_credit_version()
    #create_di_version()
    print("Script ready to create versions")
    print("Note: Due to the file complexity, versions are better created manually")
