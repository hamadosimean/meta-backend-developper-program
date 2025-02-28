from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify

# Create your models here.


# Adding custom user model
class CustomUser(AbstractUser):
    contact = models.CharField(max_length=225, blank=True, null=True)
    # bio = models.TextField(null=True, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    # photo = models.ImageField(upload_to="images", blank=True, null=True)
    # birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


# Category model
class Category(models.Model):
    slug = models.SlugField(db_index=True)
    title = models.CharField(max_length=225)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slug)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


# Menu item model
class MenuItem(models.Model):
    title = models.CharField(max_length=225, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    # image = models.ImageField(upload_to="menu_items/", blank=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title


# Cart model , this cart must be empty upon submission for orders
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ("user", "menuitem")

    def __str__(self) -> str:
        return self.user.username


# Order tables
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="delivery_crew",
        null=True,
    )
    status = models.BooleanField(
        db_index=True, default=0
    )  # This field allows to get the status of the order , whether it is cancel, delivered or spending
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)

    def __str__(self) -> str:
        return self.user.username + " " + self.delivery_crew.username


# Orders items tables
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ("user", "menuitem")

    def __str__(self) -> str:
        return self.user.username
