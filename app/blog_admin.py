# app/blog_admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import messages
from .models import BlogArticle, Comment

class BlogArticleAdmin(admin.ModelAdmin):
    """Отдельная админ-панель только для статей блога"""
    list_display = ['id', 'title', 'short_content_preview', 'published_date', 'created_at', 'view_on_site_link']
    list_display_links = ['id', 'title']
    list_filter = ['published_date', 'created_at']
    search_fields = ['title', 'short_content', 'full_content']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'published_date'
    
    # actions должен быть списком строк (названий методов)
    actions = ['publish_selected_articles']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'short_content', 'full_content', 'image')
        }),
        ('Даты', {
            'fields': ('published_date', ('created_at', 'updated_at'))
        }),
    )
    
    def short_content_preview(self, obj):
        if obj.short_content:
            return obj.short_content[:100] + "..." if len(obj.short_content) > 100 else obj.short_content
        return "Без описания"
    short_content_preview.short_description = "Краткое содержание"
    
    def view_on_site_link(self, obj):
        if obj.id:
            url = reverse('blog_article_detail', args=[obj.id])
            return format_html(
                '<a href="{}" target="_blank" style="background-color: #8B0000; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;">📖 Читать на сайте</a>', 
                url
            )
        return "-"
    view_on_site_link.short_description = 'На сайт'
    
    # Метод для публикации статей
    def publish_selected_articles(self, request, queryset):
        count = queryset.update(published_date=timezone.now())
        self.message_user(request, f'✅ Опубликовано {count} статей.', messages.SUCCESS)
    publish_selected_articles.short_description = "📅 Опубликовать выбранные статьи"


class CommentAdmin(admin.ModelAdmin):
    """Админ-панель для комментариев"""
    list_display = ['id', 'author', 'post_title', 'text_preview', 'created_date', 'approved_comment', 'admin_actions']
    list_display_links = ['id', 'author']
    list_filter = ['approved_comment', 'created_date', 'author']
    search_fields = ['text', 'author__username', 'post__title']
    list_per_page = 20
    
    # actions должен быть списком строк
    actions = ['approve_comments', 'disapprove_comments']
    
    def post_title(self, obj):
        return obj.post.title[:50] + "..." if len(obj.post.title) > 50 else obj.post.title
    post_title.short_description = "Статья"
    
    def text_preview(self, obj):
        return obj.text[:100] + "..." if len(obj.text) > 100 else obj.text
    text_preview.short_description = "Текст комментария"
    
    def admin_actions(self, obj):
        return format_html(
            '<div style="display: flex; gap: 5px;">'
            '<a href="/blog-admin/app/comment/{}/change/" class="btn btn-xs btn-primary">✏️</a>'
            '<a href="/blog-admin/app/comment/{}/delete/" class="btn btn-xs btn-danger">🗑️</a>'
            '</div>',
            obj.id, obj.id
        )
    admin_actions.short_description = "Действия"
    
    # Методы для действий с комментариями
    def approve_comments(self, request, queryset):
        count = queryset.update(approved_comment=True)
        self.message_user(request, f'✅ Одобрено {count} комментариев.', messages.SUCCESS)
    approve_comments.short_description = "✅ Одобрить выбранные комментарии"
    
    def disapprove_comments(self, request, queryset):
        count = queryset.update(approved_comment=False)
        self.message_user(request, f'🚫 Скрыто {count} комментариев.', messages.WARNING)
    disapprove_comments.short_description = "🚫 Скрыть выбранные комментарии"


# Создаем отдельный админ-сайт для блога
blog_admin_site = admin.AdminSite(name='blogadmin')
blog_admin_site.register(BlogArticle, BlogArticleAdmin)
blog_admin_site.register(Comment, CommentAdmin)

# Настройки для этой админки
blog_admin_site.site_header = "📰 Управление блогом - Avec Plaisir"
blog_admin_site.site_title = "Администрирование блога и комментариев"
blog_admin_site.index_title = "Панель управления контентом блога"