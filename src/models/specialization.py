from enum import Enum
from pydantic import BaseModel, model_validator


class Domains(Enum):
    CONSULTING_MEDICINE = 'רפואה יועצת'
    DENTISTRY = 'כללית סמייל'

class ConsultingMedicineSpecializations(Enum):
    ORTHOPEDICS = 'אורתופדיה'
    ENT = 'אף אוזן גרון'
    SKIN = 'עור'
    EYES = 'עיניים'
    LARYNGOSCOPY = 'א.א.ג - לרינגוסקופיה'
    FAMILY_DOCTOR = 'רפואת משפחה/ילדים'
    
class DentistrySpecializations(Enum):
    DENTIST = 'בדיקת רופא'
    TOOTH_FILLING = 'סתימה'
    DENTAL_HYGIENIST = 'שיננית'  
    
class Specialization(BaseModel):
    name: str
    domain: str = ''
    
    @model_validator(mode='before')
    def set_specialization_details(cls, values: dict) -> dict:
        specialization = values['name'].upper()
        is_consulting_medicine = specialization in ConsultingMedicineSpecializations.__members__
        is_dentistry = specialization in DentistrySpecializations.__members__
        
        if is_consulting_medicine or is_dentistry:
            values['domain'] = 'consulting_medicine' if is_consulting_medicine else 'dentistry'
            return values
        raise ValueError(f"{specialization} is not a valid specialization")
