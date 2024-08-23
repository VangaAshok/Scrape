from django.db import models

class Product(models.Model):
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    product_url = models.URLField(max_length=1024)
    description = models.TextField()

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1024)

    def __str__(self):
        return f"Image for {self.product.name}"
