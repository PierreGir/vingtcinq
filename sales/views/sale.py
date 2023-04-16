from sales.models import Sale
from sales.serializers import SaleSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
