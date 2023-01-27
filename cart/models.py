from django.db import models
from django.contrib.auth import get_user_model

from product.models import Product

User = get_user_model()


class Cart(models.Model):
    """ Корзина """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    products = models.ManyToManyField('CartProduct', blank=True, related_name='related_cart')
    final_price = models.IntegerField(default=0, verbose_name='Общая цена')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartProduct(models.Model):
    """ Объект корзины """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True)
    final_price = models.IntegerField(verbose_name='Общая цена', blank=True)

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Объект: {self.product.title} (для корзины)"

    class Meta:
        verbose_name = 'Объект корзины'
        verbose_name_plural = 'Объекты корзины'


class Order(models.Model):
    """ Заказ """
    user = models.ForeignKey(User, related_name='userorders', verbose_name="Покупатель", on_delete=models.CASCADE,
                             blank=True, null=True)
    products = models.ManyToManyField('OrderItem', blank=True, related_name='related_order')
    user_comment = models.TextField(blank=True,
                                    null=True)
    name = models.CharField('имя заказчика', max_length=250, null=True)
    last_name = models.CharField('фамилия заказчика', max_length=250, null=True)
    telephone = models.CharField('телефон заказчика', max_length=250, null=True)
    final_price = models.IntegerField(default=1)
    paid = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    """ Предмет заказа """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True)
    final_price = models.IntegerField(verbose_name='Общая цена', blank=True)

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.product}'

    class Meta:
        verbose_name = 'Объект заказа'
        verbose_name_plural = 'Объекты заказа'
