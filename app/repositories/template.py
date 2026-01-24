from sqlalchemy.orm import Session, joinedload
from app.models.template import Template

class TemplateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        """Վերադարձնում է բոլոր տեմպլեյթները իրենց կատեգորիաների հետ միասին"""
        return self.db.query(Template).options(joinedload(Template.category)).all()

    def get_by_id(self, template_id: int):
        """Գտնում է կոնկրետ տեմպլեյթը"""
        return self.db.query(Template).options(joinedload(Template.category)).filter(Template.id == template_id).first()

    def get_by_category(self, category_id: int):
        """Ֆիլտրում է տեմպլեյթները ըստ կատեգորիայի ID-ի"""
        return self.db.query(Template).filter(Template.category_id == category_id).all()