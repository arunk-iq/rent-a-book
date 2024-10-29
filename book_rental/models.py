from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from dateutil.relativedelta import relativedelta


User = get_user_model()

class Book(models.Model):
    title = models.CharField(max_length=250)
    authors = models.CharField(max_length=500)
    page_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rentals')
    rented_on = models.DateTimeField(default=timezone.now)
    return_date = models.DateField()
    rental_cost = models.DecimalField(max_digits=6, decimal_places=2)  # Add rental cost field

    def __str__(self):
        return f"{self.user.username} rented {self.book.title}"

    def calculate_rental_cost(self):
        # Ensure both rented_on and return_date dates are set
        if self.rented_on and self.return_date:
            # Calculate the month difference
            diff = relativedelta(self.return_date, self.rented_on)
            month_difference = diff.years * 12 + diff.months + (1 if diff.days > 0 else 0)  # Count an extra month if there are leftover days
            # Calculate rental cost based on page count
            page_count_factor = self.book.page_count / 100 if self.book.page_count else 0
            if month_difference == 1:
                return 0
            else:
                rental_cost = (month_difference-1) * page_count_factor
                return round(rental_cost, 2)
        return 0.00

    def save(self, *args, **kwargs):
        # Set return_date to one month from rented_on if it’s not already set
        if not self.return_date:
            self.return_date = self.rented_on + relativedelta(months=1)

        # Calculate and set the rental cost
        self.rental_cost = self.calculate_rental_cost()

        super().save(*args, **kwargs)





