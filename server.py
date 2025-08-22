import os
import json
from typing import Any, Dict, List, Optional
from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_cors import CORS
from datetime import datetime

DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.getcwd(), "data"))
BOUNDARY_PATH = os.path.join(DATA_DIR, "campus_boundary.geojson")
BUILDINGS_PATH = os.path.join(DATA_DIR, "buildings.geojson")
NAV_CONFIG_PATH = os.path.join(DATA_DIR, "navigation_config.json")

# In-memory storage for events
events = [
    {
        'id': 1,
        'name': 'Annual Sports Meet',
        'category': 'Sports',
        'date': '2025-01-15T09:00:00',
        'location': 'Sports Complex',
        'description': 'Annual inter-department sports competition featuring athletics, football, basketball, and more.',
        'participants': 'John Doe, Jane Smith, Mike Johnson',
        'coordinators': 'Coach Wilson: 9876543210, Prof. Davis: 9876543211',
        'winners': 'CSE Department - 1st Place, ECE Department - 2nd Place',
        'imageUrl': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop',
        'status': 'upcoming'
    },
    {
        'id': 2,
        'name': 'Cultural Night 2025',
        'category': 'Cultural',
        'date': '2025-01-20T18:00:00',
        'location': 'Auditorium',
        'description': 'A spectacular evening of music, dance, drama, and cultural performances by talented students.',
        'participants': 'Music Club, Dance Team, Drama Society',
        'coordinators': 'Prof. Kumar: 9876543212, Ms. Patel: 9876543213',
        'winners': 'Best Performance - Dance Team, Best Music - Guitar Ensemble',
        'imageUrl': 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=400&h=300&fit=crop',
        'status': 'upcoming'
    },
    {
        'id': 3,
        'name': 'Tech Fest 2025',
        'category': 'Tech',
        'date': '2025-01-25T10:00:00',
        'location': 'Computer Science Block',
        'description': 'Showcase of innovative projects, coding competitions, and tech talks by industry experts.',
        'participants': 'CSE Students, ECE Students, Tech Enthusiasts',
        'coordinators': 'Dr. Sharma: 9876543214, Prof. Reddy: 9876543215',
        'winners': 'Best Project - AI Chatbot, Best Coder - Alex Chen',
        'imageUrl': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop',
        'status': 'upcoming'
    },
    {
        'id': 4,
        'name': 'Basketball Tournament',
        'category': 'Sports',
        'date': '2025-01-10T16:00:00',
        'location': 'Basketball Court',
        'description': 'Inter-year basketball tournament with exciting matches and prizes.',
        'participants': 'All Year Students',
        'coordinators': 'Coach Anderson: 9876543216',
        'winners': '3rd Year - Champions, 2nd Year - Runners Up',
        'imageUrl': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400&h=300&fit=crop',
        'status': 'finished'
    },
    {
        'id': 5,
        'name': 'Poetry Slam',
        'category': 'Cultural',
        'date': '2025-01-12T19:00:00',
        'location': 'Library Seminar Hall',
        'description': 'An evening of powerful poetry performances and spoken word art.',
        'participants': 'Literature Club, Poetry Enthusiasts',
        'coordinators': 'Prof. Singh: 9876543217',
        'winners': 'Best Performance - Sarah Wilson, Most Creative - David Brown',
        'imageUrl': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop',
        'status': 'finished'
    },
    {
        'id': 6,
        'name': 'Hackathon 2025',
        'category': 'Tech',
        'date': '2025-01-18T08:00:00',
        'location': 'Innovation Lab',
        'description': '24-hour coding challenge to solve real-world problems with amazing prizes.',
        'participants': 'Coding Teams, Developers',
        'coordinators': 'Dr. Gupta: 9876543218, Prof. Iyer: 9876543219',
        'winners': '1st Place - Team CodeCraft, 2nd Place - Team Innovators',
        'imageUrl': 'https://images.unsplash.com/photo-1555066931-4365d9e62a0d?w=400&h=300&fit=crop',
        'status': 'ongoing'
    }
]
next_event_id = 7

# Lost & Found data
lost_found_items = []
next_item_id = 1

# Cafeteria data and user reporting system
cafeteria_data = {
    'main_cafeteria': {
        'name': 'Main Cafeteria',
        'current_rush_time': 15,
        'last_updated': None,
        'total_reports': 0,
        'crowd_reports': [],
        'menu': {
            'monday': {
                'breakfast': {
                    'time': '7:00 AM - 10:00 AM',
                    'items': [
                        {'name': 'Idli Sambar', 'price': 25, 'available': True, 'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Dosa', 'price': 30, 'available': True, 'image': 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Upma', 'price': 20, 'available': False, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Poha', 'price': 18, 'available': True, 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=100&h=100&fit=crop&q=80'}
                    ]
                },
                'lunch': {
                    'time': '12:00 PM - 3:00 PM',
                    'items': [
                        {'name': 'Rice + Dal + Sabzi', 'price': 45, 'available': True, 'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chicken Curry', 'price': 80, 'available': True, 'image': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Paneer Butter Masala', 'price': 70, 'available': False, 'image': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Rajma Rice', 'price': 50, 'available': True, 'image': 'https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'tuesday': {
                'breakfast': {
                    'time': '7:00 AM - 10:00 AM',
                    'items': [
                        {'name': 'Idli Sambar', 'price': 25, 'available': True, 'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Vada', 'price': 20, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Upma', 'price': 20, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Poha', 'price': 18, 'available': True, 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=100&h=100&fit=crop&q=80'}
                    ]
                },
                'lunch': {
                    'time': '12:00 PM - 3:00 PM',
                    'items': [
                        {'name': 'Rice + Dal + Sabzi', 'price': 45, 'available': True, 'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Fish Curry', 'price': 85, 'available': True, 'image': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Aloo Gobi', 'price': 60, 'available': True, 'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Curd Rice', 'price': 40, 'available': True, 'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'wednesday': {
                'breakfast': {
                    'time': '7:00 AM - 10:00 AM',
                    'items': [
                        {'name': 'Dosa', 'price': 30, 'available': True, 'image': 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Uttapam', 'price': 35, 'available': True, 'image': 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Upma', 'price': 20, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Poha', 'price': 18, 'available': True, 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=100&h=100&fit=crop&q=80'}
                    ]
                },
                'lunch': {
                    'time': '12:00 PM - 3:00 PM',
                    'items': [
                        {'name': 'Rice + Dal + Sabzi', 'price': 45, 'available': True, 'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Mutton Curry', 'price': 100, 'available': True, 'image': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Paneer Butter Masala', 'price': 70, 'available': True, 'image': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Rajma Rice', 'price': 50, 'available': True, 'image': 'https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'thursday': {
                'breakfast': {
                    'time': '7:00 AM - 10:00 AM',
                    'items': [
                        {'name': 'Idli Sambar', 'price': 25, 'available': True, 'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Dosa', 'price': 30, 'available': True, 'image': 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Pongal', 'price': 22, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Poha', 'price': 18, 'available': True, 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=100&h=100&fit=crop&q=80'}
                    ]
                },
                'lunch': {
                    'time': '12:00 PM - 3:00 PM',
                    'items': [
                        {'name': 'Rice + Dal + Sabzi', 'price': 45, 'available': True, 'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chicken Curry', 'price': 80, 'available': True, 'image': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Dal Makhani', 'price': 65, 'available': True, 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Jeera Rice', 'price': 45, 'available': True, 'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'friday': {
                'breakfast': {
                    'time': '7:00 AM - 10:00 AM',
                    'items': [
                        {'name': 'Idli Sambar', 'price': 25, 'available': True, 'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Dosa', 'price': 30, 'available': True, 'image': 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Pongal', 'price': 22, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Poha', 'price': 18, 'available': True, 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=100&h=100&fit=crop&q=80'}
                    ]
                },
                'lunch': {
                    'time': '12:00 PM - 3:00 PM',
                    'items': [
                        {'name': 'Rice + Dal + Sabzi', 'price': 45, 'available': True, 'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chicken Curry', 'price': 80, 'available': True, 'image': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Paneer Butter Masala', 'price': 70, 'available': True, 'image': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Rajma Rice', 'price': 50, 'available': True, 'image': 'https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'saturday': {
                'breakfast': {
                    'time': '7:00 AM - 10:00 AM',
                    'items': [
                        {'name': 'Idli Sambar', 'price': 25, 'available': True, 'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Dosa', 'price': 30, 'available': True, 'image': 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Upma', 'price': 20, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Poha', 'price': 18, 'available': True, 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=100&h=100&fit=crop&q=80'}
                    ]
                },
                'lunch': {
                    'time': '12:00 PM - 3:00 PM',
                    'items': [
                        {'name': 'Rice + Dal + Sabzi', 'price': 45, 'available': True, 'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chicken Curry', 'price': 80, 'available': True, 'image': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Paneer Butter Masala', 'price': 70, 'available': True, 'image': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Rajma Rice', 'price': 50, 'available': True, 'image': 'https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'sunday': {
                'breakfast': {
                    'time': '7:00 AM - 10:00 AM',
                    'items': [
                        {'name': 'Idli Sambar', 'price': 25, 'available': True, 'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Dosa', 'price': 30, 'available': True, 'image': 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Upma', 'price': 20, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Poha', 'price': 18, 'available': True, 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=100&h=100&fit=crop&q=80'}
                    ]
                },
                'lunch': {
                    'time': '12:00 PM - 3:00 PM',
                    'items': [
                        {'name': 'Rice + Dal + Sabzi', 'price': 45, 'available': True, 'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chicken Curry', 'price': 80, 'available': True, 'image': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Paneer Butter Masala', 'price': 70, 'available': True, 'image': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Rajma Rice', 'price': 50, 'available': True, 'image': 'https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            }
        }
    },
    'canteen_block_a': {
        'name': 'Canteen Block A',
        'current_rush_time': 12,
        'last_updated': None,
        'total_reports': 0,
        'crowd_reports': [],
        'menu': {
            'monday': {
                'snacks': {
                    'time': '9:00 AM - 6:00 PM',
                    'items': [
                        {'name': 'Samosa', 'price': 12, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Pakora', 'price': 15, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Tea', 'price': 8, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Biscuits', 'price': 10, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chips', 'price': 20, 'available': False, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'tuesday': {
                'snacks': {
                    'time': '9:00 AM - 6:00 PM',
                    'items': [
                        {'name': 'Samosa', 'price': 12, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Pakora', 'price': 15, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Tea', 'price': 8, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Biscuits', 'price': 10, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chips', 'price': 20, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'wednesday': {
                'snacks': {
                    'time': '9:00 AM - 6:00 PM',
                    'items': [
                        {'name': 'Samosa', 'price': 12, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Pakora', 'price': 15, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Tea', 'price': 8, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Biscuits', 'price': 10, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chips', 'price': 20, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'thursday': {
                'snacks': {
                    'time': '9:00 AM - 6:00 PM',
                    'items': [
                        {'name': 'Samosa', 'price': 12, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Pakora', 'price': 15, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Tea', 'price': 8, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Biscuits', 'price': 10, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chips', 'price': 20, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'friday': {
                'snacks': {
                    'time': '9:00 AM - 6:00 PM',
                    'items': [
                        {'name': 'Samosa', 'price': 12, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Pakora', 'price': 15, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Tea', 'price': 8, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Biscuits', 'price': 10, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chips', 'price': 20, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'saturday': {
                'snacks': {
                    'time': '9:00 AM - 6:00 PM',
                    'items': [
                        {'name': 'Samosa', 'price': 12, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Pakora', 'price': 15, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Tea', 'price': 8, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Biscuits', 'price': 10, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chips', 'price': 20, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            },
            'sunday': {
                'snacks': {
                    'time': '9:00 AM - 6:00 PM',
                    'items': [
                        {'name': 'Samosa', 'price': 12, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Pakora', 'price': 15, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Tea', 'price': 8, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Biscuits', 'price': 10, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'},
                        {'name': 'Chips', 'price': 20, 'available': True, 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=100&h=100&fit=crop&q=80'}
                    ]
                }
            }
        }
    }
}

# User reporting system with gamification
user_reports = {}
crowd_history = {}




def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Enable CORS for all routes (adjust origins for production as needed)
    CORS(app, resources={r"/*": {"origins": "*"}})



    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "Backend is running"}), 200

    # Home page at /
    @app.route("/", methods=["GET"])
    def home_page():
        return send_from_directory("templates", "index.html")


    # Serve Map at /map
    @app.route("/map", methods=["GET"])
    def map_page():
        return send_from_directory("templates", "map.html")


    @app.route("/api/campus/boundary", methods=["GET"])
    def get_campus_boundary():
        boundary = _load_campus_boundary()
        if boundary is None:
            return jsonify({"id": "campus", "name": "Campus (placeholder)", "coordinates": []}), 200
        return jsonify(boundary), 200

    @app.route("/api/locations", methods=["GET"])
    def get_locations():
        locations = _load_locations()
        return jsonify(locations), 200

    @app.route("/api/locations/<loc_id>", methods=["GET"])
    def get_location_by_id(loc_id: str):
        for loc in _load_locations():
            if str(loc.get("id")) == str(loc_id):
                return jsonify(loc), 200
        return jsonify({"error": "Location not found"}), 404



    @app.route("/api/navigation/config", methods=["GET"])
    def get_navigation_config():
        cfg = _load_nav_config()
        return jsonify(cfg), 200



    @app.route("/api/navigation/all", methods=["GET"])
    def get_navigation_all():
        boundary = _load_campus_boundary()
        if boundary is None:
            boundary = {"id": "campus", "name": "Campus (placeholder)", "coordinates": []}
        locations = _load_locations()
        cfg = _load_nav_config()
        return jsonify({
            "config": cfg,
            "boundary": boundary,
            "locations": locations,
        }), 200

    # -----------------------------
    # Events Routes
    # -----------------------------
    
    # Serve Events page at /events
    @app.route("/events", methods=["GET"])
    def events_page():
        return send_from_directory("templates", "events.html")

    # Comprehensive Events API Routes
    @app.route("/api/events", methods=["GET", "POST"])
    def handle_events():
        if request.method == "GET":
            return get_events()
        elif request.method == "POST":
            return create_event()

    def get_events():
        return jsonify(events), 200

    def create_event():
        global next_event_id
        data = request.get_json(silent=True) or {}
        
        # Validate required fields
        if not data or not all(key in data for key in ['name', 'date', 'location']):
            return jsonify({"error": "Missing required fields: name, date, location"}), 400
        
        # Create new event
        new_event = {
            'id': next_event_id,
            'name': data['name'],
            'date': data['date'],
            'location': data['location'],
            'description': data.get('description', ''),
            'category': data.get('category', 'General'),
            'participants': data.get('participants', ''),
            'coordinators': data.get('coordinators', ''),
            'winners': data.get('winners', ''),
            'imageUrl': data.get('imageUrl', ''),
            'status': 'Upcoming'
        }
        
        events.append(new_event)
        next_event_id += 1
        
        return jsonify(new_event), 201

    @app.route("/api/events/<int:event_id>", methods=["GET", "PUT", "DELETE"])
    def handle_event_by_id(event_id):
        if request.method == "GET":
            return get_event(event_id)
        elif request.method == "PUT":
            return update_event(event_id)
        elif request.method == "DELETE":
            return delete_event(event_id)

    def get_event(event_id):
        event = next((e for e in events if e['id'] == event_id), None)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify(event), 200

    def update_event(event_id):
        event = next((e for e in events if e['id'] == event_id), None)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        
        data = request.get_json(silent=True) or {}
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Update event fields
        for key, value in data.items():
            if key in event:
                event[key] = value
        
        return jsonify(event), 200

    def delete_event(event_id):
        global events
        event = next((e for e in events if e['id'] == event_id), None)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        
        events = [e for e in events if e['id'] != event_id]
        return jsonify({"message": "Event deleted"}), 200

    @app.route("/api/events/search", methods=["GET"])
    def search_events():
        query = request.args.get('query', '').lower()
        if not query:
            return jsonify(events), 200
        
        filtered_events = [
            e for e in events 
            if query in e['name'].lower() or query in e['description'].lower()
        ]
        return jsonify(filtered_events), 200

    @app.route("/api/events/filter", methods=["GET"])
    def filter_events():
        date_filter = request.args.get('date')
        location_filter = request.args.get('location')
        
        filtered_events = events.copy()
        
        if date_filter:
            filtered_events = [
                e for e in filtered_events 
                if e['date'].startswith(date_filter)
            ]
        
        if location_filter:
            filtered_events = [
                e for e in filtered_events 
                if location_filter.lower() in e['location'].lower()
            ]
        
        return jsonify(filtered_events), 200

    @app.route("/api/events/upcoming", methods=["GET"])
    def get_upcoming_events():
        today = datetime.now().strftime('%Y-%m-%d')
        upcoming_events = [
            e for e in events 
            if e['date'] >= today
        ]
        
        # Sort by date
        upcoming_events.sort(key=lambda x: x['date'])
        return jsonify(upcoming_events), 200

    # -----------------------------
    # Cafeteria Routes
    # -----------------------------
    
    # Serve Cafeteria page at /cafeteria
    @app.route("/cafeteria", methods=["GET"])
    def cafeteria_page():
        return send_from_directory("templates", "cafeteria.html")

    # Cafeteria crowd reporting API
    @app.route("/api/cafeteria/report-crowd", methods=["POST"])
    def report_crowd():
        """API endpoint for students to report crowd levels with gamification"""
        data = request.get_json()
        cafeteria_id = data.get('cafeteria_id')
        rush_time = data.get('rush_time')
        user_id = data.get('user_id', 'anonymous')

        if cafeteria_id in cafeteria_data and isinstance(rush_time, int) and 0 <= rush_time <= 60:
            # Update cafeteria data
            cafeteria_data[cafeteria_id]['current_rush_time'] = rush_time
            cafeteria_data[cafeteria_id]['last_updated'] = datetime.now().strftime('%H:%M')
            cafeteria_data[cafeteria_id]['total_reports'] += 1

            # Add to recent reports
            report = {
                'user_id': user_id,
                'rush_time': rush_time,
                'timestamp': datetime.now().strftime('%H:%M'),
                'crowd_level': get_crowd_level(rush_time)
            }

            cafeteria_data[cafeteria_id]['crowd_reports'].append(report)

            # Keep only last 10 reports
            if len(cafeteria_data[cafeteria_id]['crowd_reports']) > 10:
                cafeteria_data[cafeteria_id]['crowd_reports'] = cafeteria_data[cafeteria_id]['crowd_reports'][-10:]

            # Update user reporting stats
            if user_id not in user_reports:
                user_reports[user_id] = {'count': 0, 'points': 0, 'last_report': None}

            user_reports[user_id]['count'] += 1
            user_reports[user_id]['last_report'] = datetime.now().strftime('%H:%M')

            # Calculate points and badge
            badge = get_user_badge(user_reports[user_id]['count'])
            user_reports[user_id]['points'] = badge['points']
            user_reports[user_id]['badge'] = badge

            return jsonify({
                'success': True,
                'message': 'Crowd report submitted successfully! +10 points earned!',
                'data': {
                    'cafeteria': cafeteria_data[cafeteria_id],
                    'user_stats': user_reports[user_id],
                    'crowd_level': get_crowd_level(rush_time)
                }
            })

        return jsonify({
            'success': False,
            'message': 'Invalid cafeteria ID or rush time'
        }), 400

    # Get user reporting statistics and badges
    @app.route("/api/user/stats/<user_id>")
    def get_user_stats(user_id):
        if user_id in user_reports:
            return jsonify({
                'success': True,
                'data': user_reports[user_id]
            })
        else:
            return jsonify({
                'success': True,
                'data': {
                    'count': 0,
                    'points': 0,
                    'badge': get_user_badge(0),
                    'last_report': None
                }
            })

    # Get cafeteria status and menu
    @app.route("/api/cafeteria/status")
    def get_cafeteria_status():
        return jsonify({
            'success': True,
            'data': cafeteria_data
        })

    # -----------------------------
    # Lost & Found Routes
    # -----------------------------
    
    # Serve Lost & Found page at /lost-found
    @app.route("/lost-found", methods=["GET"])
    def lost_found_page():
        return send_from_directory("templates", "lost_found.html")

    # Get all lost and found items
    @app.route("/api/lost-found/items")
    def get_lost_found_items():
        return jsonify({
            'success': True,
            'data': lost_found_items
        })

    # Report a new lost or found item
    @app.route("/api/lost-found/report", methods=["POST"])
    def report_lost_found_item():
        global next_item_id
        
        try:
            data = request.get_json()
            
            new_item = {
                'id': next_item_id,
                'title': data.get('title'),
                'description': data.get('description'),
                'category': data.get('category'),
                'item_type': data.get('item_type'),  # 'lost' or 'found'
                'location': data.get('location'),
                'contact_method': data.get('contact_method'),
                'contact_info': data.get('contact_info', ''),
                'image_url': data.get('image_url', ''),
                'status': 'active',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'user_id': data.get('user_id', 'anonymous')
            }
            
            lost_found_items.append(new_item)
            next_item_id += 1
            
            return jsonify({
                'success': True,
                'message': 'Item reported successfully!',
                'item': new_item
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400

    # Get a specific lost or found item
    @app.route("/api/lost-found/items/<int:item_id>")
    def get_lost_found_item(item_id):
        item = next((item for item in lost_found_items if item['id'] == item_id), None)
        if item:
            return jsonify({
                'success': True,
                'data': item
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Item not found'
            }), 404

    # Resolve a lost or found item
    @app.route("/api/lost-found/items/<int:item_id>/resolve", methods=["POST"])
    def resolve_lost_found_item(item_id):
        item = next((item for item in lost_found_items if item['id'] == item_id), None)
        if item:
            item['status'] = 'resolved'
            return jsonify({
                'success': True,
                'message': 'Item marked as resolved!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Item not found'
            }), 404

    # Helper functions for cafeteria
    def get_user_badge(report_count):
        """Get user badge based on report count"""
        if report_count >= 50:
            return {'name': '🏆 Campus Hero', 'color': '#FFD700', 'points': 500, 'level': 5}
        elif report_count >= 25:
            return {'name': '⭐ Super Reporter', 'color': '#FF6B6B', 'points': 250, 'level': 4}
        elif report_count >= 10:
            return {'name': '🎯 Active Reporter', 'color': '#4ECDC4', 'points': 100, 'level': 3}
        elif report_count >= 5:
            return {'name': '📊 Regular Reporter', 'color': '#45B7D1', 'points': 50, 'level': 2}
        else:
            return {'name': '🆕 New Reporter', 'color': '#96CEB4', 'points': 10, 'level': 1}

    def get_crowd_level(rush_time):
        """Get crowd level with color coding and percentage"""
        if rush_time <= 5:
            return {
                'level': 'Low', 
                'color': '#28a745', 
                'icon': '🟢', 
                'description': 'No waiting, go now!',
                'percentage': min(rush_time * 20, 100),
                'meter_color': '#28a745'
            }
        elif rush_time <= 15:
            return {
                'level': 'Medium', 
                'color': '#ffc107', 
                'icon': '🟡', 
                'description': 'Short wait expected',
                'percentage': min(30 + (rush_time - 5) * 7, 100),
                'meter_color': '#ffc107'
            }
        else:
            return {
                'level': 'High', 
                'color': '#dc3545', 
                'icon': '🔴', 
                'description': 'Long wait, avoid if possible',
                'percentage': min(70 + (rush_time - 15) * 2, 100),
                'meter_color': '#dc3545'
            }

    # -----------------------------
    # Helpers: data loading & convert
    # -----------------------------

    def _safe_read_json(path: str) -> Optional[Dict[str, Any]]:
        try:
            if not os.path.isfile(path):
                return None
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Failed to read JSON from {path}: {e}", flush=True)
            return None

    def _geojson_outer_ring_to_latlng(geom: Dict[str, Any]) -> List[List[float]]:
        if not geom or "type" not in geom or "coordinates" not in geom:
            return []

        gtype = geom["type"]
        coords = geom["coordinates"]

        ring: List[List[float]] = []

        if gtype == "Polygon":
            if not coords or not coords[0]:
                return []
            outer = coords[0]
            ring = [[pt[1], pt[0]] for pt in outer if isinstance(pt, (list, tuple)) and len(pt) >= 2]
        elif gtype == "MultiPolygon":
            if not coords:
                return []
            candidate = max(coords, key=lambda poly: len(poly[0]) if poly and poly[0] else 0)
            if not candidate or not candidate[0]:
                return []
            outer = candidate[0]
            ring = [[pt[1], pt[0]] for pt in outer if isinstance(pt, (list, tuple)) and len(pt) >= 2]
        else:
            return []

        if ring and ring[0] != ring[-1]:
            ring.append(ring[0])
        return ring

    def _load_campus_boundary() -> Optional[Dict[str, Any]]:
        data = _safe_read_json(BOUNDARY_PATH)
        if not data:
            return None

        if data.get("type") == "Feature":
            geom = data.get("geometry", {})
            name = data.get("properties", {}).get("name") or "Campus"
        elif data.get("type") in ("Polygon", "MultiPolygon"):
            geom = data
            name = "Campus"
        else:
            if data.get("type") == "FeatureCollection" and data.get("features"):
                feat = data["features"][0]
                geom = feat.get("geometry", {})
                name = feat.get("properties", {}).get("name") or "Campus"
            else:
                return None

        coords_latlng = _geojson_outer_ring_to_latlng(geom)
        return {"id": "campus", "name": name, "coordinates": coords_latlng}

    def _load_locations() -> List[Dict[str, Any]]:
        data = _safe_read_json(BUILDINGS_PATH)
        if not data:
            return [
                {
                    "id": "b1",
                    "name": "Main Block",
                    "category": "Academic",
                    "coordinates": [[16.4945, 80.5123], [16.4946, 80.5129], [16.4941, 80.5130], [16.4940, 80.5124], [16.4945, 80.5123]],
                    "description": "Central academic building.",
                    "imageUrl": "https://example.com/main-block.jpg",
                },
                {
                    "id": "b2",
                    "name": "Auditorium",
                    "category": "Facility",
                    "coordinates": [[16.4930, 80.5110], [16.4934, 80.5115], [16.4929, 80.5118], [16.4926, 80.5112], [16.4930, 80.5110]],
                    "description": "Events and cultural programs.",
                    "imageUrl": "https://example.com/auditorium.jpg",
                },
            ]

        feats: List[Dict[str, Any]] = []
        if data.get("type") == "FeatureCollection":
            for feat in data.get("features", []):
                geom = feat.get("geometry", {})
                props = feat.get("properties", {})
                ring = _geojson_outer_ring_to_latlng(geom)
                if not ring:
                    continue
                feats.append({
                    "id": str(props.get("id") or props.get("code") or props.get("name") or len(feats) + 1),
                    "name": str(props.get("name") or "Building"),
                    "category": str(props.get("category") or "General"),
                    "coordinates": ring,
                    "description": str(props.get("description") or ""),
                    "imageUrl": str(props.get("imageUrl") or ""),
                })
        elif data.get("type") == "Feature":
            geom = data.get("geometry", {})
            props = data.get("properties", {})
            ring = _geojson_outer_ring_to_latlng(geom)
            if ring:
                feats.append({
                    "id": str(props.get("id") or props.get("code") or props.get("name") or 1),
                    "name": str(props.get("name") or "Building"),
                    "category": str(props.get("category") or "General"),
                    "coordinates": ring,
                    "description": str(props.get("description") or ""),
                    "imageUrl": str(props.get("imageUrl") or ""),
                })
        return feats

    def _load_nav_config() -> Dict[str, Any]:
        data = _safe_read_json(NAV_CONFIG_PATH)
        default = {
            "center": [16.493, 80.513],
            "defaultZoom": 17,
            "categoryColors": {
                "Academic": "#2563eb",
                "Admin": "#f59e0b",
                "Hostel": "#10b981",
                "Facility": "#8b5cf6",
                "Sports": "#ef4444",
                "General": "#3b82f6",
            },
        }
        if isinstance(data, dict):
            cfg = default.copy()
            for k in ("center", "defaultZoom", "categoryColors"):
                if k in data:
                    cfg[k] = data[k]
            return cfg
        return default



    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    # Bind to 0.0.0.0 for container/VM compatibility
    app.run(host="0.0.0.0", port=port, debug=debug)

