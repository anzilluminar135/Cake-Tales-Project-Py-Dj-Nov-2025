from django.db import models


import uuid
# Create your models here.

from django.db.models import Sum


class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True,default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta :

        abstract = True

# class CategoryChoices(models.TextChoices):

#     WEDDING_CAKES = 'Wedding Cakes','Wedding Cakes'

#     BIRTHDAY_CAKES = 'Birthday Cakes','Birthday Cakes'

#     PLUM_CAKES = 'Plum Cakes','Plum Cakes'

#     CUP_CAKES = 'Cup Cakes','Cup Cakes'

class Category(BaseClass):

    name = models.CharField(max_length=30)


    def __str__(self):

        return self.name
    
    class Meta :

        verbose_name = 'Categories'

        verbose_name_plural = 'Categories'


# class FlavourChoices(models.TextChoices):

#     VANILLA = 'Vanilla','Vanilla'

#     CHOCOLATE = 'Chocolate','Chocolate'

#     BUTTERSCOTCH = 'Butterscotch','Butterscotch'

#     STRAWBERRY = 'Strawberry','Strawberry'

#     RED_VELVET = 'Red Velvet','Red Velvet'

#     BLACK_FOREST = 'Black Forest','Black Forest'

#     WHITE_FOREST = 'White Forest','White Forest'

#     PINEAPPLE = 'Pineapple','Pineapple'

#     BLUEBERRY = 'Blueberry','Blueberry'

#     MANGO = 'Mango','Mango'

#     OREO = 'Oreo','Oreo'

class Flavour(BaseClass):

    name = models.CharField(max_length=30)


    def __str__(self):

        return self.name
    
    class Meta :

        verbose_name = 'Flavours'

        verbose_name_plural = 'Flavours'


# class ShapeChoices(models.TextChoices):

#     ROUND = 'Round','Round'

#     SQUARE = 'Square','Square'

#     RECTANGLE = 'Rectangle','Rectangle'

#     HEART = 'Heart','Heart'

#     OVAL = 'Oval','Oval'
class Shape(BaseClass):

    name = models.CharField(max_length=30)


    def __str__(self):

        return self.name
    
    class Meta :

        verbose_name = 'Shapes'

        verbose_name_plural = 'Shapes'

# class WeightChoices(models.TextChoices):

#     HALF_KG = '1/2 kg','1/2 kg'    

#     ONE_KG = '1 kg','1 kg'

#     TWO_KG = '2 kg','2 kg'

#     THREE_KG = '3 kg','3 kg'

class Weight(BaseClass):

    name = models.CharField(max_length=30)


    def __str__(self):

        return self.name
    
    class Meta :

        verbose_name = 'Weights'

        verbose_name_plural = 'Weights'


class Cake(BaseClass):

    name = models.CharField(max_length=50)

    description = models.TextField()

    photo = models.ImageField(upload_to='cake-images')

    category = models.ForeignKey('Category',on_delete=models.CASCADE)

    flavour = models.ForeignKey('Flavour',on_delete=models.CASCADE)

    shape = models.ForeignKey('Shape',on_delete=models.CASCADE)

    weight = models.ForeignKey('Weight',on_delete=models.CASCADE)

    egg_added = models.BooleanField(default=True)

    is_available = models.BooleanField(default=True)

    price = models.FloatField()

    def __str__(self):

        return self.name
    
    class Meta :

        verbose_name = 'Cakes'

        verbose_name_plural = 'Cakes'


class Wishlist(BaseClass):

    user = models.OneToOneField('authentication.Profile',on_delete=models.CASCADE)

    cakes = models.ManyToManyField('Cake')

    def __str__(self):

        return f'{self.user.username} wishlist'
    
    class Meta :

        verbose_name = 'Wishlists'

        verbose_name_plural = 'Wishlists'

class Cart(BaseClass):

    user = models.OneToOneField('authentication.Profile',on_delete=models.CASCADE)

    cakes = models.ManyToManyField('Cake')

    def __str__(self):

        return f'{self.user.username} cart'
    
    class Meta :

        verbose_name = 'Carts'

        verbose_name_plural = 'Carts'

    @property
    def get_total(self):

        total = self.cakes.aggregate(total=Sum('price')).get('total')

        return total if total else 0
    

class PaymentMethodChoices(models.TextChoices):

    COD = 'COD','COD'

    ONLINE = 'Online','Online'


class DeliveryAddress(BaseClass):

    user = models.ForeignKey('authentication.Profile',on_delete=models.CASCADE,related_name='deliveryaddress') 

    house_or_building_name = models.CharField(max_length=30)  

    landmark = models.CharField(max_length=20)

    place = models.CharField(max_length=15) 

    pincode = models.CharField(max_length=6)

    def __str__(self):

        return f'{self.user.username} Delivery Addresses'
    
    class Meta :

        verbose_name = 'Delivery Addresses'

        verbose_name_plural = 'Delivery Addresses'
    

class Order(BaseClass):

    user = models.ForeignKey('authentication.Profile',on_delete=models.CASCADE)  

    order_id = models.CharField(max_length=10)

    cakes = models.ManyToManyField('Cake')  

    total_price = models.FloatField()

    payment_method = models.CharField(max_length=10,choices=PaymentMethodChoices.choices,null=True,blank=True)

    delivery_address = models.ForeignKey('DeliveryAddress',on_delete=models.CASCADE,null=True,blank=True)

    order_placed = models.BooleanField(default=False)

    def __str__(self):

        return f'{self.user.username}-{self.order_id}'
    
    class Meta :

        verbose_name = 'Orders'

        verbose_name_plural = 'Orders'

