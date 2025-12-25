# AvecPlaisirShop/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app.views import (
    home, about, contact, feedback, feedback_list,
    register, user_login, user_logout, my_feedbacks,
    delete_feedback, blog_list, blog_article_detail,
    create_article, edit_article, delete_article, delete_comment,
    video_page,
    catalog, create_product, edit_product, delete_product,
    view_cart, add_to_cart, remove_from_cart, update_cart_item, clear_cart
)

# Импортируем созданную админку блога
try:
    from app.blog_admin import blog_admin_site
    BLOG_ADMIN_AVAILABLE = True
except ImportError:
    print("⚠️ Файл blog_admin.py не найден. Создайте его в папке app/")
    BLOG_ADMIN_AVAILABLE = False

urlpatterns = [
    path('admin/', admin.site.urls),  # Основная админка
]

# Добавляем админку блога только если она доступна
if BLOG_ADMIN_AVAILABLE:
    urlpatterns.append(path('blog-admin/', blog_admin_site.urls))

# Основные пути сайта
urlpatterns += [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('feedback/', feedback, name='feedback'),  
    path('feedback/all/', feedback_list, name='feedback_list'),
    path('feedback/delete/<int:feedback_id>/', delete_feedback, name='delete_feedback'),
    path('my-feedbacks/', my_feedbacks, name='my_feedbacks'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/article/<int:article_id>/', blog_article_detail, name='blog_article_detail'),
    path('blog/edit/<int:article_id>/', edit_article, name='edit_article'),
    path('blog/create/', create_article, name='create_article'),
    path('blog/delete/<int:article_id>/', delete_article, name='delete_article'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('blog/comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    # Страница с видео
    path('video/', video_page, name='video_page'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/add/', create_product, name='create_product'),  # для админов
    path('catalog/edit/<int:product_id>/', edit_product, name='edit_product'),
    path('catalog/delete/<int:product_id>/', delete_product, name='delete_product'),
    
    # Корзина
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/clear/', clear_cart, name='clear_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)