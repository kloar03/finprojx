""" contains miscellaneous utils """

def float_as_money(float):
    """ prints a float in dollars """
    return f"${float:,.2f}"

if __name__ == '__main__':
    print(float_as_money(0))
    print(float_as_money(1000.0357))