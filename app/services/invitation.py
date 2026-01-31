import uuid
from app.schemas.invitation import InvitationCreate
from app.repositories.invitation import InvitationRepository
from fastapi import HTTPException

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
        # 1. Սխեման սարքում ենք dict
        data = invitation_in.model_dump()

        # 2. Գեներացնում ենք UUID-ները և ավելացնում տվյալների մեջ
        # admin_token-ը կառավարման էջի համար (manage?at=...)
        data["admin_token"] = str(uuid.uuid4())

        # guest_token-ը դիտելու համար (invite?gt=...)
        data["guest_token"] = str(uuid.uuid4())

        # 3. Ուղարկում ենք ամբողջական տվյալները ռեպոզիտորիային
        return self.repo.create(data)