🍽️ Food Media

Food Media is a role-based social networking web app for the culinary world.
It connects Food Enthusiasts with Restaurants in a simple and interactive way.

✨ Key Features
Dual Roles
Restaurants: Post dishes, manage profile, view ratings
Enthusiasts: Like, comment, rate, and explore food
Feed System
Recent posts
Popular posts (based on likes)
Ratings & Points
Restaurants get ⭐ star ratings
Users earn 🍴 foodie points
Search & Discover
Find restaurants easily
View curated food content
Modern UI
Clean design with smooth navigation
Mobile-friendly layout
🛠️ Tech Stack
Backend: Django
Database: SQLite
Frontend: HTML, CSS, JavaScript
Image Handling: Pillow
🚀 Setup
# Activate virtual environment
.\venv\Scripts\Activate

# Install dependencies
pip install django pillow

# Setup database
python manage.py migrate

# Run server
python manage.py runserver

Visit: http://localhost:8000

👥 User Roles
Enthusiast → Explore, like, comment, rate
Restaurant → Post dishes, manage profile
Admin → Manage platform content
📁 Structure
accounts/ → users & authentication
feed/ → posts, likes, comments
discover/ → search & content
templates/ → HTML files
static/ → CSS & JS
