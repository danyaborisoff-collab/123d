# models.py - ФИНАЛЬНАЯ ВЕРСИЯ
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Feedback(models.Model):
    """Модель отзыва"""
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    overall_rating = models.CharField(max_length=50, verbose_name="Общая оценка")
    liked_features = models.TextField(verbose_name="Что понравилось", blank=True)
    visit_frequency = models.CharField(max_length=50, verbose_name="Частота посещений")
    recommendation = models.IntegerField(verbose_name="Рекомендация (0-10)")
    suggestions = models.TextField(verbose_name="Предложения", blank=True)
    agree_to_terms = models.BooleanField(verbose_name="Согласие на обработку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"Отзыв от {self.name}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']


class Souvenir(models.Model):
    """Модель сувенира"""
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    def __str__(self):
        return f"{self.name} - {self.price} руб."
    
    class Meta:
        verbose_name = "Сувенир"
        verbose_name_plural = "Сувениры"


class BlogArticle(models.Model):
    """Модель статьи блога с изображением (Задание 3)"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_content = models.TextField(max_length=500, verbose_name="Краткое содержание")
    full_content = models.TextField(verbose_name="Полное содержание")
    
    # === НОВОЕ ПОЛЕ ДЛЯ ЗАДАНИЯ 3 ===
    image = models.ImageField(
        upload_to='blog_images/',
        verbose_name="Изображение статьи",
        blank=True,
        null=True,
        help_text="Загрузите изображение для статьи (рекомендуемый размер: 1200x600)"
    )
    
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return self.title
    
    def get_short_content(self):
        """Получить укороченное содержание для превью"""
        if len(self.full_content) > 150:
            return self.full_content[:147] + "..."
        return self.full_content
    
    def get_comments_count(self):
        """Получить количество комментариев"""
        return self.comments.filter(approved_comment=True).count()
    
    def get_comments(self):
        """Получить все комментарии к статье"""
        return self.comments.filter(approved_comment=True).order_by('-created_date')
    
    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
        ordering = ['-published_date']


class Comment(models.Model):
    """Модель комментария к статье блога"""
    post = models.ForeignKey(
        BlogArticle, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name="Статья"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        verbose_name="Автор"
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания"
    )
    approved_comment = models.BooleanField(
        default=True,
        verbose_name="Одобрен"
    )
    
    def __str__(self):
        return f'Комментарий от {self.author.username} к "{self.post.title[:20]}"'
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_date']


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    # Поле для изображения товара
    image = models.ImageField(
        upload_to='products/',
        verbose_name="Изображение товара",
        blank=True,
        null=True,
        help_text="Загрузите изображение товара"
    )
    
    category = models.CharField(
        max_length=100, 
        verbose_name="Категория",
        default="сувенир"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return f"{self.name} - {self.price} руб."
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['name']


class Cart(models.Model):
    """Модель корзины"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    def __str__(self):
        return f"Корзина пользователя {self.user.username}"
    
    def total_price(self):
        """Общая стоимость товаров в корзине"""
        total = 0
        for item in self.items.all():
            total += item.quantity * item.product.price
        return total
    
    def total_items(self):
        """Общее количество товаров в корзине"""
        return self.items.count()
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class CartItem(models.Model):
    """Модель товара в корзине"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    def item_price(self):
        """Цена за количество товаров"""
        return self.quantity * self.product.price
    
    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        unique_together = ['cart', 'product']


class UserProfile(models.Model):
    """Расширенная модель пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    address = models.TextField(blank=True, verbose_name="Адрес")
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")
    blocked_until = models.DateTimeField(null=True, blank=True, verbose_name="Заблокирован до")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    
    def __str__(self):
        return f"Профиль {self.user.username}"
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


# Сигнал для автоматического создания профиля пользователя при регистрации
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создает профиль при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Автоматически сохраняет профиль при сохранении пользователя"""
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)