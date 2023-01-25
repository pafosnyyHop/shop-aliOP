from django.db import models
from product.models import Product
from aliOP import settings


class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product')
    rating = models.PositiveIntegerField(
        null=False,
        blank=False)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        unique_together = [
            'user',
            'product']

