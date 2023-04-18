from sales.models import Sale, Article
from sales.serializers import SaleSerializer, SalesByArticleSerializer
from rest_framework import decorators, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, F, Max
from rest_framework_json_api.pagination import JsonApiPageNumberPagination


class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    pagination_class = JsonApiPageNumberPagination
    pagination_class.page_size = 25
    
    def create(self, request):
        # Get article
        try:
            article_code = request.data.get("article_code")
        except:
            article_code=None
        if not article_code:
            raise ValueError("The field article_code is mandatory")
        article = Article.objects.get(code=article_code)

        # Create sale
        sale = Sale(
            date=request.data.get("date"),
            author=request.user,
            article=article,
            quantity=request.data.get("quantity"),
            unit_selling_price=request.data.get("unit_selling_price"),
        )
        sale.save()
        
        # Return json response
        serializer = self.serializer_class(sale, many=False, context={"request": request})
        return Response(serializer.data, status=201)
    
    def update(self, request, pk=None, partial=False):
        # Get sale 
        sale = Sale.objects.get(id=pk)
        if sale.author != request.user:
            raise PermissionDenied
        
        # Get article
        try:
            article_code = request.data.get("article_code")
        except:
            article_code=None
        if article_code:
            article = Article.objects.get(code=article_code)
        else: 
            article = None
    
        # Update sale
        sale.date = request.data.get("date")
        sale.quantity = request.data.get("quantity")
        sale.unit_selling_price=request.data.get("unit_selling_price")
        if article: 
            sale.article = article 
        sale.save()
        
        # Return json response
        serializer = self.serializer_class(sale, many=False, context={"request": request})
        return Response(serializer.data, status=200)
    
    def destroy(self, request, pk=None, partial=False):
        # Get sale 
        sale = Sale.objects.get(id=pk)
        if sale.author != request.user:
            raise PermissionDenied
        
        # Delete sale
        sale.delete()
        
        # Return response
        return Response(None, status=204)
    
    @decorators.action(detail=False, methods=["get"])
    def sales_by_article(self, request):
        
        # Get sales by article
        sales_by_article = Article.objects.annotate(
            category_name=F('category__display_name'),
            total_selling_price=Sum(F('sales__quantity') * F('sales__unit_selling_price')),
            total_manifacturing_cost=Sum(F('sales__quantity') * F('manufacturing_cost')),
            last_sale_date=Max("sales__date")
        ).values(
            "code",
            "name",
            "category_name", 
            "total_selling_price", 
            "total_manifacturing_cost",
            "last_sale_date"
        ).order_by("-total_selling_price")
        

        # Apply pagination
        page = self.paginate_queryset(sales_by_article)
        if page is not None:
            serializer = SalesByArticleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Serialize
        serializer = SalesByArticleSerializer(sales_by_article, many=True)
        return Response(serializer.data)