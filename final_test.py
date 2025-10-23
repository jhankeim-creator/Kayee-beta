#!/usr/bin/env python3
import requests
import json

# Test the exact data from the review request
backend_url = 'https://luxestore-dash.preview.emergentagent.com/api'

test_order_data = {
    'user_email': 'test@example.com',
    'user_name': 'Test User',
    'items': [
        {
            'product_id': 'test-123',
            'name': 'Test Product',
            'price': 100.0,
            'quantity': 1,
            'image': 'https://example.com/image.jpg'
        }
    ],
    'total': 110.0,
    'shipping_method': 'fedex',
    'shipping_cost': 10.0,
    'payment_method': 'stripe',
    'shipping_address': {
        'address': '123 Test St',
        'city': 'Test City',
        'postal_code': '12345',
        'country': 'USA'
    },
    'phone': '+1234567890',
    'notes': 'Test order'
}

print('🧪 Testing exact data from review request...')
response = requests.post(f'{backend_url}/orders', json=test_order_data, timeout=30)

if response.status_code == 200:
    order = response.json()
    print('✅ Order created successfully!')
    print(f'Order ID: {order.get("id")}')
    print(f'Order Number: {order.get("order_number")}')
    print(f'Total: ${order.get("total")}')
    print(f'Shipping Method: {order.get("shipping_method")}')
    print(f'Shipping Cost: ${order.get("shipping_cost")}')
    print(f'Payment Method: {order.get("payment_method")}')
    print(f'Stripe Payment ID: {order.get("stripe_payment_id")}')
    print(f'Stripe Payment URL: {order.get("stripe_payment_url")}')
    print(f'CoinPal Payment ID: {order.get("coinpal_payment_id")}')
    print(f'CoinPal Payment URL: {order.get("coinpal_payment_url")}')
    
    # Verify all requirements
    checks = []
    checks.append(('Total includes shipping', order.get('total') == 110.0))
    checks.append(('Shipping method is fedex', order.get('shipping_method') == 'fedex'))
    checks.append(('Shipping cost is 10', order.get('shipping_cost') == 10.0))
    checks.append(('Stripe payment ID exists', order.get('stripe_payment_id') is not None))
    checks.append(('Stripe payment URL exists', order.get('stripe_payment_url') is not None))
    checks.append(('CoinPal payment ID is None', order.get('coinpal_payment_id') is None))
    checks.append(('CoinPal payment URL is None', order.get('coinpal_payment_url') is None))
    
    print('\n📋 Requirements Check:')
    all_passed = True
    for check_name, passed in checks:
        status = '✅' if passed else '❌'
        print(f'{status} {check_name}')
        if not passed:
            all_passed = False
    
    if all_passed:
        print('\n🎉 ALL REQUIREMENTS PASSED!')
    else:
        print('\n⚠️ Some requirements failed!')
        
else:
    print(f'❌ Order creation failed: {response.status_code}')
    print(response.text)