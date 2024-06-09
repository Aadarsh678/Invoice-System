import nepali_datetime

def get_nepali_fiscal_year(nepali_date):
    # Nepali fiscal year starts on 1st Shrawan (typically July 16th )
    fiscal_start_month = 4  # Shrawan
    fiscal_start_day = 1    # 1st Shrawan
    
    # Extract the Bikram Sambat year, month, and day from the Nepali date
    year = nepali_date.year
    month = nepali_date.month
    day = nepali_date.day
    
    # Determine the fiscal year based on the current Nepali date
    if (month > fiscal_start_month) or (month == fiscal_start_month and day >= fiscal_start_day):
        fiscal_year_start = year
        fiscal_year_end = year + 1
    else:
        fiscal_year_start = year - 1
        fiscal_year_end = year

    return fiscal_year_start, fiscal_year_end

def generate_invoice_number():
    from .models import Bill  

    # Get the current Nepali date
    current_nepali_date = nepali_datetime.date.today()

    # Get the current fiscal year
    fiscal_year_start, fiscal_year_end = get_nepali_fiscal_year(current_nepali_date)

    # Create the fiscal year format as YYYYYY (e.g., 208081 for fiscal year 2080/81)
    fiscal_year_format = f"{fiscal_year_start}{str(fiscal_year_end)[-2:]}"

    # Get the last invoice number for the current fiscal year
    last_invoice = Bill.objects.filter(invoice_number__startswith=f"INV{fiscal_year_format}").order_by('-invoice_number').first()

    if last_invoice:
        last_invoice_number = int(last_invoice.invoice_number[-4:])  # Extract the sequential number part
        new_invoice_number = last_invoice_number + 1
    else:
        new_invoice_number = 1

    # Format the invoice number
    invoice_number = f"INV{fiscal_year_format}{new_invoice_number:04}"

    return invoice_number
