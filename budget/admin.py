from django.contrib import admin
from budget.models import Budget, Expense, Income, ExpenseCategory, PlannedExpense


# Register your models here.


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["family", "period"]
    search_fields = ["family__family_name"]
    ordering = ["-id"]


@admin.register(PlannedExpense)
class PlannedExpenseAdmin(admin.ModelAdmin):
    list_display = ["category", "budget", "amount"]
    search_fields = ["category__name"]
    ordering = ["-id"]


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "family"]
    search_fields = ["name", "description", "family__family_name"]
    ordering = ["-id"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["name", "amount", "date", "category", "user", "family"]
    search_fields = ["name", "category__name", "user__email", "family__family_name"]
    ordering = ["-id"]


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ["name", "amount", "date", "user", "family"]
    search_fields = ["name", "user__email", "family__family_name"]
    ordering = ["-id"]