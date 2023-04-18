
from rest_framework_json_api import serializers

from sales.models import *


class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.display_name")
    manufacturing_cost = serializers.FloatField()

    class Meta:
        model = Article
        resource_name = "articles"
        fields = ["id", "code", "category", "name", "manufacturing_cost"]

class SaleSerializer(serializers.ModelSerializer):
    article_category = serializers.CharField(source="article.category")
    article_code = serializers.CharField(source="article.code")
    article_name = serializers.CharField(source="article.name")
    unit_selling_price = serializers.FloatField()
    total_selling_price = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        resource_name = "sales"
        fields = ["id", "date", "article_category", "article_code", "article_name", "quantity", "unit_selling_price", "total_selling_price"]

    def get_total_selling_price(self, obj):
        return int(obj.quantity) * float(obj.unit_selling_price)
    
class SalesByArticleSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    category_name = serializers.CharField()
    total_selling_price = serializers.FloatField()
    margin_percentage = serializers.SerializerMethodField()
    last_sale_date = serializers.DateField()

    class Meta:
        fields = ["code", "name", "category_name", "total_selling_price", "margin_percentage", "last_sale_date"]
        
    def get_margin_percentage(self, obj):
        try:
            result = (float(obj["total_selling_price"]) - float(obj["total_manifacturing_cost"])) / float(obj["total_manifacturing_cost"])
        except:
            result = 0
        return result
