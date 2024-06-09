from django.db import models
from .utils import *
from .nepali_months import *
import nepali_datetime
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from django.forms import modelformset_factory
from django.template.loader import render_to_string
import io
from reportlab.lib.pagesizes import A4
import pdfkit
from django.conf import settings
from django.core.mail import EmailMessage,send_mail


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Bill(models.Model):
    invoice_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=13)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='invoices/', null=True, blank=True)
  

    def save(self, *args, **kwargs):
        if not self.pk:
            self.invoice_number = generate_invoice_number()
        super().save(*args, **kwargs)
        

    def generate_pdf(self):
        html_string = render_to_string('invoice_pdf.html', {'mybill': self, 'bill_items': self.billitem_set.all()})
        config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_CMD)
        pdf_file = pdfkit.from_string(html_string, False, configuration=config, options=settings.PDFKIT_OPTIONS)
        pdf_name = f"invoice_{self.invoice_number}.pdf"
        self.pdf.save(pdf_name, ContentFile(pdf_file), save=False)

    def send_email_with_pdf(self):
        if not self.pdf:
            self.generate_pdf()

        subject = f"Invoice {self.invoice_number}"
        message = f"Dear {self.customer.name},\n\nPlease find attached your invoice.\n\nThank you!"
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [self.customer.email])

        if self.pdf:
            self.pdf.open()
            email.attach(self.pdf.name, self.pdf.read(), 'application/pdf')
            self.pdf.close()

        email.send()

    
    def time_stamp(self):
        nep_date = nepali_datetime.date.today()
        nepali_day = nep_date.day
        nepali_year = nep_date.year
        nepali_month = NEPALI_MONTHS[nep_date.month]
        return f"{nepali_month} {nepali_day}, {nepali_year}"

    def subtotal(self):
        return sum(item.subtotal() for item in self.billitem_set.all())

    def total_price(self):
        subtotal = self.subtotal()
        vat_amount = subtotal * (self.vat / 100)
        total = subtotal + vat_amount
        if self.shipping_cost:
            total += self.shipping_cost
        return total

    def get_paid_status(self):
        return "Paid" if self.paid else "Unpaid"

    def __str__(self):
        return f"{self.customer.name}'s Bill"

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    



    def subtotal(self):
        return self.purchase_price * self.quantity

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.product.quantity_available >= self.quantity:
                self.purchase_price = self.product.price
                self.product.quantity_available -= self.quantity
                self.product.save()
            else:
                raise ValueError("Not enough quantity available for this product")
        super().save(*args, **kwargs)
