# Ներմուծում ենք բոլոր սխեմաները համապատասխան ֆայլերից
from .category import CategoryBase, CategorySchema
from .template import TemplateBase, TemplateCreate, TemplateSchema
from .invitation import InvitationBase, InvitationCreate, InvitationSchema, InvitationFullSchema
from .invitation_media import InvitationMediaBase, InvitationMediaCreate, InvitationMediaSchema
from .rsvp import RSVPResponseBase, RSVPResponseCreate, RSVPResponseSchema
from .order import OrderBase, OrderCreate, OrderSchema

# Այս ցուցակը պարտադիր չէ, բայց լավ պրակտիկա է՝ նշելու համար, թե ինչն է հասանելի դրսից
__all__ = [
    "CategoryBase", "CategorySchema",
    "TemplateBase", "TemplateCreate", "TemplateSchema",
    "InvitationBase", "InvitationCreate", "InvitationSchema","InvitationFullSchema",
    "InvitationMediaBase", "InvitationMediaCreate", "InvitationMediaSchema",
    "RSVPResponseBase", "RSVPResponseCreate", "RSVPResponseSchema",
    "OrderBase", "OrderCreate", "OrderSchema"
]