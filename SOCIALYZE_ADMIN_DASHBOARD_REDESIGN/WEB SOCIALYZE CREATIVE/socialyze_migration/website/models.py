
import uuid
from django.db import models
from django.conf import settings




class Order(models.Model):
    STATUS_CHOICES = [
        ('Menunggu konfirmasi', 'Menunggu konfirmasi'),
        ('Sedang ditinjau', 'Sedang ditinjau'),
        ('Selesai', 'Selesai'),
        ('Dibatalkan', 'Dibatalkan'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Menunggu pembayaran'),
        ('SUCCESS', 'Berhasil'),
        ('FAILED', 'Gagal'),
        ('CANCELLED', 'Dibatalkan'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('VIRTUAL_ACCOUNT', 'Virtual Account'),
        ('E_WALLET', 'E-Wallet'),
        ('QRIS', 'QRIS'),
    ]

    reference = models.CharField(
        max_length=20, unique=True, editable=False, db_index=True
    )
    customer_token = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False
    )

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    notes = models.TextField(blank=True)

    payment_method = models.CharField(
        max_length=80,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        default=''
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )
    paid_at = models.DateTimeField(blank=True, null=True)

    items = models.JSONField(default=list)
    total = models.PositiveBigIntegerField(default=0)

    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default='Menunggu konfirmasi'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = 'SOC-' + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.reference} — {self.name}'



class Consultation(models.Model):
    STATUS_CHOICES = [
        ('Menunggu ditinjau', 'Menunggu ditinjau'),
        ('Sedang ditindaklanjuti', 'Sedang ditindaklanjuti'),
        ('Selesai', 'Selesai')
    ]

    reference = models.CharField(max_length=20, unique=True, editable=False, db_index=True)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    service = models.CharField(max_length=120)
    budget = models.CharField(max_length=100)
    brief = models.TextField()
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='Menunggu ditinjau')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = 'CON-' + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.reference} — {self.name}'


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=40, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profil {self.user.username}'


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'website_articlecategory'

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.CharField(max_length=300)
    body = models.TextField()

    # Gambar eksternal yang sudah digunakan sebelumnya.
    image = models.CharField(max_length=100, blank=True, null=True)

    # Thumbnail yang diunggah langsung dari dashboard.
    uploaded_image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True
    )

    # Link sumber artikel eksternal tetap dipertahankan.
    source_url = models.URLField(max_length=1000, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='published'
    )

    author = models.CharField(
        max_length=150,
        blank=True,
        default='Socialyze Team'
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='articles'
    )

    class Meta:
        db_table = 'website_article'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField(max_length=150)
    category_label = models.CharField(
        max_length=100,
        help_text='Contoh: 01 / BRAND'
    )
    icon = models.CharField(
        max_length=30,
        blank=True,
        default='✳'
    )
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'website_service'
        ordering = ['display_order', 'id']
        verbose_name = 'Layanan'
        verbose_name_plural = 'Layanan'

    def __str__(self):
        return self.name
