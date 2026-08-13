# app/services/parser_service.py
from typing import Dict, Any
from app.schemas.payload import StandardizedLeadSchema
from app.core.security import sanitize_text

class PayloadParserService:
    @staticmethod
    def parse_payload(source_slug: str, raw_json: Dict[str, Any]) -> StandardizedLeadSchema:
        """
        Extracts key lead attributes across varying payload standards 
        (Typeform, Google Forms, Custom JSON) and cleans all values.
        """
        lead = StandardizedLeadSchema()
        
        if source_slug.lower() == "typeform":
            # Extract from Typeform response architecture
            form_response = raw_json.get("form_response", {})
            lead.form_title = sanitize_text(form_response.get("definition", {}).get("title", "Typeform Submission"))
            
            answers = form_response.get("answers", [])
            fields = form_response.get("definition", {}).get("fields", [])
            field_map = {f["id"]: f["title"] for f in fields}
            
            extracted_fields = {}
            for ans in answers:
                field_id = ans.get("field", {}).get("id")
                label = field_map.get(field_id, "Question")
                
                # Derive answer by dynamic type
                ans_type = ans.get("type")
                val = ans.get(ans_type)
                if isinstance(val, dict):
                    val = val.get("label") or str(val)
                
                val_clean = sanitize_text(str(val))
                extracted_fields[label] = val_clean
                
                # Smart field mapping
                label_lower = label.lower()
                if "name" in label_lower:
                    lead.lead_name = val_clean
                elif "email" in label_lower:
                    lead.lead_email = val_clean
                elif "phone" in label_lower or "mobile" in label_lower:
                    lead.lead_phone = val_clean
                elif "message" in label_lower or "note" in label_lower:
                    lead.message = val_clean

            lead.raw_fields = extracted_fields

        else:
            # Generic/Google Forms webhook structure handler
            lead.form_title = sanitize_text(raw_json.get("form_title", "Inbound Contact Lead"))
            
            clean_dict = {}
            for k, v in raw_json.items():
                k_clean = sanitize_text(str(k))
                v_clean = sanitize_text(str(v))
                clean_dict[k_clean] = v_clean
                
                k_lower = k_clean.lower()
                if "name" in k_lower and lead.lead_name == "Valued Prospect":
                    lead.lead_name = v_clean
                elif "email" in k_lower and not lead.lead_email:
                    lead.lead_email = v_clean
                elif ("phone" in k_lower or "mobile" in k_lower) and not lead.lead_phone:
                    lead.lead_phone = v_clean
                elif ("message" in k_lower or "comment" in k_lower) and lead.message == "No message body supplied.":
                    lead.message = v_clean

            lead.raw_fields = clean_dict

        return lead

parser_service = PayloadParserService()
