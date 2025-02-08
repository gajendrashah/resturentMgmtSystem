from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError

# Model for Table Numbers
class Table(models.Model):
    table_number = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Table {self.table_number}"

    class Meta:
        ordering = ['table_number']

# Model for Item Categories
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# Model for Subcategories
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    

# Model for Menu Items
class MenuItem(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# Model for Building
class Building(models.Model):
    building_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.building_name

# Model for Room
class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.building.building_name} - Room {self.room_number}"

    class Meta:
        unique_together = ('building', 'room_number')

# Model for Customer
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# Model for Cart
class Cart(models.Model):
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name='carts')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not (self.table or self.customer):
            raise ValidationError('Either table or customer must be selected')

    def __str__(self):
        if self.table:
            return f"Cart for Table {self.table.table_number}"
        elif self.customer:
            return f"Cart for Customer {self.customer.name}"
        return "Unassigned Cart"

    class Meta:
        ordering = ['-created_at']

# Model for Cart Items
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} in Cart {self.cart.id}"

    class Meta:
        unique_together = ('cart', 'menu_item')

# Model for Sales
class Sale(models.Model):
    STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),   
    ]

    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='sale')
    sale_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Unpaid')

    def __str__(self):
        return f"Sale {self.id} - {self.status}"

    class Meta:
        ordering = ['-sale_date']

# Model for Purchases (Inventory Management)
class Purchase(models.Model):
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    bill_number = models.CharField(max_length=10)
    remarks = models.TextField(blank=True, null=True)
    purchase_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Purchase of {self.item_name} on {self.purchase_date}"

    class Meta:
        ordering = ['-purchase_date']