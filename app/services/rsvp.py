from app.repositories.rsvp import RSVPRepository
from app import schemas

class RSVPService:
    def __init__(self, repo: RSVPRepository):
        self.repo = repo

    def submit_response(self, rsvp_data: schemas.RSVPResponseCreate):
        """Սա կկանչվի, երբ հյուրը սեղմի 'Ուղարկել' կոճակը հրավիրատոմսի վրա"""
        return self.repo.create(rsvp_data)

    def get_invitation_responses(self, invitation_id: int):
        """Տանտիրոջ համար՝ տեսնելու բոլոր հյուրերի անունները և նամակները"""
        return self.repo.get_by_invitation_id(invitation_id)

    def get_invitation_stats(self, invitation_id: int):
        """Տանտիրոջ համար՝ արագ տեսնելու ընդհանուր քանակը"""
        return self.repo.get_stats(invitation_id)