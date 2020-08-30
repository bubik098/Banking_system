import random
import sqlite3
conn=sqlite3.connect("card.s3db")
c=conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS card(
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER
);""")
conn.commit()


class Card():

    def Luhn_algorithm(self,card_num):
        suma = 0
        for i in range(1, 16):
            if i % 2 != 0:
                num = int(card_num[i - 1]) * 2
                if num > 9:
                    num = num - 9
                    suma += num
                else:
                    suma += num
            else:
                suma += int(card_num[i - 1])
        cyfra = int((str(suma))[-1])
        if cyfra == 0 and cyfra != int(card_num[-1]):
            return "correct"

        elif 10 - cyfra == int(card_num[-1]):
            return "correct"
        else:
            return None

    def create_card(self):
        suma = 8
        card_num = "400000"
        print("Your card has been created")
        x = 1
        while x < 10:
            # print("x",x)
            num = random.randint(0, 9)
            card_num += str(num)
            # print("random num",num)
            if x % 2 != 0:
                num = num * 2
                if num > 9:
                    num = num - 9
            # print(num,"po")
            suma += num

            x += 1

        cyfra = int((str(suma))[-1])
        if cyfra==0:
            card_num=card_num+"0"
        else:
            checksum = 10 - cyfra
            card_num = card_num + str(checksum)
        print("Your card number:")
        print(card_num)
        return card_num

    def create_pin(self):
        print("Your card PIN:")
        x = 0
        pin_num = ""
        while x < 4:
            num = random.randint(0, 9)
            pin_num += str(num)
            x += 1
        print(pin_num)
        return pin_num

    def check_balance(self,card_num):
        c.execute("select  balance from card where number=?",(card_num,))
        balance=c.fetchall()[0][0]
        print("Balance: ", balance)

    def add_money(self,card_num):
        print("Enter income:")
        kwota=input()
        c.execute("UPDATE card set balance=balance+? where number=?",(int(kwota),card_num))
        conn.commit()
        print("Income was added!")

    def close_account(self,card_num):
        c.execute("delete from card where number=?",(card_num,))
        conn.commit()

    def transfer_money(self,card_num):
        print("Enter card number:")
        receiver_num=input()
        receiver=self.Luhn_algorithm(receiver_num)
        if receiver:
            if receiver_num==card_num:
                print("You can't transfer money to the same account!")
            else:
                c.execute("select  number,balance from card")
                baza=c.fetchall()
                x=0
                for row in baza:

                    if receiver_num==row[0]:
                        x=1
                        print("Enter how much money you want to transfer:")
                        money=int(input())
                        c.execute("select  balance from card where number=?",(card_num,))
                        if money>c.fetchall()[0][0]:
                            print("Not enough money!")
                        else:
                            c.execute("UPDATE card set balance=balance+? where number=?", (money, receiver_num))
                            c.execute("UPDATE card set balance=balance-? where number=?", (money, card_num))
                            conn.commit()
                            print("Success!")
                if x==0:
                    print("Such a card does not exist.")
        else:
            print("Probably you made mistake in the card number. Please try again!")
        # c.execute("select")


class Bank():

    def __init__(self):
        self.id=1
        self.card = Card()

    def menu(self):
        while True:
            print("1. Create an account\n2. Log into account\n0. Exit")
            user = input()
            print()
            if user == "1":
                card_num = self.card.create_card()
                pin_num = self.card.create_pin()
                dane=(self.id,card_num,pin_num,0)
                c.execute("INSERT INTO card(id, number,pin,balance) VALUES(?,?,?,?)", dane)
                conn.commit()
                # print(dane)
                # self.baza_danych.setdefault(card_num, str(pin_num))
                self.id+=1
                # print(self.baza_danych)

            elif user == "2":
                c.execute("select * from card")

                baza_danych=c.fetchall()
                # print(baza_danych)

                print("Enter your card number:")
                card_num = input()

                print("Enter your PIN:")
                pin = input()
                x=0
                for row in baza_danych:
                    if card_num==row[1] and pin==row[2]:
                        x=1
                        print()
                        print("You have successfully logged in!")
                        while True:
                            print()
                            print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                            user1 = input()

                            if user1 == "1":
                                self.card.check_balance(card_num)
                                # print("Balance: ",row[3])

                            elif user1=="2":
                                self.card.add_money(card_num)

                            elif user1=="3":
                                self.card.transfer_money(card_num)


                            elif user1=="4":
                                self.card.close_account(card_num)
                                break

                                # self.card.check_balance()
                            elif user1 == "5":
                                print("You have successfully logged out!")
                                break
                            elif user1 == "0":
                                print()
                                print("Bye!")
                                exit()
                if x==0:
                    print("Wrong card number or PIN!")

            elif user == "0":
                print()
                print("Bye!")
                exit()
            print()


bank_system = Bank()
bank_system.menu()