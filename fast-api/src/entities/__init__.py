from .db import *  # Import Base từ file db.py
from .repo import *  # Import Base từ file repo.py
from .user import User  # Import các model cụ thể
from .product import Product

# Base.metadata sẽ chứa metadata của tất cả các models (User, Product, ...)
__all__ = ["Base", "User", "Product"]
