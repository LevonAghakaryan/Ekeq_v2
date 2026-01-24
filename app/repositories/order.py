from sqlalchemy.orm import Session, joinedload
from app.models.order import Order
from app import schemas

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_data: schemas.OrderCreate):
        """Ստեղծում է նոր պատվեր"""
        db_order = Order(**order_data.model_dump())
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def get_all(self):
        """Բերում է բոլոր պատվերները՝ ներառելով տեմպլեյթի տվյալները"""
        return self.db.query(Order).options(joinedload(Order.template)).order_by(Order.created_at.desc()).all()

    def update_status(self, order_id: int, status: str):
        """Թարմացնում է պատվերի կարգավիճակը (օր.՝ 'Completed')"""
        db_order = self.db.query(Order).filter(Order.id == order_id).first()
        if db_order:
            db_order.status = status
            self.db.commit()
            self.db.refresh(db_order)
        return db_order