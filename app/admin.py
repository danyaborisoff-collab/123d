# app/admin.py
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Feedback, Souvenir, UserProfile, BlogArticle
from django.db import connection


class FeedbackAdmin(admin.ModelAdmin):
    """Админ-панель для отзывов"""
    list_display = ['id', 'name', 'email', 'overall_rating', 'recommendation', 'created_at']
    list_filter = ['overall_rating', 'visit_frequency', 'created_at']
    search_fields = ['name', 'email', 'suggestions']
    readonly_fields = ['created_at']
    
    def response_change(self, request, obj):
        if "_delete_feedback" in request.POST:
            if obj:
                name = obj.name
                obj.delete()
                self.message_user(request, f'✅ Отзыв от "{name}" успешно удален.', messages.SUCCESS)
                return HttpResponseRedirect(reverse('admin:app_feedback_changelist'))
        return super().response_change(request, obj)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_blocked', 'blocked_until', 'phone']
    list_filter = ['is_blocked']
    search_fields = ['user__username', 'user__email', 'phone']


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    actions = ['delete_selected_users']
    
    def delete_selected_users(self, request, queryset):
        queryset = queryset.filter(is_superuser=False)
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Удалено {count} пользователей.', messages.SUCCESS)
    delete_selected_users.short_description = "Удалить выбранных пользователей"


class SouvenirAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name', 'description']


class MainBlogArticleAdmin(admin.ModelAdmin):
    """Упрощенная версия для основной админки (опционально)"""
    list_display = ['title', 'published_date', 'created_at']
    list_filter = ['published_date']
    search_fields = ['title']


# Регистрируем модели в основной админке
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Souvenir, SouvenirAdmin)
admin.site.register(BlogArticle, MainBlogArticleAdmin)  # Упрощенная версия

# Перерегистрируем User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Проверка таблицы
def verify_models():
    try:
        print("🔍 Проверка моделей...")
        from .models import BlogArticle
        count = BlogArticle.objects.count()
        print(f"✅ Найдено статей в базе: {count}")
    except Exception as e:
        print(f"⚠️ Ошибка при проверке: {e}")

verify_models()

# Настройки основной админ-панели
admin.site.site_header = "Avec Plaisir - Панель управления"
admin.site.site_title = "Администрирование магазина"
admin.site.index_title = "Управление сайтом"