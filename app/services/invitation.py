import uuid
from app.schemas.invitation import InvitationCreate
from app.repositories.invitation import InvitationRepository
from fastapi import HTTPException
from sqlalchemy.orm.attributes import flag_modified

class InvitationService:
    def __init__(self, repo: InvitationRepository):
        self.repo = repo

    def get_invitation_data(self, slug: str):
        """Ստանում է հրավիրատոմսի տվյալները ըստ slug-ի"""
        invitation = self.repo.get_by_slug(slug)
        if not invitation:
            raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")
        return invitation

    def create_invitation(self, invitation_in: InvitationCreate):
        """Ստեղծում է նոր հրավիրատոմս ավտոմատ գեներացված տոկեններով"""
        data = invitation_in.model_dump()

        # Գեներացնում ենք անվտանգության տոկենները
        data["admin_token"] = str(uuid.uuid4())
        data["guest_token"] = str(uuid.uuid4())

        # Լռելյայն JSON բովանդակություն, եթե դատարկ է
        if not data.get("content"):
            data["content"] = {
                "couple_names": {"groom": "Փեսա", "bride": "Հարս"},
                "welcome_text": {"title": "Հրավեր", "description": "Սիրով սպասում ենք"},
                "locations": [],
                "rsvp_settings": {"deadline": None}
            }

        return self.repo.create(data)

    def update_invitation_by_token(self, admin_token: str, update_data: dict):
        """Թարմացնում է հրավիրատոմսը՝ օգտագործելով Repository-ի update մեթոդը"""
        invitation = self.repo.get_by_admin_token(admin_token)
        if not invitation:
            raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

        # Հեռացնում ենք դատարկ (None) արժեքները, որպեսզի պատահական չջնջենք հին տվյալները
        clean_data = {k: v for k, v in update_data.items() if v is not None}

        # Եթե թարմացվում է JSON բովանդակությունը (content)
        if "content" in clean_data:
            # SQLAlchemy-ին պետք է հուշել, որ JSON դաշտը փոփոխվել է
            setattr(invitation, "content", clean_data["content"])
            flag_modified(invitation, "content")
            # Հեռացնում ենք data-ից, քանի որ արդեն setattr արեցինք flag_modified-ով
            del clean_data["content"]

        # Մնացած բոլոր դաշտերը (music_url, event_date, is_custom, custom_html_path)
        # թարմացվում են Repository-ի միջոցով
        return self.repo.update(invitation, clean_data)