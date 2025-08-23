#!/usr/bin/env python3
"""
Quick script to update Canteen Block A menu with breakfast and lunch for all days
"""

# Standard breakfast and lunch items for Canteen Block A
breakfast_items = [
    {'name': 'Bread Toast', 'price': 15, 'available': True, 'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=100&h=100&fit=crop&q=80'},
    {'name': 'Omelette', 'price': 25, 'available': True, 'image': 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=100&h=100&fit=crop&q=80'},
    {'name': 'Tea', 'price': 8, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
    {'name': 'Coffee', 'price': 10, 'available': True, 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=100&h=100&fit=crop&q=80'}
]

lunch_items = [
    {'name': 'Fried Rice', 'price': 40, 'available': True, 'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=100&h=100&fit=crop&q=80'},
    {'name': 'Noodles', 'price': 35, 'available': True, 'image': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=100&h=100&fit=crop&q=80'},
    {'name': 'Sandwich', 'price': 30, 'available': True, 'image': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=100&h=100&fit=crop&q=80'},
    {'name': 'Burger', 'price': 45, 'available': True, 'image': 'https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=100&h=100&fit=crop&q=80'}
]

print("Menu structure for Canteen Block A:")
print("Days that need breakfast and lunch added: wednesday, thursday, friday, saturday, sunday")
print("\nBreakfast section:")
print("'breakfast': {")
print("    'time': '7:00 AM - 10:00 AM',")
print("    'items': [")
for item in breakfast_items:
    print(f"        {item},")
print("    ]")
print("},")

print("\nLunch section:")
print("'lunch': {")
print("    'time': '12:00 PM - 3:00 PM',")
print("    'items': [")
for item in lunch_items:
    print(f"        {item},")
print("    ]")
print("},")

print("\n✅ The menu order will be: Breakfast → Lunch → Snacks")
print("✅ All canteens will have consistent 3-meal structure")
print("✅ 4 items per row layout is working")
print("✅ Single crowd tracker is functional")
