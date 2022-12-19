from rest_framework.serializers import ModelSerializer
from budget.models import ExpenseCategory


class ExpenseCategorySerializer(ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
