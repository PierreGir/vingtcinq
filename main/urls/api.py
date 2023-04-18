from django.urls import path, include

from rest_framework import routers
import sales.views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"articles", sales.views.ArticleViewSet)
router.register(r"sales", sales.views.SaleViewSet)

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("", include(router.urls)),
                path('sales_by_article', sales.views.SaleViewSet.as_view({'get': 'sales_by_article'}), name='sales_by_article'),
            ]
        ),
    )
]
