#!/usr/bin/python

class Customer():
    """A customer of ABC Bank with a checking account. Customers have the
    following properties:

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.
    """

    def __init__(self, name):
        """Return a Customer object whose name is *name*.""" 
        self.name = name
        self.balance = 0.0

    def withdraw(self, amount):
        """Return the balance remaining after withdrawing *amount*
        dollars."""
        if amount > self.balance:
            print 'Insufficient balance'
        self.balance -= amount
        return self.balance

    def deposit(self, amount):
        """Return the balance remaining after depositing *amount*
        dollars."""
        self.balance += amount
        return self.balance
    def balancecheck(self):
        """Return the balance remaining dollars."""
        return self.balance

def main():

    name = raw_input("Hello! Enter your name: ")
    account = Customer(name)

    action = input("Enter your choice: \n 1. Withdrawal \n 2. deposit \n 3. Balance check \n4. Exit \n" )

    if action == 1:
            amount = input("Enter amount you need to withdraw:")
            result = account.withdraw(amount)
            print "You have %d remaining in your account" % result

    elif action == 2:
            amount = input("Enter amount you need to deposit:")
            result = account.deposit(amount)
            print "Amount %d deposited and your account balance is %d" % (amount, result)
     
    elif action == 3:
            result = account.balancecheck()
            print "You have $ %d in your account!!!" % result
    elif action == 4:
    	    exit(0)
    else:
            print "Invalid option"
	    exit(1)


if __name__ == "__main__":

    main()


