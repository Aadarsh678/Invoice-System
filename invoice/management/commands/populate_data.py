from django.core.management.base import BaseCommand
from faker import Faker
import random
from invoice.models import Customer, Category, Product, Bill, BillItem

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Predefined categories and products for realism
        category_product_mapping = {
            'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Camera'],
            'Books': ['Novel', 'Science Book', 'Biography', 'Cookbook'],
            'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sweater'],
            'Home & Kitchen': ['Blender', 'Microwave', 'Cookware Set', 'Vacuum Cleaner'],
            'Sports & Outdoors': ['Tent', 'Sleeping Bag', 'Yoga Mat', 'Bike'],
            'Toys & Games': ['Board Game', 'Doll', 'Action Figure', 'Puzzle'],
            'Health & Personal Care': ['Shampoo', 'Toothpaste', 'Vitamin', 'Lotion']
        }

        # Create Categories
        categories = []
        for category_name in category_product_mapping.keys():
            category = Category.objects.create(name=category_name)
            categories.append(category)

        # Create Customers
        customers = []
        for _ in range(50):
            customer = Customer.objects.create(
                name=fake.name(),
                email=fake.email(),
                address=fake.address(),
                phone_number=fake.phone_number()
            )
            customers.append(customer)

        # Create Products
        products = []
        for category in categories:
            for product_name in category_product_mapping[category.name]:
                product = Product.objects.create(
                    category=category,
                    name=product_name,
                    price=random.uniform(10.0, 1000.0),
                    quantity_available=random.randint(1, 100)
                )
                products.append(product)

        # Create Bills and BillItems
        # for _ in range(20):
        #     customer = random.choice(customers)
        #     bill = Bill.objects.create(
        #         customer=customer,
        #         vat=13.0,
        #         shipping_cost=random.uniform(5.0, 20.0),
        #         paid=random.choice([True, False])
        #     )

        #     # Create BillItems
        #     available_products = [product for product in products if product.quantity_available > 0]
        #     for _ in range(random.randint(1, 5)):
        #         if not available_products:
        #             break
        #         product = random.choice(available_products)
        #         quantity = random.randint(1, product.quantity_available)
        #         BillItem.objects.create(
        #             bill=bill,
        #             product=product,
        #             quantity=quantity,
        #             purchase_price=product.price
        #         )
        #         product.quantity_available -= quantity
        #         product.save()
        #         if product.quantity_available == 0:
        #             available_products.remove(product)

        # self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data'))
