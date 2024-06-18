from django.urls import path
from .views import (
    CustomerInfoView, CustomerEmailView, CustomerProductsView,
    CustomerSinceView, CustomerStatusView, CustomerCurrentPeriodEndView,
    CustomerStartDateView
)

urlpatterns = [
    path('customer-info/<str:email>/', CustomerInfoView.as_view(), name='customer-info'),
    path('customer-email/<str:email>/', CustomerEmailView.as_view(), name='customer-email'),
    path('customer-products/<str:email>/', CustomerProductsView.as_view(), name='customer-products'),
    path('customer-since/<str:email>/', CustomerSinceView.as_view(), name='customer-since'),
    path('customer-status/<str:email>/', CustomerStatusView.as_view(), name='customer-status'),
    path('customer-current_period_end/<str:email>/', CustomerCurrentPeriodEndView.as_view(), name='customer-current_period_end'),
    path('customer-start_date/<str:email>/', CustomerStartDateView.as_view(), name='customer-start_date'),
]
