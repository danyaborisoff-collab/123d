# fix_now.py
import os

print("🔧 Исправляю шаблоны...")

# Список файлов для исправления (ТОЛЬКО HTML!)
html_files = [
    "app/templates/app/blog_article_detail.html",
    "app/templates/app/blog_list.html",
    "app/templates/app/change_form.html",
    "app/templates/app/change_list.html",
    "app/templates/app/feedback_list.html",
    "app/templates/app/feedback.html",
    "app/templates/app/my_feedbacks.html"
]

for file_path in html_files:
    if os.path.exists(file_path):
        print(f"\n📄 Обрабатываю: {os.path.basename(file_path)}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Замены для blog
        if 'blog_article_detail' in file_path:
            old = "{% url 'admin:app_blogarticle_change' article.id %}"
            new = "/admin/app/blogarticle/{{ article.id }}/change/"
            if old in content:
                content = content.replace(old, new)
                print(f"  ✅ Заменил: {old}")
        
        if 'blog_list' in file_path:
            old = "{% url 'admin:app_blogarticle_changelist' %}"
            new = "/admin/app/blogarticle/"
            if old in content:
                content = content.replace(old, new)
                print(f"  ✅ Заменил: {old}")
        
        # Замены для feedback
        if 'change_form' in file_path or 'feedback' in file_path:
            old1 = "{% url 'admin:app_feedback_changelist' %}"
            new1 = "/admin/app/feedback/"
            old2 = "{% url 'admin:app_feedback_delete' original.id %}"
            new2 = "/admin/app/feedback/{{ original.id }}/delete/"
            
            if old1 in content:
                content = content.replace(old1, new1)
                print(f"  ✅ Заменил: {old1}")
            if old2 in content:
                content = content.replace(old2, new2)
                print(f"  ✅ Заменил: {old2}")
        
        # Общие замены
        old_admin = "{% url 'admin:index' %}"
        new_admin = "/admin/"
        if old_admin in content:
            content = content.replace(old_admin, new_admin)
            print(f"  ✅ Заменил админскую ссылку")
        
        # Сохраняем изменения
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  💾 Сохранен")
    else:
        print(f"\n⚠️ Не найден: {file_path}")

print("\n" + "="*50)
print("🎉 ВСЕ ШАБЛОНЫ ИСПРАВЛЕНЫ!")
print("Запустите сервер: env\\Scripts\\python.exe manage.py runserver")
print("Проверьте: http://127.0.0.1:8000/blog/")