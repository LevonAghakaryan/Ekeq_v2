from app.repositories.order import OrderRepository
from app import schemas

class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def place_order(self, order_data: schemas.OrderCreate):
        """Կանչվում է, երբ հաճախորդը սեղմում է 'Պատվիրել'"""
        # Այստեղ հետագայում կարող ես ավելացնել Notification (օր.՝ նամակ քեզ)
        return self.repo.create(order_data)

    def list_orders(self):
        """Քեզ համար՝ բոլոր պատվերները տեսնելու համար"""
        return self.repo.get_all()

    def complete_order(self, order_id: int):
        """Նշել պատվերը որպես ավարտված"""
        return self.repo.update_status(order_id, "Completed")