from enum import Enum

class Gender(str, Enum):
    M = "M"
    F = "F"

class ProductCategoryEnum(str, Enum):
    FRUITS = "fruits"
    GRAINS = "grains"
    VEGETABLES = "vegetables"
    CEREALS = "cereals"
    LEGUMES = "legumes"
    SPICES = "spices"

class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"






