
from rest_framework_json_api import serializers

from sales.models import *


class SaleSerializer(serializers.HyperlinkedModelSerializer):
    quantity = serializers.IntegerField()

    class Meta:
        model = Sale
        resource_name = "sales"
        fields = ["quantity"]


