from datetime import timedelta

class Config:
    SECRET_KEY = "RD_Black_Jack_App"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
    USER = "Casino_Admin"
    PASSWORD = "AdminAdmin"