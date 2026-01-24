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

    def create(self, data: dict):
        """Ստեղծում է նոր հրավիրատոմս"""
        db_invitation = Invitation(**data)
        self.db.add(db_invitation)
        self.db.commit()
        self.db.refresh(db_invitation)
        return db_invitation