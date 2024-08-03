from django.db import models

from LibraryAPI import settings
from django.core.validators import URLValidator


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(
        max_length=4,
        choices=CoverType.choices,
        default=CoverType.SOFT,
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book_id = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Borrowing by {self.user.__str__()} on {self.borrow_date}"


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(
        max_length=7,
        choices=Status.choices,
        default=Status.PENDING
    )
    type = models.CharField(
        max_length=7,
        choices=Type.choices,
        default=Type.PAYMENT
    )
    borrowing = models.ForeignKey(Borrowing, on_delete=models.SET_NULL)
    session_url = models.URLField(validators=[URLValidator()])
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment of {self.money_to_pay} for borrowing {self.borrowing.id}, user: {self.borrowing.user.__str__()}"
