from django.db import models


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Shop(BaseModel):
    title = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.title


class ProductType(BaseModel):
    title = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=511)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    price_credit = models.DecimalField(max_digits=20, decimal_places=2,
                                       blank=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,
                             related_name='products', blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE,
                                     related_name='products', blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.title


class DataDict(BaseModel):
    json_data = models.JSONField(blank=True)
    users_data = models.JSONField(blank=True)
    texts_data = models.JSONField(blank=True)
    objects = models.Manager()

    def __str__(self):
        return f"DataDict(pk = {self.pk})"


class User(BaseModel):
    chat_id = models.IntegerField()

    first_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)

    language = models.CharField(max_length=5, default='uz')
    current_text = models.CharField(max_length=255, default='')
    current_values = models.JSONField(blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f'User(chat_id={self.chat_id})'


class UserHistory(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE,
                             related_name='histories')
    texts = models.JSONField(blank=True, null=True)
    values = models.JSONField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return f"UserHistory(pk = {self.pk}, user_id = {self.user_id})"
