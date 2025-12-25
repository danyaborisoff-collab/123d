# fix_blog_error.py
import os
import sys

# Путь к вашему проекту
project_path = r"C:\Users\tt\source\repos\AvecPlaisirShop\AvecPlaisirShop"
app_path = os.path.join(project_path, "app")

print("🛠️  Исправляю ошибку с блогом...")

# 1. Исправляем views.py
views_file = os.path.join(app_path, "views.py")
if os.path.exists(views_file):
    with open(views_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем неверный импорт
    content = content.replace("from .blog_models import BlogArticle", "from .models import Feedback, BlogArticle")
    content = content.replace("from .models import Feedback", "from .models import Feedback, BlogArticle")
    
    # Убедимся, что BlogArticle импортируется
    if "from .models import" in content and "BlogArticle" not in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "from .models import" in line and "Feedback" in line and "BlogArticle" not in line:
                lines[i] = line.replace("from .models import Feedback", "from .models import Feedback, BlogArticle")
                break
        content = '\n'.join(lines)
    
    with open(views_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ views.py исправлен")

# 2. Проверяем models.py
models_file = os.path.join(app_path, "models.py")
if os.path.exists(models_file):
    with open(models_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "class BlogArticle" not in content:
        print("❌ BlogArticle не найден в models.py")
        print("📝 Добавляю BlogArticle в models.py...")
        blog_article_code = '''
class BlogArticle(models.Model):
    """Модель статьи блога"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_content = models.TextField(max_length=500, verbose_name="Краткое содержание")
    full_content = models.TextField(verbose_name="Полное содержание")
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
    
    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
        ordering = ['-published_date']
'''
        
        # Находим место для вставки (перед UserProfile)
        if "class UserProfile" in content:
            content = content.replace("class UserProfile", blog_article_code + "\n\nclass UserProfile")
        else:
            # Вставляем в конец
            content += blog_article_code
        
        with open(models_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ BlogArticle добавлен в models.py")
    else:
        print("✅ BlogArticle уже есть в models.py")

# 3. Удаляем blog_models.py если он есть
blog_models_file = os.path.join(app_path, "blog_models.py")
if os.path.exists(blog_models_file):
    os.remove(blog_models_file)
    print("🗑️  Удален blog_models.py")

print("\n📋 ПРОВЕРКА:")
print("=" * 50)

# Проверяем imports
with open(views_file, 'r', encoding='utf-8') as f:
    content = f.read()
    if "from .models import" in content and "BlogArticle" in content:
        print("✅ views.py: правильный импорт BlogArticle")
    else:
        print("❌ views.py: НЕПРАВИЛЬНЫЙ импорт BlogArticle")

with open(models_file, 'r', encoding='utf-8') as f:
    content = f.read()
    if "class BlogArticle" in content:
        print("✅ models.py: BlogArticle существует")
    else:
        print("❌ models.py: BlogArticle НЕ существует")

print("=" * 50)
print("\n🚀 Запускаю миграции...")

# Запускаем Django для миграций
sys.path.append(project_path)
os.chdir(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AvecPlaisirShop.settings')

try:
    import django
    django.setup()
    
    from django.core.management import execute_from_command_line
    
    print("🔄 Создаю миграции...")
    execute_from_command_line(['manage.py', 'makemigrations', 'app'])
    
    print("📥 Применяю миграции...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ Миграции успешно применены!")
    
    # Проверяем таблицу
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='app_blogarticle'")
        table_exists = cursor.fetchone()
        if table_exists:
            print("✅ Таблица 'app_blogarticle' существует в базе данных")
        else:
            print("❌ Таблица 'app_blogarticle' НЕ существует")
            
except Exception as e:
    print(f"⚠️ Ошибка: {e}")

print("\n🎉 Исправление завершено!")
print("Запустите сервер: python manage.py runserver")
print("Проверьте блог: http://127.0.0.1:8000/blog/")