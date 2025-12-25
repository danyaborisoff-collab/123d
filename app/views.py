# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Avg
from django.utils import timezone

# === ИМПОРТ ФОРМ (ОДИН РАЗ!) ===
from .forms import FeedbackForm, CommentForm, BlogArticleForm, ProductForm 

# === ИМПОРТ МОДЕЛЕЙ (ОДИН РАЗ!) ===
from .models import Feedback, BlogArticle, Comment, Product, Cart, CartItem 

def home(request):
    return render(request, 'app/index.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('home')

@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            liked_features = ', '.join(form.cleaned_data['liked_features'])
            feedback_obj = Feedback.objects.create(
                name=form.cleaned_data['name'],
                email=request.user.email,
                overall_rating=form.cleaned_data['overall_rating'],
                liked_features=liked_features,
                visit_frequency=form.cleaned_data['visit_frequency'],
                recommendation=form.cleaned_data['recommendation'],
                suggestions=form.cleaned_data['suggestions'] or '',
                agree_to_terms=form.cleaned_data['agree_to_terms']
            )
            messages.success(request, 'Спасибо за ваш отзыв!')
            return render(request, 'app/feedback_thanks.html', {'feedback': feedback_obj})
    else:
        form = FeedbackForm(initial={
            'name': request.user.username,
            'email': request.user.email,
        })
    return render(request, 'app/feedback.html', {'form': form})

def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    total_feedbacks = feedbacks.count()
    if total_feedbacks > 0:
        avg_result = feedbacks.aggregate(Avg('recommendation'))
        avg_recommendation = round(avg_result['recommendation__avg'], 1)
    else:
        avg_recommendation = 0
    return render(request, 'app/feedback_list.html', {
        'feedbacks': feedbacks,
        'total_feedbacks': total_feedbacks,
        'avg_recommendation': avg_recommendation,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    })

@login_required
def my_feedbacks(request):
    user_feedbacks = Feedback.objects.filter(
        email=request.user.email
    ).order_by('-created_at')
    return render(request, 'app/my_feedbacks.html', {
        'feedbacks': user_feedbacks,
        'total_feedbacks': user_feedbacks.count()
    })

@login_required
def delete_feedback(request, feedback_id):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'У вас нет прав для удаления отзывов.')
        return redirect('feedback_list')
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Отзыв был успешно удален.')
        return redirect('feedback_list')
    return render(request, 'app/delete_feedback_confirm.html', {
        'feedback': feedback
    })

def blog_list(request):
    articles = BlogArticle.objects.all().order_by('-published_date')
    return render(request, 'app/blog_list.html', {
        'articles': articles,
        'show_create_button': request.user.is_staff or request.user.is_superuser
    })

def blog_article_detail(request, article_id):
    article = get_object_or_404(BlogArticle, id=article_id)
    comments = article.comments.filter(approved_comment=True).order_by('-created_date')
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text', '').strip()
        if text and len(text) >= 3:
            Comment.objects.create(
                post=article,
                author=request.user,
                text=text,
                approved_comment=True
            )
            messages.success(request, '✅ Ваш комментарий успешно добавлен!')
            return redirect('blog_article_detail', article_id=article_id)
        else:
            messages.error(request, '❌ Комментарий должен содержать минимум 3 символа')
    return render(request, 'app/blog_article_detail.html', {
        'article': article,
        'comments': comments,
        'user_can_comment': request.user.is_authenticated,
        'show_edit_button': request.user.is_staff or request.user.is_superuser
    })

# ========== КАТАЛОГ ТОВАРОВ ==========
def catalog(request):
    """Каталог товаров"""
    products = Product.objects.all().order_by('name')
    return render(request, 'app/catalog.html', {
        'products': products,
        'title': 'Каталог товаров'
    })


@login_required
def add_to_cart(request, product_id):
    """Добавить товар в корзину"""
    product = get_object_or_404(Product, id=product_id)
    
    # Получаем или создаем корзину пользователя
    cart, created = Cart.objects.get_or_create(
        user=request.user,
        is_active=True
    )
    
    # Проверяем, есть ли уже этот товар в корзине
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not item_created:
        # Если товар уже в корзине, увеличиваем количество
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество товара "{product.name}" увеличено в корзине')
    else:
        messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    
    return redirect('catalog')


@login_required
def remove_from_cart(request, item_id):
    """Удалить товар из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Товар "{product_name}" удален из корзины')
    return redirect('view_cart')


@login_required
def update_cart_item(request, item_id):
    """Обновить количество товара в корзине"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f'Количество товара "{cart_item.product.name}" обновлено')
        else:
            cart_item.delete()
            messages.success(request, f'Товар "{cart_item.product.name}" удален из корзины')
    
    return redirect('view_cart')


@login_required
def view_cart(request):
    """Просмотр корзины"""
    # ИСПРАВЛЕНО: правильно используем get_or_create
    cart, created = Cart.objects.get_or_create(
        user=request.user,
        is_active=True
    )
    
    cart_items = cart.items.all().select_related('product')
    
    return render(request, 'app/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.total_price(),
        'title': 'Моя корзина'
    })


@login_required
def clear_cart(request):
    """Очистить корзину"""
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    count = cart.items.count()
    cart.items.all().delete()
    messages.success(request, f'Корзина очищена ({count} товаров удалено)')
    return redirect('view_cart')


# Админские функции для товаров
@login_required
def create_product(request):
    """Создание товара (только для администраторов)"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'У вас нет прав для создания товаров.')
        return redirect('catalog')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'✅ Товар "{product.name}" успешно создан!')
            return redirect('catalog')
    else:
        form = ProductForm()
    
    return render(request, 'app/create_product.html', {
        'form': form,
        'title': 'Добавление нового товара'
    })


@login_required
def edit_product(request, product_id):
    """Редактирование товара (только для администраторов)"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'У вас нет прав для редактирования товаров.')
        return redirect('catalog')
    
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Товар "{product.name}" успешно обновлен!')
            return redirect('catalog')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'app/create_product.html', {
        'form': form,
        'product': product,
        'title': f'Редактирование товара: {product.name}'
    })


@login_required
def delete_product(request, product_id):
    """Удаление товара (только для администраторов)"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'У вас нет прав для удаления товаров.')
        return redirect('catalog')
    
    product = get_object_or_404(Product, id=product_id)
    product_name = product.name
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, f'🗑️ Товар "{product_name}" успешно удален.')
        return redirect('catalog')
    
    return render(request, 'app/delete_product_confirm.html', {
        'product': product
    })


# Функция для проверки количества товаров в корзине (для шаблона)
def get_cart_items_count(request):
    """Получить количество товаров в корзине"""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, is_active=True)
            return cart.items.count()
        except Cart.DoesNotExist:
            return 0
    return 0


@login_required
def create_article(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'У вас нет прав для создания статей.')
        return redirect('blog_list')
    if request.method == 'POST':
        form = BlogArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'✅ Статья "{article.title}" успешно создана!')
            return redirect('blog_list')
    else:
        form = BlogArticleForm(initial={
            'published_date': timezone.now()
        })
    return render(request, 'app/create_article.html', {
        'form': form,
        'title': 'Создание новой статьи'
    })

@login_required
def edit_article(request, article_id):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'У вас нет прав для редактирования статей.')
        return redirect('blog_list')
    article = get_object_or_404(BlogArticle, id=article_id)
    if request.method == 'POST':
        form = BlogArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Статья "{article.title}" успешно обновлена!')
            return redirect('blog_article_detail', article_id=article.id)
    else:
        form = BlogArticleForm(instance=article)
        if article.published_date:
            form.initial['published_date'] = article.published_date.strftime('%Y-%m-%dT%H:%M')
    return render(request, 'app/create_article.html', {
        'form': form,
        'article': article,
        'title': f'Редактирование статьи: {article.title}'
    })

@login_required
def delete_article(request, article_id):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'У вас нет прав для удаления статей.')
        return redirect('blog_list')
    article = get_object_or_404(BlogArticle, id=article_id)
    article_title = article.title
    if request.method == 'POST':
        article.delete()
        messages.success(request, f'🗑️ Статья "{article_title}" успешно удалена.')
        return redirect('blog_list')
    return render(request, 'app/delete_article_confirm.html', {
        'article': article
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    article_id = comment.post.id
    if not (request.user.is_staff or request.user.is_superuser or request.user == comment.author):
        messages.error(request, 'У вас нет прав для удаления этого комментария.')
        return redirect('blog_article_detail', article_id=article_id)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, '🗑️ Комментарий успешно удален.')
        return redirect('blog_article_detail', article_id=article_id)
    return render(request, 'app/delete_comment_confirm.html', {
        'comment': comment
    })

def video_page(request):
    return render(request, 'app/video.html')