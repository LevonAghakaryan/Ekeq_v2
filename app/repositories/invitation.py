from sqlalchemy.orm import Session, joinedload
from app.models.invitation import Invitation


class InvitationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_slug(self, slug: str):
        """
        Գտնում է հրավիրատոմսը ըստ slug-ի և միանգամից բեռնում է
        տեմպլեյթը և բոլոր մեդիա ֆայլերը:
        """
        return self.db.query(Invitation).options(
            joinedload(Invitation.template),
            joinedload(Invitation.media_files)
        ).filter(Invitation.slug == slug).first()

    def get_by_admin_token(self, token: str):
        """Ադմինիստրատորի համար՝ իր տոկենով"""
        return self.db.query(Invitation).filter(Invitation.admin_token == token).first()

    def create(self, data: dict):
        # SQLAlchemy-ն ավտոմատ կլրացնի նաև is_custom-ը, եթե այն կա data-ի մեջ
        db_invitation = Invitation(**data)
        self.db.add(db_invitation)
        self.db.commit()
        self.db.refresh(db_invitation)
        return db_invitation

    # 👇 ԱՎԵԼԱՑՐՈՒ ԱՅՍ ՖՈՒՆԿՑԻԱՆ ԹԱՐՄԱՑՄԱՆ ՀԱՄԱՐ 👇
    def update(self, db_obj: Invitation, obj_in: dict):
        """
        Թարմացնում է գոյություն ունեցող օբյեկտը բազայում
        """
        for field in obj_in:
            if hasattr(db_obj, field):
                setattr(db_obj, field, obj_in[field])

        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj