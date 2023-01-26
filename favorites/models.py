from django.db import models

from product.models import Product


class Favorites(models.Model):
    owner = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE,
                              related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='favorites')

    class Meta:
        unique_together = ['owner', 'product']

