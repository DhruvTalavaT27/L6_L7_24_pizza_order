TOPPINGS = {"cheese": 40, "olives": 30, "onion": 20, "paneer": 50}
SIZES = {"S": 8, "M": 10, "L": 12}


def toppings_price(toppings_csv):
    # Bug found by fuzzing: None raised AttributeError and any unknown topping
    # raised KeyError.  Unknown or blank entries are now ignored instead.
    if not isinstance(toppings_csv, str):
        return 0
    total = 0
    for t in toppings_csv.split(','):
        total += TOPPINGS.get(t.strip().lower(), 0)
    return total


def pizza_inches(size):
    # Bug found by fuzzing: None raised AttributeError and an unknown size code
    # raised KeyError.  An unknown size now returns 0 inches.
    if not isinstance(size, str):
        return 0
    return SIZES.get(size.strip().upper(), 0)


def split_bill(text):
    # Bug found by fuzzing: None raised AttributeError, text without a '/' raised
    # ValueError from unpacking, and a zero divisor raised ZeroDivisionError.
    # Unparseable input now returns 0.0 instead of crashing.
    if not isinstance(text, str):
        return 0.0
    parts = text.split('/')
    if len(parts) != 2:
        return 0.0
    try:
        total = int(parts[0].strip())
        people = int(parts[1].strip())
    except ValueError:
        return 0.0
    if total < 0 or people <= 0:
        return 0.0
    return round(total / people, 2)


def main():
    print("==== Running toppings_price ====")
    user_input = input("Enter toppings as CSV (e.g. cheese,olives): ")
    result = toppings_price(user_input)
    print("Toppings Price:", result)

    print("\n==== Running pizza_inches ====")
    user_input = input("Enter pizza size (S/M/L): ")
    result = pizza_inches(user_input)
    print("Size in Inches:", result)

    print("\n==== Running split_bill ====")
    user_input = input("Enter total and people (e.g. 900/3): ")
    result = split_bill(user_input)
    print("Per Person:", result)


if __name__ == "__main__":
    main()
