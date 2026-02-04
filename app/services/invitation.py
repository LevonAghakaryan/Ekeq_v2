import uuid
from app.schemas.invitation import InvitationCreate
from app.repositories.invitation import InvitationRepository
from fastapi import HTTPException
from sqlalchemy.orm.attributes import flag_modified

class InvitationService:
    def __init__(self, repo: InvitationRepository):
        self.repo = repo

    def get_invitation_data(self, slug: str):
        """
        Ստանում է հրավիրատոմսի ամբողջական տվյալները:
        Եթե հրավիրատոմսը չկա, վերադարձնում է None:
        """
        invitation = self.repo.get_by_slug(slug)
        if not invitation:
            raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

        # Այստեղ կարող ես ավելացնել լրացուցիչ ստուգումներ,
        # օրինակ՝ արդյոք միջոցառման օրը չի անցել:
        return invitation

    def create_invitation(self, invitation_in: InvitationCreate):
        """
        Ստեղծում է նոր հրավիրատոմս և ավտոմատ գեներացնում է
        ադմինի ու հյուրի գաղտնի տոկենները:
        """
        """
        Ստեղծում է նոր հրավիրատոմս: 
        Եթե content-ը արդեն լրացված է Dashboard-ից, այն կպահպանվի:
        """
        # 1. Սխեման սարքում ենք dict
        data = invitation_in.model_dump()

        # 2. Գեներացնում ենք UUID-ները և ավելացնում տվյալների մեջ
        # admin_token-ը կառավարման էջի համար (manage?at=...)
        data["admin_token"] = str(uuid.uuid4())

        # guest_token-ը դիտելու համար (invite?gt=...)
        data["guest_token"] = str(uuid.uuid4())

        # Եթե Frontend-ից event_date-ը գալիս է որպես string,
        # Pydantic-ը այն արդեն դարձրել է datetime օբյեկտ։

        # Եթե Dashboard-ից JSON-ը դատարկ է եկել, նոր միայն դնում ենք default-ը:
        if not data.get("content"):
            data["content"] = {
                "couple_names": {"groom": "Փեսա", "bride": "Հարս"},
                "welcome_text": {"title": "Հրավեր", "description": "Սիրով սպասում ենք"},
                "locations": [],
                "rsvp_settings": {"deadline": None}
            }

        # 3. Պահպանում ենք ռեպոզիտորիի միջոցով
        return self.repo.create(data)

    def update_invitation_by_token(self, admin_token: str, update_data: dict):
        invitation = self.repo.get_by_admin_token(admin_token)
        if not invitation:
            raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

        # Թարմացնում ենք event_date-ը, եթե կա
        if "event_date" in update_data and update_data["event_date"]:
            invitation.event_date = update_data["event_date"]

        # Թարմացնում ենք երաժշտության URL-ը
        if "music_url" in update_data:
            invitation.music_url = update_data["music_url"]

        # Թարմացնում ենք հիմնական JSON բովանդակությունը
        if "content" in update_data:
            invitation.content = update_data["content"]
            # SQLAlchemy-ին հուշում ենք, որ JSON-ը փոխվել է
            flag_modified(invitation, "content")

        self.repo.db.commit()
        return invitation