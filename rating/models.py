from django.db import models
from product.models import Product
from django.contrib.auth import get_user_model
from aliOP import settings

User = get_user_model()


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        ordering = ["-value"]


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product')
    rating = models.ForeignKey(RatingStar, on_delete=models.CASCADE, related_name='stars')

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return f'{self.user} - {self.product} - {self.rating}'

