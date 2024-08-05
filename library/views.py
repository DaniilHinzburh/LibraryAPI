from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import *
from library.models import *
from library.serializers import BookSerializer, BorrowingSerializer, PaymentSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        book_title = serializer.validated_data["book"]
        book = Book.objects.get(title=book_title)
        if book.inventory <= 0:
            return Response({"error": "The book is not available"}, status=400)
        book.inventory -= 1
        book.save()

        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        if serializer.validated_data.get("actual_return_date"):
            book = instance.book
            book.inventory += 1
            book.save()

        return Response(serializer.data)



class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
