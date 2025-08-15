# Expenses Tracker Program

# This program allows you to(Add, update, delete, and view expenses)
# Automatically save expenses to a file
# Load saved expenses from a file
# Calculate total expenses and totals by category

expenses = []  # a global empty list to save the expenses to

# Function: add_expense
# Adds a new expense to the expenses list, auto-saves it to a file
# price: float - the cost of the expense
# category: str - the category (food, drinks, ...)
def add_expense(price, category):
    try:
        expenses.append({"Price:": float(price), "Category": category.lower()}) # add a new expense as a dictionary (price converted to float, category in lowercase)
        print(f"Added: ${price} for {category}")#prints that you added (x) to price and (y) for category
        write_expenses_to_file()  # auto-save after adding the expense
    except ValueError:
        print("Invalid input. Please enter a valid number for price")#prints this if you entered str for example instead of (int,float)
    except Exception as e:
        print("Failed to add expense:", e)

# Function: write_expenses_to_file
# Saves the current expenses list to a text file
# filename: str - default file name "expenses.txt"
def write_expenses_to_file(filename="expenses.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as f: #opens the file with the "utf-8" to accept multiple languages
            for exp in expenses: # loop to Save each expense in csv format: (price,category)
                f.write(f"{exp['Price:']},{exp['Category']}\n")
    except Exception as e: #if theres an exception
        print("Saving failed:", e)#prints this

# Function: load_expenses_from_file
# Loads expenses from a file into the expenses list
# filename: str - default file name "expenses.txt"
def load_expenses_from_file(filename="expenses.txt"):
    global expenses
    try:
        with open(filename, "r", encoding="utf-8") as f:
            expenses = [] # Clear current list before loading
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2 and parts[0] != "": # makes sure line is valid before adding it to the list
                    expenses.append({"Price:": float(parts[0]), "Category": parts[1]})
        print("Saved expenses loaded:")
        for exp in expenses:
            print(f"${exp['Price:']} - {exp['Category']}")#prints the saved expenses (price: ... , category: ...)
        return expenses
    except FileNotFoundError:
        print("No saved expenses found")#if theres no saved expenses or empty expenses file
        return []
    except ValueError:
        print("Error reading file: corrupted data detected")
        return []
    except Exception as e:
        print("Loading failed:", e)
        return []

# Function: update_expenses
# Updates an existing expense's amount and/or category
# index, amount, category are optional so it can be interactive or direct
def update_expenses(index=None, amount=None, category=None):
    if not expenses:
        print("No expenses to update")#if theres no expenses in the file it will print this
        return False
    try:
        if index is None:  # If index is not provided, display expenses and let user pick the expense he wants to update
            for i, exp in enumerate(expenses):#enumerate loops and provides both the index and the value
                print(f"{i + 1}. ${exp['Price:']} - {exp['Category']}") #asks the user which index he wants to update for both price and category
            index = int(input("Select expense to update: ")) - 1 #the user input

        if not (0 <= index < len(expenses)): # Check if index is valid
            print("Invalid index")#if its not valid prints this
            return False

        if amount is None and category is None: # If no update values provided, ask user
            new_amount = input("New amount (leave blank to keep): ").strip()#asks for the new value for the updated expense price, presses enter(blank) to skip changing the value
            new_category = input("New category (leave blank to keep): ").strip()#asks for the new value for the updated expense category, presses enter(blank) to skip changing the value

            if new_amount != "":#if the user does not leave it blank,asiigns the new value for price
                expenses[index]["Price:"] = float(new_amount)
            if new_category != "":#if the user does not leave it blank,asiigns the new value for category, in lower so it does not seperate for ex:-(food from FOOD), its the same category
                expenses[index]["Category"] = new_category.lower()
        else:
            if amount is not None:
                expenses[index]["Price:"] = float(amount) #if the user leaves it blank, keeps the old value of price
            if category is not None:
                expenses[index]["Category"] = category.lower() #if the user leaves it blank, keeps the old value of category

        print("Expenses Updated")#exiting the loop and prints this
        write_expenses_to_file()  # auto-save after update
        return True
    except ValueError:
        print("Update Failed: please enter a valid number for amount")
        return False
    except Exception as e:
        print("Update failed:", e)
        return False

# Function: delete_expense
# Deletes an expense by index
def delete_expense():
    if not expenses:
        print("No Expenses to Delete")#if theres no expenses saved in the file
        return
    try:
        for i, exp in enumerate(expenses): #shows all expenses in the list for selection
            print(f"{i + 1}. ${exp['Price:']} - {exp['Category']}")
        index = int(input("Select Expense to Delete: ")) - 1

        if not (0 <= index < len(expenses)): #checks if its valid
            print("Invalid Index")
            return

        removed = expenses.pop(index)  # Remove the selected expense
        print(f"Deleted: ${removed['Price:']} - {removed['Category']}")
        write_expenses_to_file()  # auto-save after delete
    except ValueError:
        print("Invalid input! Please enter a number")
    except Exception as e:
        print("Deletion failed:", e)

# Function: calculate_total_expenses
# Returns the total sum of all expenses
def calculate_total_expenses():
    try:
        total = sum(exp["Price:"] for exp in expenses)#for loop to calculate the summation of the price only
        print(f"Total: ${total:.2f}")#prints the answer in a decimal form
        return total
    except Exception as e:
        print("Failed to Calculate Total:", e)
        return 0

# Function: calculate_total_expenses_by_category
# Calculates and prints total expenses per category
def calculate_total_expenses_by_category():
    if not expenses:
        print("No Expenses to Calculate")
        return {}
    try:
        categories = {}
        for exp in expenses:
            cat = exp["Category"] #cat for category
            categories[cat] = categories.get(cat, 0) + exp["Price:"] # Add up totals for each category
        print("Expenses by category:") # Print results
        for category, amt in categories.items(): #amt for amount(price)
            print(f"{category}: ${amt:.2f}")
        return categories
    except Exception as e:
        print("Failed to calculate by category:", e)
        return {}

# Function: menu
# Displays the main menu and processes user choices
def menu():
    while True:
        print("\nSelect an Option:")
        print("1. Add Expense")
        print("2. Load Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Total Expenses")
        print("6. Total Expenses(By Category)")
        print("7. [ Exit ]")
        choice = input("Enter your option: ")

        if choice == "1":
            try:
                price = float(input("Enter price: "))#float to accept decimal numbers
                category = input("Enter category: ")
                add_expense(price, category)
            except ValueError:
                print("Invalid price. Please enter a number")#prints this if you entered a string value instead of a number(int,float)
            except Exception as e:
                print("Failed to add Expense", e)#if thres an exception it will print this message
        elif choice == "2":
            load_expenses_from_file()
        elif choice == "3":
            update_expenses()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            calculate_total_expenses()
        elif choice == "6":
            calculate_total_expenses_by_category()
        elif choice == "7":
            exit()
        else:
            print("Invalid Option, Enter a Number Between 1 and 7")

# This script will run the menu at first
if __name__ == "__main__":
    menu()