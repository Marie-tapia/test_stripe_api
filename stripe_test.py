import stripe

stripe.api_key = 'sk_live_test'

import datetime

def find_customer_by_email(email):

    customers = stripe.Customer.list(email=email).data
    if customers:
        return customers[0]
    return None

def get_subscription_info(customer):

    subscriptions = stripe.Subscription.list(customer=customer.id).data
    subscription_list = []
    for subscription in subscriptions:
        product = stripe.Product.retrieve(subscription.plan.product) if subscription.plan and subscription.plan.product else None
        product_name = product.name if product else 'Unknown Product'
        subscription_info = {
            'status': subscription.status,
            'current_period_end': datetime.datetime.fromtimestamp(subscription.current_period_end).strftime('%Y-%m-%d %H:%M:%S'),
            'start_date': datetime.datetime.fromtimestamp(subscription.start_date).strftime('%Y-%m-%d %H:%M:%S'),
            'product': product_name
        }
        subscription_list.append(subscription_info)
    return subscription_list

def display_customer_info(customer, subscriptions):
    print(f"Email: {customer.email}")
    print(f"Customer Since: {datetime.datetime.fromtimestamp(customer.created).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Purchased Products:")
    for idx, subscription in enumerate(subscriptions, start=1):
        print(f"  {idx}. Product: {subscription['product']}")
        print(f"     Status: {subscription['status']}")
        print(f"     Next Billing Date: {subscription['current_period_end']}")
        print(f"     Start Date: {subscription['start_date']}")

if __name__ == "__main__":
    email = 'customer@example.com'  # Adresse email à remplacer
    customer = find_customer_by_email(email)
    if customer:
        subscriptions = get_subscription_info(customer)
        display_customer_info(customer, subscriptions)
    else:
        print("No customer found with that email")
