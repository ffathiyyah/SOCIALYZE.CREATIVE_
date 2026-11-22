
import bleach

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.utils import timezone

from .models import (
    UserProfile,
    Service,
    Article,
    ArticleCategory,
)

User = get_user_model()


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nama Pengguna',
        widget=forms.TextInput(attrs={
            'placeholder': 'Masukkan nama pengguna'
        })
    )

    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Masukkan email'
        })
    )

    password1 = forms.CharField(
        required=True,
        label='Kata Sandi',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Masukkan kata sandi'
        })
    )

    password2 = forms.CharField(
        required=True,
        label='Konfirmasi Kata Sandi',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Konfirmasi kata sandi'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email sudah digunakan.')

        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Nama depan',
            'last_name': 'Nama belakang',
            'email': 'Email'
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone',)
        labels = {
            'phone': 'Nomor telepon / WhatsApp'
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'name',
            'category_label',
            'icon',
            'description',
            'is_active',
            'display_order',
        ]

        labels = {
            'name': 'Nama layanan',
            'category_label': 'Kategori layanan',
            'icon': 'Ikon layanan',
            'description': 'Deskripsi layanan',
            'is_active': 'Tampilkan layanan',
            'display_order': 'Urutan tampilan',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Contoh: Branding & Visual Identity'
            }),
            'category_label': forms.TextInput(attrs={
                'placeholder': 'Contoh: 01 / BRAND'
            }),
            'icon': forms.TextInput(attrs={
                'placeholder': 'Contoh: ✳'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Masukkan deskripsi layanan'
            }),
            'display_order': forms.NumberInput(attrs={
                'min': 0
            }),
        }


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article

        fields = [
            'title',
            'excerpt',
            'body',
            'uploaded_image',
            'category',
            'author',
            'published_at',
            'status',
        ]

        labels = {
            'title': 'Judul artikel',
            'excerpt': 'Ringkasan artikel',
            'body': 'Isi artikel',
            'uploaded_image': 'Thumbnail artikel',
            'category': 'Kategori artikel',
            'author': 'Nama penulis',
            'published_at': 'Tanggal publikasi',
            'status': 'Status artikel',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Masukkan judul artikel'
            }),

            'excerpt': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tuliskan ringkasan singkat artikel'
            }),

            'body': forms.Textarea(attrs={
                'rows': 15,
                'placeholder': 'Tuliskan isi lengkap artikel di sini...',
                'class': 'article-editor'
            }),

            'uploaded_image': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            }),

            'category': forms.Select(),

            'author': forms.TextInput(attrs={
                'placeholder': 'Contoh: Socialyze Team'
            }),

            'published_at': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local'
                }
            ),

            'status': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = ArticleCategory.objects.all()
        self.fields['category'].empty_label = 'Pilih kategori'

        self.fields['uploaded_image'].required = False

        self.fields['published_at'].required = False
        self.fields['published_at'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]

        self.fields['author'].initial = (
            self.instance.author
            if self.instance and self.instance.pk
            else 'Socialyze Team'
        )

    def clean_title(self):
        title = self.cleaned_data['title'].strip()

        if not title:
            raise forms.ValidationError(
                'Judul artikel wajib diisi.'
            )

        return title

    # Membersihkan HTML pada isi artikel.
    def clean_body(self):
        body = self.cleaned_data.get('body', '')

        allowed_tags = [
            'p', 'br',
            'h2', 'h3', 'h4',
            'strong', 'b',
            'em', 'i',
            'u',
            'ul', 'ol', 'li',
            'blockquote',
            'a',
        ]

        allowed_attributes = {
            'a': ['href', 'title', 'target', 'rel'],
        }

        return bleach.clean(
            body,
            tags=allowed_tags,
            attributes=allowed_attributes,
            protocols=['http', 'https', 'mailto'],
            strip=True
        )

    def clean_uploaded_image(self):
        image = self.cleaned_data.get('uploaded_image')

        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                'Ukuran gambar maksimal 5 MB.'
            )

        return image

    def save(self, commit=True):
        article = super().save(commit=False)

        # Membuat slug otomatis berdasarkan judul.
        base_slug = slugify(article.title) or 'artikel'
        slug = base_slug
        counter = 1

        while Article.objects.filter(slug=slug).exclude(
            pk=article.pk
        ).exists():
            counter += 1
            suffix = f'-{counter}'
            slug = f'{base_slug[:200-len(suffix)]}{suffix}'

        article.slug = slug

        now = timezone.now()

        if not article.pk:
            article.created_at = now

        article.updated_at = now

        if article.status == 'published' and not article.published_at:
            article.published_at = now

        if commit:
            article.save()
            self.save_m2m()

        return article
