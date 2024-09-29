import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    GASBUDDY_API_KEY = os.getenv('GASBUDDY_API_KEY')


"""
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=supersecretkey
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
GASBUDDY_API_KEY=your_gasbuddy_api_key

"""