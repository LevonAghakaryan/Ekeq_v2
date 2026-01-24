from sqlalchemy.orm import Session
from app.models.invitation_media import InvitationMedia
from app import schemas

class InvitationMediaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, media_data: schemas.InvitationMediaCreate):
        """Պահում է մեկ նկար կամ վիդեո"""
        db_media = InvitationMedia(**media_data.model_dump())
        self.db.add(db_media)
        self.db.commit()
        self.db.refresh(db_media)
        return db_media

    def create_multiple(self, media_list: list[schemas.InvitationMediaCreate]):
        """Պահում է մի քանի ֆայլ միանգամից"""
        db_media_list = [InvitationMedia(**item.model_dump()) for item in media_list]
        self.db.add_all(db_media_list)
        self.db.commit()
        return db_media_list

    def get_by_invitation_id(self, invitation_id: int):
        """Բերում է տվյալ հրավիրատոմսի ամբողջ մեդիան"""
        return self.db.query(InvitationMedia).filter(
            InvitationMedia.invitation_id == invitation_id
        ).all()