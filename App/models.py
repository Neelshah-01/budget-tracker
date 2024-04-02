from django.db import models
from django.db.models import IntegerField, Sum
from django.db.models.functions import Cast

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=[('expense', 'Expense'), ('income', 'Income')])
    notes = models.TextField(blank=True, null=True)
    
    @classmethod
    def total_income_expenses(cls, transactions=None):
        if transactions is None:
            transactions = cls.objects.all()
        total_income = transactions.filter(type='income').aggregate(total=Cast(Sum('amount'), IntegerField()))['total'] or 0
        total_expenses = transactions.filter(type='expense').aggregate(total=Cast(Sum('amount'), IntegerField()))['total'] or 0
        return total_income, total_expenses
    
    def __str__(self):
        return f"Transaction of {self.amount} on {self.date}"
