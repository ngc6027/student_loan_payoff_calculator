import sys

import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import copy

debugFlag = False

class studentLoanPayment:
    def __init__(self, amount, startMonth, startYear, endMonth, endYear):
        self.amount = amount

        self.startDate = datetime(startYear, startMonth, 1)
        self.endDate = datetime(endYear, endMonth, 22)


    def setAmount(self, amount):
        self.amount = amount


class studentLoan:
    def __init__(self, startingBalance, interestRate, stepPayments, aidvantageLoanNum, enrolledInAutoPay=False):
        self.startingBalance = startingBalance
        self.currentBalance = startingBalance

        self.enrolledInAutoPay = enrolledInAutoPay

        if self.enrolledInAutoPay:
            self.interestRate = (interestRate - 0.25) / 100
        else:
            self.interestRate = interestRate / 100

        self.dailyInterestRate = self.interestRate / 365.25

        self.stepPayments = copy.deepcopy(stepPayments)

        self.aidvantageLoanNum = aidvantageLoanNum

        self.accruedInterest = 0

        self.dateOfLastPayment = None

        self.payoffDate = None


    def setInterestAccrualStartDate(self, startDate):
        self.dateOfLastPayment = startDate - timedelta(days=1)


    def resetLoan(self, date):
        self.currentBalance = self.startingBalance
        self.accruedInterest = 0
        self.setInterestAccrualStartDate(date)


    def payOffLoan(self, date):
        self.currentBalance = 0
        self.payoffDate = date


    def setStepPayments(self, stepPayments):
        self.stepPayments = stepPayments


    def calculateInterestSinceLastPayment(self, date):
        interest = 0

        # Add special 1% autopay interest rate reduction
        onePercentAutopayStartDate = datetime(2026, 7, 1)
        onePercentAutopayEndDate = datetime(2028, 6, 30)
        specialDailyInterestRate = (self.interestRate - (0.75 / 100)) / 365.25

        if self.enrolledInAutoPay and onePercentAutopayStartDate <= date <= onePercentAutopayEndDate:
            # Edge case at beginning of range
            if date - relativedelta(months=1) < onePercentAutopayStartDate:
                startOfMonth = date.replace(day=1)

                timeAtNormalInterest = startOfMonth - self.dateOfLastPayment
                interest = self.currentBalance * self.dailyInterestRate * timeAtNormalInterest.days

                timeAtSpecialInterest = date - startOfMonth
                interest += self.currentBalance * specialDailyInterestRate * timeAtSpecialInterest.days

            # Normal case in the middle of the special interest rate period
            else:
                timeSinceLastPayment = date - self.dateOfLastPayment
                dailyInterestRate = (self.interestRate - (0.75 / 100)) / 365.25
                interest = self.currentBalance * specialDailyInterestRate * timeSinceLastPayment.days

        # Edge case at end of range
        elif self.enrolledInAutoPay and onePercentAutopayEndDate < date <= (onePercentAutopayEndDate + relativedelta(months=1)):
            startOfMonth = date.replace(day=1)

            timeAtSpecialInterest = startOfMonth - self.dateOfLastPayment
            interest = self.currentBalance * specialDailyInterestRate * timeAtSpecialInterest.days

            timeAtNormalInterest = date - startOfMonth
            interest += self.currentBalance * self.dailyInterestRate * timeAtNormalInterest.days

        # Standard case
        else:
            timeSinceLastPayment = date - self.dateOfLastPayment
            interest = self.currentBalance * self.dailyInterestRate * timeSinceLastPayment.days

        return interest


    def applyMonthlyInterest(self, date):
        monthlyInterest = self.calculateInterestSinceLastPayment(date)

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

        # Apply payment and set payoff date if the balance hits 0 as a result of the payment
        if self.currentBalance != 0:
            if paymentAmount >= stepPaymentAmount:
                self.currentBalance -= paymentAmount
            else:
                self.payOffLoan(date)

        self.dateOfLastPayment = date

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
        printStr = f'Aidvantage Loan Number: {self.aidvantageLoanNum}'
        printStr += f'\n\tLoan Starting Balance: ${self.startingBalance:,.2f}'
        printStr += f'\n\tLoan Current Balance: ${round(self.currentBalance, 2):,.2f}'
        printStr += f'\n\tInterest Rate: {round(self.interestRate * 100, 2)}%'
        printStr += f'\n\tDaily Interest Rate: {round(self.dailyInterestRate * 100, 5)}%'
        printStr += f'\n\tEnrolled in AutoPay? {self.enrolledInAutoPay}'
        printStr += f'\n\t\tStep 1 Payment: ${self.stepPayments[0].amount:,.2f}'
        printStr += f'\n\t\tStep 2 Payment: ${self.stepPayments[1].amount:,.2f}'
        printStr += f'\n\t\tStep 3 Payment: ${self.stepPayments[2].amount:,.2f}'
        printStr += f'\n\t\tStep 4 Payment: ${self.stepPayments[3].amount:,.2f}'
        printStr += f'\n\t\tStep 5 Payment: ${self.stepPayments[4].amount:,.2f}'

        return printStr


def createStudentLoansList():
    studentLoans = list()

    payment1 = studentLoanPayment(27.00, 10, 2023, 9, 2025)
    payment2 = studentLoanPayment(35.53, 10, 2025, 9, 2027)
    payment3 = studentLoanPayment(46.76, 10, 2027, 9, 2029)
    payment4 = studentLoanPayment(61.53, 10, 2029, 9, 2031)
    payment5 = studentLoanPayment(80.97, 10, 2031, 6, 2033)
    # studentLoans.append(studentLoan(4441.30, 4.66, [payment1, payment2, payment3, payment4, payment5], 1, False))
    studentLoans.append(studentLoan(4441.30, 4.66, [payment1, payment2, payment3, payment4, payment5], 1, True))

    payment1.setAmount(14.81)
    payment2.setAmount(19.49)
    payment3.setAmount(25.65)
    payment4.setAmount(33.76)
    payment5.setAmount(44.43)
    # studentLoans.append(studentLoan(2436.58, 4.66, [payment1, payment2, payment3, payment4, payment5], 2, False))
    studentLoans.append(studentLoan(2436.58, 4.66, [payment1, payment2, payment3, payment4, payment5], 2, True))

    payment1.setAmount(32.31)
    payment2.setAmount(42.52)
    payment3.setAmount(55.95)
    payment4.setAmount(73.63)
    payment5.setAmount(96.89)
    # studentLoans.append(studentLoan(5425.03, 4.29, [payment1, payment2, payment3, payment4, payment5], 3, False))
    studentLoans.append(studentLoan(5425.03, 4.29, [payment1, payment2, payment3, payment4, payment5], 3, True))

    payment1.setAmount(48.22)
    payment2.setAmount(63.46)
    payment3.setAmount(83.51)
    payment4.setAmount(109.90)
    payment5.setAmount(144.63)
    # studentLoans.append(studentLoan(8097.05, 4.29, [payment1, payment2, payment3, payment4, payment5], 4, False))
    studentLoans.append(studentLoan(8097.05, 4.29, [payment1, payment2, payment3, payment4, payment5], 4, True))

    payment1.setAmount(31.33)
    payment2.setAmount(41.23)
    payment3.setAmount(54.26)
    payment4.setAmount(71.41)
    payment5.setAmount(93.97)
    # studentLoans.append(studentLoan(5419.29, 3.76, [payment1, payment2, payment3, payment4, payment5], 5, False))
    studentLoans.append(studentLoan(5419.29, 3.76, [payment1, payment2, payment3, payment4, payment5], 5, True))

    payment1.setAmount(44.39)
    payment2.setAmount(58.42)
    payment3.setAmount(76.87)
    payment4.setAmount(101.16)
    payment5.setAmount(133.12)
    # studentLoans.append(studentLoan(7677.75, 3.76, [payment1, payment2, payment3, payment4, payment5], 6, False))
    studentLoans.append(studentLoan(7677.75, 3.76, [payment1, payment2, payment3, payment4, payment5], 6, True))

    payment1.setAmount(32.60)
    payment2.setAmount(42.90)
    payment3.setAmount(56.46)
    payment4.setAmount(74.31)
    payment5.setAmount(97.80)
    # studentLoans.append(studentLoan(5426.37, 4.45, [payment1, payment2, payment3, payment4, payment5], 7, False))
    studentLoans.append(studentLoan(5426.37, 4.45, [payment1, payment2, payment3, payment4, payment5], 7, True))

    payment1.setAmount(45.20)
    payment2.setAmount(59.49)
    payment3.setAmount(78.29)
    payment4.setAmount(103.03)
    payment5.setAmount(135.60)
    # studentLoans.append(studentLoan(7523.55, 4.45, [payment1, payment2, payment3, payment4, payment5], 8, False))
    studentLoans.append(studentLoan(7523.55, 4.45, [payment1, payment2, payment3, payment4, payment5], 8, True))

    payment1.setAmount(109.63)
    payment2.setAmount(144.28)
    payment3.setAmount(189.88)
    payment4.setAmount(249.89)
    payment5.setAmount(328.87)
    # studentLoans.append(studentLoan(16222.15, 6.6, [payment1, payment2, payment3, payment4, payment5], 9, False))
    studentLoans.append(studentLoan(16222.15, 6.6, [payment1, payment2, payment3, payment4, payment5], 9, True))

    for loan in studentLoans:
        loan.setInterestAccrualStartDate(datetime(2023, 9, 1))

    return studentLoans


def main():
    studentLoans = createStudentLoansList()
    studentLoans.sort(key=lambda x: (x.interestRate, -x.startingBalance), reverse=True)

    desiredPayment = 675

    # Create range of payment due dates
    paymentDates = pd.date_range(start = datetime(2023, 10, 1), end = datetime(2033, 6, 30), freq = "MS").to_pydatetime().tolist()
    paymentDates = [paymentDate.replace(day=22) for paymentDate in paymentDates]

    for paymentDate in paymentDates:
        # Apply monthly interest for each loan
        for loan in studentLoans:
            loan.applyMonthlyInterest(paymentDate)

        paymentObligation = sum((loan.calculateMonthlyPayment(paymentDate)[0] for loan in studentLoans))

        if paymentObligation > desiredPayment:
            print(f'NOTE: payment for {paymentDate.month}/{paymentDate.year} will be higher than the desired payment amount. Obligation: ${paymentObligation:,.2f}')
            extraPayment = 0
        else:
            extraPayment = desiredPayment - paymentObligation

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

        # # NOTE: Due to calling the applyMonthlyInterest() method, this slightly bungles the final calculation.
        # # We should:
        # #   (a) Figure out how to print better so we don't need to apply the interest, we can just calculate and add it
        # #   (b) make this optional with e.g. a command-line flag
        # today = datetime.today()
        # nextPaymentDate = paymentDate + relativedelta(months=1)
        # if paymentDate <= today <= nextPaymentDate:
        #     print("You are here:")
        #     print(f"paymentDate: {paymentDate}")
        #     print(f"today: {today}")
        #     print(f"nextPaymentDate: {nextPaymentDate}")

        #     print()

        #     for loan in studentLoans:
        #         loan.applyMonthlyInterest(today)
        #         print(loan)
        #         print()

    print()

    totalInterest = 0

    for loan in studentLoans:
        if loan.payoffDate is not None:
            print(f'Loan {loan.aidvantageLoanNum} payoff date: {loan.payoffDate}')
        else:
            print(f'Payoff date not set for Loan {loan.aidvantageLoanNum}')

    print()

    for loan in studentLoans:
        totalInterest += loan.accruedInterest
        print(f'Loan {loan.aidvantageLoanNum}: Total interest: ${round(loan.accruedInterest, 2):,.2f}')

    print(f'\nTotal Interest: ${round(totalInterest, 2):,.2f}')

    return 0


if __name__ == "__main__":
    sys.exit(main())
