steps = []

def do_action(name):
    steps.append(name)
    
WAREHOUSE_PHONE = '<phone number here e.g. +44712345678>'
SECRET_CODE = '<paste here>'

def handle_purchase():
    """
    Here are the actions you can trigger:
    
    calculate_price - Calculates total cost of the order
    check_inventory - Checks that the product is available in the warehouse
    finish_purchase - Ends the purchasing process
    inform_warehouse - Informs the warehouse team on the number above that an order has been made
    notify_customer - Notifies the purchaser that the order was successful
    start_purchase - Starts the purchasing process
    take_payment - Takes payment from the customer
    update_sales_tracker - Updates the sales tracker to log this successful purchase
    
    To trigger an action use, do_action and the label above, in quotes.
    
    """
    do_action('start_purchase')
    do_action('take_payment')
    do_action('finish_purchase')