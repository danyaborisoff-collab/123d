import os
import django
import sys

# Настройка Django
sys.path.append(r'C:\Users\tt\source\repos\AvecPlaisirShop\AvecPlaisirShop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AvecPlaisirShop.settings')
django.setup()

from django.db import connection

# Создаем таблицу вручную
with connection.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "app_blogarticle" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "title" varchar(200) NOT NULL,
            "short_content" text NOT NULL,
            "full_content" text NOT NULL,
            "published_date" datetime NOT NULL,
            "created_at" datetime NOT NULL,
            "updated_at" datetime NOT NULL
        )
    """)
    print("✅ Таблица 'app_blogarticle' создана успешно!")