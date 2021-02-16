"""
User interface for module currency

When run as a script, this module prompts the user for two currencies and 
an amount. It prints out the result of converting the first currency to 
the second.

Author: Arthur Wayne asw263
Date:   30 September 2020
"""

import a1
x = input("Enter source currency: ")
y = input("Enter target currency: ")
z = input("Enter original amount: ")
result = str(a1.exchange(x,y,float(z)))
print("You can exchange "+z+" "+x+" for "+result+" "+y)