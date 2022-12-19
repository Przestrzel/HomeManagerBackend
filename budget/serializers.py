from rest_framework.serializers import ModelSerializer
from budget.models import ExpenseCategory, Expense
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
    family = FamilySerializer(read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'
