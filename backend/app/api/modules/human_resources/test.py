from app.api.modules.personel.models import Personel
from generate_schema_from_model import generate_schemas_from_model

PersonelCreate, PersonelUpdate, PersonelRead = generate_schemas_from_model(Personel)
