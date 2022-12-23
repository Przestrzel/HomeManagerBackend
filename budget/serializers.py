from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from budget.models import ExpenseCategory, Expense, Income
from users import serializers
from users.models import User, Family


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class FamilySerializer(ModelSerializer):
    class Meta:
        model = Family
        fields = ('id', 'family_name')


class ExpenseCategorySerializer(ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class ExpenseCategoryWithoutFamilySerializer(ExpenseCategorySerializer):
    class Meta:
        model = ExpenseCategory
        exclude = ('family',)


class ExpenseSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    category = ExpenseCategoryWithoutFamilySerializer()
    family = FamilySerializer()

    class Meta:
        model = Expense
        fields = '__all__'


class ExpenseCreateSerializer(ExpenseSerializer):
    category = PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())
    family = PrimaryKeyRelatedField(queryset=Family.objects.all())


class IncomeSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    family = FamilySerializer()

    class Meta:
        model = Income
        fields = '__all__'


class IncomeCreateSerializer(IncomeSerializer):
    family = PrimaryKeyRelatedField(queryset=Family.objects.all())
