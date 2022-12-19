from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from budget.models import ExpenseCategory, Expense
from budget.serializers import ExpenseCategorySerializer, ExpenseSerializer
from utils.permissions import IsFamilyMember


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated, IsFamilyMember]
    pagination_class = None


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsFamilyMember]

    def check_permissions(self, request):
        if request.method == "DELETE":
            self.permission_classes = [IsAuthenticated]
        super().check_permissions(request)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        is_destroying_own_expense = request.user.family.filter(id=instance.family.id).exists()
        if not is_destroying_own_expense:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


