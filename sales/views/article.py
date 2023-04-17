from sales.models import *
from sales.serializers import ArticleSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def create(self, request):
        # Get category
        category_name = request.data.get("category")
        if not category_name:
            raise ValueError("The field category is mandatory")
        try:
            category = ArticleCategory.objects.get(display_name=category_name)
        except:
            category=None
        if not category:
            raise ValueError("Unknown category")
        
        # Create article
        article = Article(
            code=request.data.get("code"),
            name=request.data.get("name"),
            category=category,
            manufacturing_cost=request.data.get("manufacturing_cost")
        )
        article.save()
        
        # Return json response
        serializer = self.serializer_class(article, many=False, context={"request": request})
        return Response(serializer.data, status=201)
    

    def update(self, request):
        raise MethodNotAllowed("update")
    
    
    def destroy(self, request):
        raise MethodNotAllowed("destroy")
