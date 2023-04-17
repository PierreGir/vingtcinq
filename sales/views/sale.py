from sales.models import Sale, Article
from sales.serializers import SaleSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied


class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    
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
