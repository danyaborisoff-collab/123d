from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import Comment, BlogArticle, Product, CartItem  # ← ВСЕ МОДЕЛИ ЗДЕСЬ

class FeedbackForm(forms.Form):
    # Поля ввода
    name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        }),
        validators=[
            MinLengthValidator(2, 'Имя должно содержать минимум 2 символа'),
            MaxLengthValidator(100, 'Имя слишком длинное')
        ]
    )
    
    email = forms.EmailField(
        label='Email адрес',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.ru'
        })
    )
    
    # Радиокнопки - общая оценка сайта
    RATING_CHOICES = [
        ('5', 'Отлично ⭐⭐⭐⭐⭐'),
        ('4', 'Хорошо ⭐⭐⭐⭐'),
        ('3', 'Удовлетворительно ⭐⭐⭐'),
        ('2', 'Плохо ⭐⭐'),
        ('1', 'Очень плохо ⭐'),
    ]
    
    overall_rating = forms.ChoiceField(
        label='Общая оценка сайта',
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'rating-radio'
        })
    )
    
    # Флажки - что понравилось
    LIKED_FEATURES = [
        ('design', 'Дизайн сайта'),
        ('navigation', 'Удобная навигация'),
        ('products', 'Ассортимент товаров'),
        ('prices', 'Цены'),
        ('delivery', 'Условия доставки'),
        ('support', 'Работа поддержки'),
    ]
    
    liked_features = forms.MultipleChoiceField(
        label='Что вам понравилось на сайте? (можно выбрать несколько)',
        choices=LIKED_FEATURES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'feature-checkbox'
        }),
        required=False
    )
    
    # Выпадающий список - частота посещений
    VISIT_FREQUENCY = [
        ('first', 'Впервые на сайте'),
        ('rarely', 'Редко (раз в несколько месяцев)'),
        ('monthly', 'Регулярно (раз в месяц)'),
        ('weekly', 'Часто (раз в неделю)'),
        ('daily', 'Очень часто (почти каждый день)'),
    ]
    
    visit_frequency = forms.ChoiceField(
        label='Как часто вы посещаете наш сайт?',
        choices=VISIT_FREQUENCY,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Слайдер/числовое поле - вероятность рекомендации
    recommendation = forms.IntegerField(
        label='Насколько вероятно, что вы порекомендуете наш сайт друзьям? (0-10)',
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'range',
            'min': '0',
            'max': '10',
            'step': '1'
        }),
        initial=5
    )
    
    # Большое текстовое поле - пожелания
    suggestions = forms.CharField(
        label='Ваши предложения по улучшению сайта',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Напишите ваши предложения, замечания или пожелания...'
        }),
        required=False,
        validators=[
            MaxLengthValidator(1000, 'Сообщение не должно превышать 1000 символов')
        ]
    )
    
    # Согласие на обработку данных
    agree_to_terms = forms.BooleanField(
        label='Я согласен на обработку моих персональных данных',
        required=True,
        error_messages={'required': 'Необходимо согласие на обработку данных'}
    )


class CommentForm(forms.ModelForm):
    """Форма для добавления комментариев к статьям"""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите ваш комментарий...',
                'style': 'background-color: #222; color: white; border: 1px solid #444;'
            })
        }
        labels = {
            'text': 'Текст комментария'
        }


class BlogArticleForm(forms.ModelForm):
    """Форма для создания/редактирования статей с изображением"""
    class Meta:
        model = BlogArticle
        fields = ['title', 'short_content', 'full_content', 'image', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок статьи'
            }),
            'short_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Краткое содержание (максимум 500 символов)'
            }),
            'full_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Полный текст статьи'
            }),
            'published_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'title': 'Заголовок статьи',
            'short_content': 'Краткое содержание',
            'full_content': 'Полный текст',
            'image': 'Изображение статьи',
            'published_date': 'Дата публикации'
        }


class ProductForm(forms.ModelForm):
    """Форма для товаров"""
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание товара'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена',
                'min': '0',
                'step': '0.01'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Категория'
            }),
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'price': 'Цена (руб.)',
            'image': 'Изображение',
            'category': 'Категория'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем описание необязательным
        self.fields['description'].required = False
        self.fields['image'].required = False


class AddToCartForm(forms.Form):
    """Форма для добавления в корзину"""
    quantity = forms.IntegerField(
        min_value=1,
        max_value=99,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 80px;'
        }),
        label='Количество'
    )


class CartItemUpdateForm(forms.ModelForm):
    """Форма для обновления количества товара в корзине"""
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '99',
                'style': 'width: 80px;'
            })
        }


class CheckoutForm(forms.Form):
    """Форма для оформления заказа"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя получателя'
        }),
        label='Имя'
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67'
        }),
        label='Телефон'
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Адрес доставки'
        }),
        label='Адрес доставки'
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Комментарий к заказу (необязательно)'
        }),
        label='Комментарий'
    )