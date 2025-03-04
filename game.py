#game.py
#Ava Heintzelman 
#3/3/25

import gamefunctions

def main():
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)

    print("\nShop Menu:")
    gamefunctions.print_shop_menu("Sword", 10.99, "Shield", 15.49)

    money = float(input("\nEnter your available money: "))
    price = float(input("Enter the price of the item: "))
    quantity = int(input("Enter the quantity to purchase: "))
    purchased, remaining = gamefunctions.purchase_item(price, money, quantity)
    print(f"You purchased {purchased} item(s). Remaining money: {remaining}")

    print("\nA wild monster appears!")
    monster = gamefunctions.new_random_monster()
    print("Monster Details:")
    for key, value in monster.items():
        print(f"{key.capitalize()}: {value}")

    a = int(input("\nEnter first number for sorta_sum: "))
    b = int(input("Enter second number for sorta_sum: "))
    result = gamefunctions.sorta_sum(a, b)
    print(f"The result of sorta_sum is: {result}")

if __name__ == "__main__":
    main()
