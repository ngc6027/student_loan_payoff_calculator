from venv import create

import pandas as pd
import tkinter as tk
import datetime

debugFlag = False

class studentLoanPayment:
    def __init__(self, amount, startMonth, startYear, endMonth, endYear):
        self.amount = amount

        self.startDate = datetime.datetime(startYear, startMonth, 1)
        self.endDate = datetime.datetime(endYear, endMonth, 22)


    def setAmount(self, amount):
        self.amount = amount


class studentLoan:
    def __init__(self, startingBalance, interestRate, stepPayments, loanPriority, aidvantageLoanNum, enrolledInAutoPay=False):
        import copy

        self.startingBalance = startingBalance
        self.currentBalance = startingBalance

        self.enrolledInAutoPay = enrolledInAutoPay

        if self.enrolledInAutoPay:
            self.interestRate = (interestRate - 0.25) / 100
        else:
            self.interestRate = interestRate / 100

        self.dailyInterestRate = self.interestRate / 365.25

        self.stepPayments = copy.deepcopy(stepPayments)

        self.loanPriority = loanPriority
        self.aidvantageLoanNum = aidvantageLoanNum

        self.accruedInterest = 0

        self.payoffDate = None


    def resestLoan(self):
        self.currentBalance = self.startingBalance
        self.accruedInterest = 0


    def payOffLoan(self, date):
        self.currentBalance = 0
        self.payoffDate = date


    def setStepPayments(self, stepPayments):
        self.stepPayments = stepPayments


    def calculateMonthlyInterest(self, date):
        import calendar
        return self.currentBalance * self.dailyInterestRate * calendar.monthrange(date.year, date.month)[1]


    def applyMonthlyInterest(self, date):
        monthlyInterest = self.calculateMonthlyInterest(date)

        self.currentBalance += monthlyInterest
        self.accruedInterest += monthlyInterest


    def calculateMonthlyPayment(self, date):
        monthlyPayment = 0
        stepMonthlyPayment = 0

        for stepPayment in self.stepPayments:
            if  stepPayment.startDate <= date <= stepPayment.endDate:
                stepMonthlyPayment = stepPayment.amount
                break

        if (self.currentBalance > 0):
            if self.currentBalance > stepPayment.amount:
                monthlyPayment = stepMonthlyPayment
            else:
                monthlyPayment = self.currentBalance

        return monthlyPayment, stepMonthlyPayment


    def applyMonthlyPayment(self, date):
        paymentAmount, stepPaymentAmount = self.calculateMonthlyPayment(date)
        paymentOverage = stepPaymentAmount - paymentAmount

        if self.currentBalance != 0:
            if paymentAmount >= stepPaymentAmount:
                self.currentBalance -= paymentAmount
            else:
                self.payOffLoan(date)

        return paymentOverage


    def applyExtraPayment(self, extraPayment, date):
        paymentApplied = 0

        if self.currentBalance != 0:
            if extraPayment <= self.currentBalance:
                paymentApplied = extraPayment
                self.currentBalance -= extraPayment
            else:
                paymentApplied = extraPayment - self.currentBalance
                self.payOffLoan(date)

        return paymentApplied

    def __str__(self):
        printStr = f'Loan Priority: {self.loanPriority}; Aidvantage Loan Number: {self.aidvantageLoanNum}'
        printStr += f'\n\tLoan Starting Balance: ${self.startingBalance:,.2f}'
        printStr += f'\n\tLoan Current Balance: ${round(self.startingBalance, 2):,.2f}'
        printStr += f'\n\tInterest Rate: {round(self.interestRate * 100, 2)}%'
        printStr += f'\n\tDaily Interest Rate: {round(self.dailyInterestRate * 100, 5)}%'
        printStr += f'\n\tEnrolled in AutoPay? {self.enrolledInAutoPay}'
        printStr += f'\n\t\tStep 1 Payment: ${self.stepPayments[0].amount:,.2f}'
        printStr += f'\n\t\tStep 2 Payment: ${self.stepPayments[1].amount:,.2f}'
        printStr += f'\n\t\tStep 3 Payment: ${self.stepPayments[2].amount:,.2f}'
        printStr += f'\n\t\tStep 4 Payment: ${self.stepPayments[3].amount:,.2f}'
        printStr += f'\n\t\tStep 5 Payment: ${self.stepPayments[4].amount:,.2f}'

        return printStr


class SLPGui():
    def __init__(self):
        pass


    def createStudentLoan(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "Add Loan Button has been pressed.")
        print("Add Loan Button has been pressed.")


    def removeStudentLoan(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "Remove Loan Button has been pressed.")
        print("Remove Loan Button has been pressed.")


    def createGui(self):
        self.window = tk.Tk()
        self.window.title("Graduated Student Loan Payoff Calculator")

        self.window.rowconfigure(0, minsize=50, weight=1)
        self.window.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], minsize=50, weight=1)

        self.lbl_amount = tk.Label(self.window, text="Amount")
        self.lbl_amount.grid(row=0, column=1)

        self.lbl_interest_rate = tk.Label(self.window, text="Interest Rate")
        self.lbl_interest_rate.grid(row=0, column=2)

        self.lbl_autopay = tk.Label(self.window, text="Enrolled in AutoPay")
        self.lbl_autopay.grid(row=0, column=3)

        self.lbl_loan_provider_number = tk.Label(self.window, text="Loan Provider Number")
        self.lbl_loan_provider_number.grid(row=0, column=1)

        self.lbl_step1_payment = tk.Label(self.window, text="Step 1 Payment")
        self.lbl_step1_payment.grid(row=0, column=4)

        self.lbl_step2_payment = tk.Label(self.window, text="Step 2 Payment")
        self.lbl_step2_payment.grid(row=0, column=5)

        self.lbl_step3_payment = tk.Label(self.window, text="Step 3 Payment")
        self.lbl_step3_payment.grid(row=0, column=6)

        self.lbl_step4_payment = tk.Label(self.window, text="Step 4 Payment")
        self.lbl_step4_payment.grid(row=0, column=7)

        self.lbl_step5_payment = tk.Label(self.window, text="Step 5 Payment")
        self.lbl_step5_payment.grid(row=0, column=8)

        self.lbl_priority = tk.Label(self.window, text="Priority")
        self.lbl_priority.grid(row=0, column=9)

        self.window.rowconfigure(1, minsize=50, weight=1)
        self.window.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], minsize=50, weight=1)

        self.label = tk.Label(self.window, text="Loan 1:")
        self.label.grid(row=1, column=0)

        self.ent_amount = tk.Entry(self.window, width=5)
        self.ent_amount.grid(row=1, column=1)

        self.ent_interest_rate = tk.Entry(self.window, width=5)
        self.ent_interest_rate.grid(row=1, column=2)

        self.ent_autopay = tk.Entry(self.window, width=5)
        self.ent_autopay.grid(row=1, column=3)

        self.ent_loan_provider_number = tk.Entry(self.window, width=5)
        self.ent_loan_provider_number.grid(row=1, column=4)

        self.ent_step1payment = tk.Entry(self.window, width=5)
        self.ent_step1payment.grid(row=1, column=5)

        self.ent_step2payment = tk.Entry(self.window, width=5)
        self.ent_step2payment.grid(row=1, column=6)

        self.ent_step3payment = tk.Entry(self.window, width=5)
        self.ent_step3payment.grid(row=1, column=7)

        self.ent_step4payment = tk.Entry(self.window, width=5)
        self.ent_step4payment.grid(row=1, column=8)

        self.ent_step5payment = tk.Entry(self.window, width=5)
        self.ent_step5payment.grid(row=1, column=9)
        
        self.ent_priority = tk.Entry(self.window, width=5)
        self.ent_priority.grid(row=1, column=1)

        self.btn_add_loan = tk.Button(
            text = "Add Loan",
            width=8,
            height=1,
            bg="blue",
            fg="yellow",
            command=lambda:self.createStudentLoan(),
        )

        self.btn_add_loan.grid(row=1, column=10)

        self.btn_remove_loan = tk.Button(
            text = "Remove Loan",
            width=10,
            height=1,
            bg="blue",
            fg="yellow",
            command=lambda:self.removeStudentLoan(),
        )

        self.window.rowconfigure(2, minsize=50, weight=1)
        self.window.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], minsize=50, weight=1)

        self.btn_remove_loan.grid(row=2, column=10)

    def runGui(self):
        self.window.mainloop()


def createStudentLoansList ():
    studentLoans = list()

    payment1 = studentLoanPayment(109.63, 10, 2023, 9, 2025)
    payment2 = studentLoanPayment(144.28, 10, 2025, 9, 2027)
    payment3 = studentLoanPayment(189.88, 10, 2027, 9, 2029)
    payment4 = studentLoanPayment(249.89, 10, 2029, 9, 2031)
    payment5 = studentLoanPayment(328.87, 10, 2031, 6, 2033)
    # studentLoans.append(studentLoan(16222.15, 6.6, [payment1, payment2, payment3, payment4, payment5], 1, 9, False))
    studentLoans.append(studentLoan(16222.15, 6.6, [payment1, payment2, payment3, payment4, payment5], 1, 9, True))

    payment1.setAmount(14.81)
    payment2.setAmount(19.49)
    payment3.setAmount(25.65)
    payment4.setAmount(33.76)
    payment5.setAmount(44.43)
    # studentLoans.append(studentLoan(2436.58, 4.66, [payment1, payment2, payment3, payment4, payment5], 2, 2, False))
    studentLoans.append(studentLoan(2436.58, 4.66, [payment1, payment2, payment3, payment4, payment5], 2, 2, True))

    payment1.setAmount(27.00)
    payment2.setAmount(35.53)
    payment3.setAmount(46.76)
    payment4.setAmount(61.53)
    payment5.setAmount(80.97)
    # studentLoans.append(studentLoan(4441.30, 4.66, [payment1, payment2, payment3, payment4, payment5], 3, 1, False))
    studentLoans.append(studentLoan(4441.30, 4.66, [payment1, payment2, payment3, payment4, payment5], 3, 1, True))

    payment1.setAmount(32.60)
    payment2.setAmount(42.90)
    payment3.setAmount(56.46)
    payment4.setAmount(74.31)
    payment5.setAmount(97.80)
    # studentLoans.append(studentLoan(5426.37, 4.45, [payment1, payment2, payment3, payment4, payment5], 4, 7, False))
    studentLoans.append(studentLoan(5426.37, 4.45, [payment1, payment2, payment3, payment4, payment5], 4, 7, True))

    payment1.setAmount(45.20)
    payment2.setAmount(59.49)
    payment3.setAmount(78.29)
    payment4.setAmount(103.03)
    payment5.setAmount(135.60)
    # studentLoans.append(studentLoan(7523.55, 4.45, [payment1, payment2, payment3, payment4, payment5], 5, 8, False))
    studentLoans.append(studentLoan(7523.55, 4.45, [payment1, payment2, payment3, payment4, payment5], 5, 8, True))

    payment1.setAmount(32.31)
    payment2.setAmount(42.52)
    payment3.setAmount(55.95)
    payment4.setAmount(73.63)
    payment5.setAmount(96.89)
    # studentLoans.append(studentLoan(5425.03, 4.29, [payment1, payment2, payment3, payment4, payment5], 6, 3, False))
    studentLoans.append(studentLoan(5425.03, 4.29, [payment1, payment2, payment3, payment4, payment5], 6, 3, True))

    payment1.setAmount(48.22)
    payment2.setAmount(63.46)
    payment3.setAmount(83.51)
    payment4.setAmount(109.90)
    payment5.setAmount(144.63)
    # studentLoans.append(studentLoan(8097.05, 4.29, [payment1, payment2, payment3, payment4, payment5], 7, 4, False))
    studentLoans.append(studentLoan(8097.05, 4.29, [payment1, payment2, payment3, payment4, payment5], 7, 4, True))

    payment1.setAmount(31.33)
    payment2.setAmount(41.23)
    payment3.setAmount(54.26)
    payment4.setAmount(71.41)
    payment5.setAmount(93.97)
    # studentLoans.append(studentLoan(5419.29, 3.76, [payment1, payment2, payment3, payment4, payment5], 8, 5, False))
    studentLoans.append(studentLoan(5419.29, 3.76, [payment1, payment2, payment3, payment4, payment5], 8, 5, True))

    payment1.setAmount(44.39)
    payment2.setAmount(58.42)
    payment3.setAmount(76.87)
    payment4.setAmount(101.16)
    payment5.setAmount(133.12)
    # studentLoans.append(studentLoan(7677.75, 3.76, [payment1, payment2, payment3, payment4, payment5], 9, 6, False))
    studentLoans.append(studentLoan(7677.75, 3.76, [payment1, payment2, payment3, payment4, payment5], 9, 6, True))

    return studentLoans


def main():
    studentLoans = createStudentLoansList()
    studentLoans.sort(key=lambda x: x.loanPriority)

    if debugFlag:
        for loan in studentLoans:
            print(loan)

        print('\n')

        for loan in studentLoans:
            print(f'Starting Balance: ${round(loan.currentBalance, 2):,.2f}; Starting September Interest: ${round(loan.calculateMonthlyInterest(9, 2023), 2):,.2f}')

        print('\n')

        for loan in studentLoans:
            for payment in loan.stepPayments:
                print(f'${payment.amount:,.2f}')
            print()

        print('\n')

    # Apply interest for the month of September 2023, before payments are due
    for loan in studentLoans:
        loan.applyMonthlyInterest(datetime.datetime(2023, 9, 1))

    desiredPayment = 674

    # Create range of payment due dates
    paymentDates = pd.date_range(start = datetime.datetime(2023, 10, 1), end = datetime.datetime(2033, 6, 30), freq = "MS").to_pydatetime().tolist()
    paymentDates = [paymentDate.replace(day=22) for paymentDate in paymentDates]

    # TODO: Convert the old way below (iterating over each loan) into the new way using paymentDates (iterating over each month)
    for paymentDate in paymentDates:
        paymentObligation = sum((loan.calculateMonthlyPayment(paymentDate)[0] for loan in studentLoans))
        actualPayment = paymentObligation

        if paymentObligation > desiredPayment:
            print(f'NOTE: payment for {paymentDate.month}/{paymentDate.year} will be higher than the desired payment amount.')
            extraPayment = 0
        else:
            actualPayment = desiredPayment
            extraPayment = desiredPayment - paymentObligation

        # print(f'Actual Payment in {paymentDate.month}/{paymentDate.year}: ${actualPayment:,.2f}')
        # print(f'Total Extra Payment in {paymentDate.month}/{paymentDate.year}: ${extraPayment:,.2f}\n')

        # Apply normal monthly payment to each loan
        for loan in studentLoans:
            loan.applyMonthlyPayment(paymentDate)

        # Apply extra payment to highest priority loan with remaining balance. Note that the loans are already organized in order of priority
        if extraPayment > 0:
            for loan in studentLoans:
                paymentApplied = loan.applyExtraPayment(extraPayment, paymentDate)
                extraPayment -= paymentApplied
                if paymentApplied == extraPayment:
                    break

        # Apply monthly interest for each loan
        for loan in studentLoans:
            loan.applyMonthlyInterest(paymentDate)

    print()

    totalInterest = 0

    for loan in studentLoans:
        if loan.payoffDate is not None:
            print(f'Loan {loan.loanPriority} payoff date: {loan.payoffDate}')
        else:
            print(f'Payoff date not set for Loan {loan.loanPriority}')

    print()

    for loan in studentLoans:
        totalInterest += loan.accruedInterest
        print(f'Loan {loan.loanPriority}: Total interest: ${round(loan.accruedInterest, 2):,.2f}')

    print(f'\nTotal Interest: ${round(totalInterest, 2):,.2f}')

    gui = SLPGui()
    gui.createGui()
    gui.runGui()


if __name__ == "__main__":
    main()
