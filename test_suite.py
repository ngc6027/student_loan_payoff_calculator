import sys

import pandas as pd
from datetime import datetime
import itertools

import graduated_student_loans


class TestResult:
    def __init__(self):
        self.order = None
        self.totalInterest = 0


def main():
    studentLoans = graduated_student_loans.createStudentLoansList()

    desiredPayment = 675

    # Create range of payment due dates
    paymentDates = pd.date_range(start = datetime(2023, 10, 1), end = datetime(2033, 6, 30), freq = "MS").to_pydatetime().tolist()
    paymentDates = [paymentDate.replace(day=22) for paymentDate in paymentDates]

    loan_order_permutations = itertools.permutations(studentLoans)
    results = list()

    for studentLoans in loan_order_permutations:
        result = TestResult()
        result.order = [loan.aidvantageLoanNum for loan in studentLoans]

        for paymentDate in paymentDates:
            # Apply monthly interest for each loan
            for loan in studentLoans:
                loan.applyMonthlyInterest(paymentDate)

            paymentObligation = sum((loan.calculateMonthlyPayment(paymentDate)[0] for loan in studentLoans))

            if paymentObligation > desiredPayment:
                # print(f'NOTE: payment for {paymentDate.month}/{paymentDate.year} will be higher than the desired payment amount. Obligation: ${paymentObligation:,.2f}')
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

        totalInterest = 0

        for loan in studentLoans:
            totalInterest += loan.accruedInterest

        result.totalInterest = totalInterest
        results.append(result)

        for loan in studentLoans:
            loan.resetLoan(datetime(2023, 9, 1))

    results.sort(key=lambda x: x.totalInterest)
    print(f"Lowest interest: ${results[0].totalInterest:,.2f}, Payoff order: {results[0].order}")
    print(f"Highest interest: ${results[-1].totalInterest:,.2f}, Payoff order: {results[-1].order}")

    with open("results_no1p.txt", "w") as f:
        for result in results:
            f.write(f"Interest: ${result.totalInterest:,.2f}, Payoff order: {result.order}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
