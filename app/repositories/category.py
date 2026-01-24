from sqlalchemy.orm import Session, joinedload
from app.models.category import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        """Վերադարձնում է բոլոր կատեգորիաները"""
        return self.db.query(Category).order_by(Category.id.asc()).all()

    def get_by_id(self, category_id: int):
        """Գտնում է կատեգորիան ըստ ID-ի"""
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_with_templates(self):
        """Բերում է բոլոր կատեգորիաները՝ ներառելով դրանց տակ գտնվող տեմպլեյթները (Eager Loading)"""
        return self.db.query(Category).options(joinedload(Category.templates)).all()