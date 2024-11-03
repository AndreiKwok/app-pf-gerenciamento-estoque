# Creating an instance of Item
item = Item(name="Laptop", description="A high-performance laptop", price=999.99)

# Accessing attributes
print(item.name)        # Output: Laptop
print(item.description) # Output: A high-performance laptop
print(item.price)       # Output: 999.99

# Validating data
try:
    invalid_item = Item(name="Phone", description="A smartphone", price="free")  # price must be a float
except ValueError as e:
    print(e)  # Will print an error message indicating that the value is not valid
