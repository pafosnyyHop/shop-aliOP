from django.db import models
from product.models import Product


class Like(models.Model):
    owner = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE,
                              related_name='liked_posts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='likes')

    class Meta:
        unique_together = ['owner', 'product']
