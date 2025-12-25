import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AvecPlaisirShop.settings')
django.setup()

from app.models import Product

def create_sample_products():
    """Создание тестовых товаров"""
    
    products = [
        {
            'name': 'Кружка Avec Plaisir',
            'description': 'Керамическая кружка с логотипом магазина. Объем 350 мл.',
            'price': 500,
            'category': 'сувениры'
        },
        {
            'name': 'Экосумка-шоппер',
            'description': 'Хлопковая экосумка с принтом. Размер 40x40 см.',
            'price': 1000,
            'category': 'аксессуары'
        },
        {
            'name': 'Стальная фляжка',
            'description': 'Нержавеющая стальная фляжка с гравировкой. Объем 250 мл.',
            'price': 2000,
            'category': 'сувениры'
        }
    ]
    
    created_count = 0
    for product_data in products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            created_count += 1
            print(f'✅ Создан товар: {product.name} - {product.price} руб.')
    
    print(f'\n🎉 Создано {created_count} товаров из {len(products)}')

if __name__ == '__main__':
    create_sample_products()