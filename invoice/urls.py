from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('create_bill/', views.create_bill, name='create_bill'),
    path('create_bill/create_customer/', views.create_customer, name='create_customer'),
    path('bill_list/bill_update/<int:id>/', views.bill_update, name='bill_update'),

    path('bill_list/<int:bill_id>/download/', views.download_bill_pdf, name='download_bill_pdf'),
    path('bill_list/<int:bill_id>/view_pdf/', views.view_pdf, name='view_pdf'),

    path('bill_list/bill_delete/<int:id>/', views.bill_delete, name='bill_delete'),

    path('bill_list/', views.bill_list, name='bill_list'),
    path('bill_list/<int:bill_id>/send_email/', views.send_bill_email, name='send_bill_email'),

    path('export/bills/csv/', views.export_bills_csv, name='export_bills_csv'),
    path('export/bills/excel/', views.export_bills_excel, name='export_bills_excel'),
    
    
    path('product_list/', views.product_list, name='product_list'),
    path('category_list/', views.category_list, name='category_list'),
    path('category_list/category_delete/<int:id>/', views.category_delete, name='category_delete'),
    path('product_list/product_delete/<int:id>/', views.product_delete, name='product_delete'),
    path('product_list/product_update/<int:id>/', views.product_update, name='product_update'),

    path('create_customer/', views.create_customer, name='create_customer'),
    path('create_customer/customer_delete/<int:id>/', views.customer_delete, name='customer_delete'),
    path('create_customer/customer_update/<int:id>/', views.customer_update, name='customer_update'),


    path('bill_list/details/<int:id>/', views.details, name='details'),








    
]

