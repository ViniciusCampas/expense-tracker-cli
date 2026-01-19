#Version 1.0
#19/01/2026
#Vinicius Camparini Siqueira

import argparse
from datetime import datetime
import csv

def idGenerator(expenses):
    if expenses:
        return max(expense['expenseId'] for expense in expenses)+1
    return 1

def addColector(expenses,description,amount,category):
    return {'expenseId':idGenerator(expenses),
            'date':datetime.now().strftime('%d-%m-%y'),
            'description':description,
            'amount':amount,
            'category':category}
        

def addExpenses(expenses,description,amount,category):
    expense=addColector(expenses,description,amount,category)
    expenses.append(expense)


def updateExpenses(expenses,expenseID,description,amount,category):
    for expense in expenses:
        if expense['expenseId'] ==expenseID:
            if description:
                expense['description']=description
            if amount:
                expense['amount']=amount
            expense['category']=category
            return True
    return False

def deleteExpenses(expenses, expenseID):
    for expense in expenses:
        if expense['expenseId'] ==expenseID:
            expenses.remove(expense)
            return True
    return False

def listExpenses(expenses):
    print(f'#   {'ID':<3}   {'Date':<10}    {'Description':<24}   {'Category':<15}  {'Amount':>7}')
    for expense in expenses:
        print(f'# | {expense['expenseId']:<3} | {expense['date']:<10} | {expense['description']:<25} | {expense['category']:<15} | {expense['amount']:>8.2f}')

def summaryExpenses(expenses):
    total=0.0
    for expense in expenses:
        total+=expense['amount']
    print(f'Total expenses: ${total}')

def summaryMonth(expenses,month):
    total=0.0
    for expense in expenses:
        monthExpense=expense['date'].split('-')
        if monthExpense[1]==month:
            total+=expense['amount']
    print(f'Total expenses: ${total}')

def save(file, expenses):
    fields = ['expenseId', 'date', 'description', 'amount', 'category']
    with open(file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        if expenses:
            writer.writerows(expenses)

    
def load(file):
    try:
        with open(file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            expenses = list(reader)
            for expense in expenses:
                expense['expenseId'] = int(expense['expenseId'])
                expense['amount'] = float(expense['amount'])
            return expenses
    except FileNotFoundError:
        save(file, [])
        return []


FILEPATH='expenses.csv'
expenses=load(FILEPATH)

parser = argparse.ArgumentParser()
subparsers= parser.add_subparsers(dest='commands')
add= subparsers.add_parser('add')
update=subparsers.add_parser('update')
delete=subparsers.add_parser('delete')
list=subparsers.add_parser('list')
summaryExp=subparsers.add_parser('summary')

add.add_argument('--description',type=str,required=True,help='Provide a description for the expense')
add.add_argument('--amount',type=float,required=True,help='Provide the expense amount')
add.add_argument('--category',type=str,default='general',help='Provide the expense category; if not provided, it will default to "general"')

update.add_argument('--expenseId',type=int,required=True,help='Provide the ID of the expense to updated')
update.add_argument('--description',type=str,help='Provide a new description for the expense')
update.add_argument('--amount',type=float,help='Provide a new amount for the expense')
update.add_argument('--category',type=str,default='general',help='Provide the expense category; if not provided, it will default to "general"')

delete.add_argument('--expenseId',type=int,required=True,help='Provide the ID of the expense to deleted')

summaryExp.add_argument('--month',type=str,help='Provide the expense month in MM format')

args=parser.parse_args()

if args.commands == 'add':
        addExpenses(expenses,args.description,args.amount,args.category)
        save(FILEPATH,expenses)
        print ('Expense successfully added')
elif args.commands == 'update':
        updateExpenses(expenses,args.expenseId,args.description,args.amount,args.category)
        save(FILEPATH,expenses)
        print(f'ID:{args.expenseId}, expense successfully updated')
elif args.commands == 'delete':
    deleteExpenses(expenses,args.expenseId)
    save(FILEPATH,expenses)
    print(f'ID:{args.expenseId}, expense successfully deleted')
elif args.commands == 'list':
    listExpenses(expenses)
elif args.commands == 'summary':
    if args.month:
        summaryMonth(expenses,args.month)
    else:
        summaryExpenses(expenses)
