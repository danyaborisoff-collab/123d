# fix_all_templates.py
import os
import re

print("🔧 Исправляю все шаблоны...")

# Список шаблонов для проверки
templates = [
    "app/templates/app/blog_list.html",
    "app/templates/app/blog_article_detail.html",
    "app/templates/app/feedback_list.html",
    "app/templates/app/feedback.html",
    "app/templates/app/my_feedbacks.html"
]

for template_path in templates:
    if os.path.exists(template_path):
        print(f"\n📄 Обрабатываю: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем ВСЕ админские URL на прямые пути
        replacements = [
            # Статьи блога
            (r"\{%\s*url\s+'admin:app_blogarticle_change'\s+article.id\s*%\}", 
             "/admin/app/blogarticle/{{ article.id }}/change/"),
            
            (r"\{%\s*url\s+'admin:app_blogarticle_changelist'\s*%\}", 
             "/admin/app/blogarticle/"),
            
            # Отзывы
            (r"\{%\s*url\s+'admin:app_feedback_change'\s+.*%\}", 
             "/admin/app/feedback/{{ feedback.id }}/change/"),
            
            (r"\{%\s*url\s+'admin:app_feedback_changelist'\s*%\}", 
             "/admin/app/feedback/"),
            
            (r"\{%\s*url\s+'admin:app_feedback_delete'\s+.*%\}", 
             "/admin/app/feedback/{{ feedback.id }}/delete/"),
            
            # Общие админские ссылки
            (r"\{%\s*url\s+'admin:index'\s*%\}", 
             "/admin/"),
        ]
        
        changes_made = False
        for pattern, replacement in replacements:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                print(f"  ✅ Заменил: {pattern[:50]}... -> {replacement}")
                changes_made = True
        
        if changes_made:
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  💾 Сохранено")
        else:
            print("  ✓ Проблемных ссылок не найдено")
    else:
        print(f"\n⚠️ Файл не найден: {template_path}")

print("\n" + "="*50)
print("🎉 ВСЕ ШАБЛОНЫ ИСПРАВЛЕНЫ!")
print("Перезапустите сервер командой:")
print("env\\Scripts\\python.exe manage.py runserver")