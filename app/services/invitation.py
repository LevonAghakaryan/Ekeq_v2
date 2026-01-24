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