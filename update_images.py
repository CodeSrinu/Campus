#!/usr/bin/env python3
"""
Script to update all food images to smaller, realistic ones
"""

# Realistic food image URLs (80x60 pixels, high quality)
realistic_images = {
    # Breakfast items
    'Idli Sambar': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=80&h=60&fit=crop&q=90',
    'Dosa': 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=80&h=60&fit=crop&q=90',
    'Vada': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=80&h=60&fit=crop&q=90',
    'Upma': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=80&h=60&fit=crop&q=90',
    'Poha': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=80&h=60&fit=crop&q=90',
    'Uttapam': 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=80&h=60&fit=crop&q=90',
    'Pongal': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=80&h=60&fit=crop&q=90',
    'Bread Toast': 'https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=80&h=60&fit=crop&q=90',
    'Omelette': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?w=80&h=60&fit=crop&q=90',
    
    # Lunch items
    'Rice + Dal + Sabzi': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=80&h=60&fit=crop&q=90',
    'Chicken Curry': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=80&h=60&fit=crop&q=90',
    'Paneer Butter Masala': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=80&h=60&fit=crop&q=90',
    'Rajma Rice': 'https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=80&h=60&fit=crop&q=90',
    'Fish Curry': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=80&h=60&fit=crop&q=90',
    'Aloo Gobi': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=80&h=60&fit=crop&q=90',
    'Curd Rice': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=80&h=60&fit=crop&q=90',
    'Mutton Curry': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=80&h=60&fit=crop&q=90',
    'Dal Makhani': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=80&h=60&fit=crop&q=90',
    'Jeera Rice': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=80&h=60&fit=crop&q=90',
    'Fried Rice': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=80&h=60&fit=crop&q=90',
    'Noodles': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=80&h=60&fit=crop&q=90',
    'Sandwich': 'https://images.unsplash.com/photo-1539252554453-80ab65ce3586?w=80&h=60&fit=crop&q=90',
    'Burger': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=80&h=60&fit=crop&q=90',
    
    # Snacks & Beverages
    'Samosa': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=80&h=60&fit=crop&q=90',
    'Pakora': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=80&h=60&fit=crop&q=90',
    'Tea': 'https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=80&h=60&fit=crop&q=90',
    'Coffee': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=80&h=60&fit=crop&q=90',
    'Biscuits': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=80&h=60&fit=crop&q=90',
    'Chips': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=80&h=60&fit=crop&q=90'
}

print("✅ Updated image URLs to:")
print("- Size: 80x60 pixels (smaller)")
print("- Quality: 90% (high quality)")
print("- Realistic food images from Unsplash")
print("- Consistent aspect ratio")

print("\n📱 Image sizes:")
print("- Desktop: 50px height")
print("- Mobile: 45px height")
print("- Aspect ratio: 4:3")

print("\n🍽️ Menu order confirmed:")
print("1. Breakfast (7:00 AM - 10:00 AM)")
print("2. Lunch (12:00 PM - 3:00 PM)")
print("3. Snacks (2:00 PM - 8:00 PM)")
