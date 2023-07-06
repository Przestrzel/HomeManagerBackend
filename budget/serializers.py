from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, Serializer
from budget.models import ExpenseCategory, Expense, Income, Budget, PlannedExpense, Period
from users.models import User, Family


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class FamilySerializer(ModelSerializer):
    class Meta:
        model = Family
        fields = ("id", "family_name")


class ExpenseCategorySerializer(ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = "__all__"


class ExpenseCategoryWithoutFamilySerializer(ExpenseCategorySerializer):
    class Meta:
        model = ExpenseCategory
        exclude = ("family",)


class ExpenseSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    category = ExpenseCategoryWithoutFamilySerializer()

    class Meta:
        model = Expense
        fields = "__all__"


class ExpenseCreateSerializer(ExpenseSerializer):
    category = PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())


class IncomeSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Income
        fields = "__all__"


class IncomeCreateSerializer(IncomeSerializer):
    family = PrimaryKeyRelatedField(queryset=Family.objects.all())


class PlannedExpenseSerializer(ModelSerializer):
    category = ExpenseCategoryWithoutFamilySerializer()

    class Meta:
        model = PlannedExpense
        fields = "__all__"


class PlannedExpenseCreateSerializer(ModelSerializer):
    class Meta:
        model = PlannedExpense
        fields = "__all__"


class BudgetSerializer(ModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"


class RevenueRequestSerializer(Serializer):
    period = serializers.ChoiceField(choices=Period.choices, default=Period.MONTH)
    date = serializers.DateTimeField(format="%Y-%m-%d")
    budget = PrimaryKeyRelatedField(queryset=Budget.objects.all())

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return None


class RevenueByCategorySerializer(Serializer):
    amount = serializers.FloatField()
    planned_amount = serializers.FloatField()

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return None


class RevenueResponseSerializer(Serializer):
    income = serializers.FloatField()
    expenses = serializers.DictField(child=RevenueByCategorySerializer())

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return None
