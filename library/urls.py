from django.urls import path, include
from library.views import *
from rest_framework import routers

app_name = "library"

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("borrowing", BorrowingViewSet)
router.register("payments", PaymentViewSet)

urlpatterns = router.urls
