from django.urls import path, include

from rest_framework import routers
import sales.views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"sales", sales.views.SaleViewSet)

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("", include(router.urls)),
            ]
        ),
    )
]
