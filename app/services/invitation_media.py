from app.repositories.invitation_media import InvitationMediaRepository
from app import schemas

class InvitationMediaService:
    def __init__(self, repo: InvitationMediaRepository):
        self.repo = repo

    def add_media_to_invitation(self, invitation_id: int, file_url: str, file_type: str, label: str = None):
        media_data = schemas.InvitationMediaCreate(
            invitation_id=invitation_id,
            file_url=file_url,
            file_type=file_type,
            label=label  # Այս դաշտը շատ կարևոր է HTML-ի համար
        )
        return self.repo.create(media_data)

    def add_multiple_media(self, invitation_id: int, media_files: list):
        """
        Օգտագործիր սա, եթե ունես նկարների ցուցակ:
        media_files-ը պետք է լինի այսպիսին՝ [{'file_url': '...', 'file_type': 'image'}, ...]
        """
        media_list = [
            schemas.InvitationMediaCreate(
                invitation_id=invitation_id,
                file_url=media['file_url'],
                file_type=media['file_type']
            )
            for media in media_files
        ]
        return self.repo.create_multiple(media_list)

    def get_invitation_media(self, invitation_id: int):
        """Սա կօգտագործվի հրավիրատոմսի էջում նկարները ցուցադրելու համար"""
        return self.repo.get_by_invitation_id(invitation_id)