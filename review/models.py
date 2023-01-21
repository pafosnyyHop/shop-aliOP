from django.db import models


class Review(models.Model):
    """ Отзыв """
    # owner = models.ForeignKey('auth.User', related_name='reviews', on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    body = models.TextField(max_length=555)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.body} {self.created_at}'  # -> {self.product}

    class Meta:
        ordering = ('created_at',)


class ReviewImages(models.Model):
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='images/')
    # review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
