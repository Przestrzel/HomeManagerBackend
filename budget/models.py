from django.db import models


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    family = models.ForeignKey('users.Family', on_delete=models.CASCADE, default=None, null=True)

    class Meta:
        verbose_name_plural = "Expense categories"

    def __str__(self):
        return self.name


class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name="expenses")
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    family = models.ForeignKey('users.Family', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Income(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    family = models.ForeignKey('users.Family', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PlannedExpense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name="planned_expenses")
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE, related_name="planned_expenses")

    def __str__(self):
        return self.category.name


class Budget(models.Model):

    class Period(models.TextChoices):
        WEEK = "WEEK"
        MONTH = "MONTH"
        YEAR = "YEAR"

    family = models.ForeignKey('users.Family', on_delete=models.CASCADE)
    period = models.CharField(max_length=5, choices=Period.choices, default=Period.MONTH)
