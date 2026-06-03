from django.db import models


class UserRegister(models.Model):

    ROLE_CHOICES = [

        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('both', 'Buyer + Seller'),
        ('admin', 'Admin'),

    ]
    

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=10
    )

    image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=6
    )

    # Increased max_length for hashed password

    password = models.CharField(
        max_length=255
    )

    id_proof = models.FileField(
        upload_to='idproofs/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    status = models.CharField(max_length=20, 
       default='active')
    
    def __str__(self):

        return f"{self.first_name} {self.last_name}"
   


class Category(models.Model):

    category_name = models.CharField(max_length=100)

    def __str__(self):

        return self.category_name


class SubCategory(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    subcategory_name = models.CharField(max_length=100)

    def __str__(self):

        return self.subcategory_name
    # PRODUCT MODEL
class Product(models.Model):

    STATUS_CHOICES = [

        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),

    ]

    AUCTION_STATUS = [

        ('upcoming', 'Upcoming'),
        ('live', 'Live'),
        ('ended', 'Ended'),

    ]

    CONDITION_CHOICES = [

        ('new', 'New'),
        ('used', 'Used'),

    ]

    seller = models.ForeignKey(
        UserRegister,
        on_delete=models.CASCADE
    )

    product_name = models.CharField(max_length=200)

    description = models.TextField()

    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE
    )

    starting_bid = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    current_bid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    winner = models.ForeignKey(
    UserRegister,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='won_auctions'
)

    bid_count = models.IntegerField(default=0)

    auction_end_time = models.DateTimeField()

    auction_status = models.CharField(
        max_length=20,
        choices=AUCTION_STATUS,
        default='upcoming'
    )

    product_image = models.ImageField(
        upload_to='products/'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    payment_status = models.CharField(
    max_length=20,
    choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid')
    ],
    default='pending'
)
    

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    auction_notification_sent = models.BooleanField(
        default=False
    )
    def save(self, *args, **kwargs):

        if not self.current_bid:

            self.current_bid = self.starting_bid

        super().save(*args, **kwargs)

    def __str__(self):

        return self.product_name
class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bidder = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    # ✅ ONLY ADD THIS
    is_paid = models.BooleanField(default=False)
class Notification(models.Model):

    user = models.ForeignKey(
        UserRegister,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    target_role = models.CharField(max_length=20)
    notification_type = models.CharField(max_length=50)

    def __str__(self):
        return self.title
class Order(models.Model):

    buyer = models.ForeignKey(
        UserRegister,
        on_delete=models.CASCADE,
        related_name='buyer_orders'
    )

    seller = models.ForeignKey(
        UserRegister,
        on_delete=models.CASCADE,
        related_name='seller_orders'
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, default='pending')
    payment_status = models.CharField(
        max_length=20,
        default='pending'
    )


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.amount}"
class Complaint(models.Model):

    user_id = models.IntegerField()

    user_type = models.CharField(max_length=20)

    subject = models.CharField(max_length=200)

    complaint = models.TextField()

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    admin_reply = models.TextField(
        blank=True,
        null=True
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )