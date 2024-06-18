from django.shortcuts import render
import stripe
import datetime
from django.http import JsonResponse
from django.views import View
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY

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

class CustomerInfoView(View):
    def get(self, request, email):
        customer = find_customer_by_email(email)
        if customer:
            subscriptions = get_subscription_info(customer)
            stripe_data = {
                'email': customer.email,
                'customer_since': datetime.datetime.fromtimestamp(customer.created).strftime('%Y-%m-%d %H:%M:%S'),
                'purchased_products': subscriptions
            }
            return JsonResponse(stripe_data)
        else:
            return JsonResponse({'error': 'No customer found with that email'}, status=404)

class CustomerEmailView(View):
    def get(self, request, email):
        customer = find_customer_by_email(email)
        if customer:
            return JsonResponse({'email': customer.email})
        else:
            return JsonResponse({'error': 'No customer found with that email'}, status=404)

class CustomerProductsView(View):
    def get(self, request, email):
        customer = find_customer_by_email(email)
        if customer:
            subscriptions = get_subscription_info(customer)
            products = [{'product': sub['product']} for sub in subscriptions]
            return JsonResponse({'purchased_products': products})
        else:
            return JsonResponse({'error': 'No customer found with that email'}, status=404)

class CustomerSinceView(View):
    def get(self, request, email):
        customer = find_customer_by_email(email)
        if customer:
            customer_since = datetime.datetime.fromtimestamp(customer.created).strftime('%Y-%m-%d %H:%M:%S')
            return JsonResponse({'customer_since': customer_since})
        else:
            return JsonResponse({'error': 'No customer found with that email'}, status=404)

class CustomerStatusView(View):
    def get(self, request, email):
        customer = find_customer_by_email(email)
        if customer:
            subscriptions = get_subscription_info(customer)
            statuses = [{'status': sub['status']} for sub in subscriptions]
            return JsonResponse({'statuses': statuses})
        else:
            return JsonResponse({'error': 'No customer found with that email'}, status=404)

class CustomerCurrentPeriodEndView(View):
    def get(self, request, email):
        customer = find_customer_by_email(email)
        if customer:
            subscriptions = get_subscription_info(customer)
            current_period_ends = [{'current_period_end': sub['current_period_end']} for sub in subscriptions]
            return JsonResponse({'current_period_ends': current_period_ends})
        else:
            return JsonResponse({'error': 'No customer found with that email'}, status=404)

class CustomerStartDateView(View):
    def get(self, request, email):
        customer = find_customer_by_email(email)
        if customer:
            subscriptions = get_subscription_info(customer)
            start_dates = [{'start_date': sub['start_date']} for sub in subscriptions]
            return JsonResponse({'start_dates': start_dates})
        else:
            return JsonResponse({'error': 'No customer found with that email'}, status=404)
