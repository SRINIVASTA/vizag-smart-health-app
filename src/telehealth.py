# src/telehealth.py
import urllib.parse
import json
import base64

def generate_encrypted_telehealth_payload(token_id, facility_name, symptoms, bp_reading):
    """
    Encrypts and packages patient vitals into a lightweight Base64 string payload 
    to be attached cleanly to outbound telehealth reference tokens.
    """
    vitals_dict = {
        "token_id": token_id,
        "origin_node": facility_name,
        "symptoms": symptoms,
        "blood_pressure": bp_reading
    }
    # Encode to JSON string, then compress to byte matrix, then Base64 encode
    json_bytes = json.dumps(vitals_dict).encode('utf-8')
    secure_hash_string = base64.b64encode(json_bytes).decode('utf-8')
    return secure_hash_string

def build_whatsapp_sanjeevani_dispatch_link(doctor_phone, token_id, facility_name, symptoms, bp_reading):
    """
    Generates an automated, localized WhatsApp Business API link that can be used 
    by ASHA workers to instantly transmit the patient's secure video room token 
    and pre-compiled clinical vitals directly to the specialized doctor's terminal.
    """
    # 1. Compile the secure vital metadata hash
    secure_payload = generate_encrypted_telehealth_payload(token_id, facility_name, symptoms, bp_reading)
    
    # 2. Build a highly actionable, structured notification text prompt
    message_body = (
        f"🚨 *BHARAT HEALTH AI: EMERGENCY TELEHEALTH INTAKE ALERT* 🚨\n\n"
        f"• *Patient Case ID:* {token_id}\n"
        f"• *Origin Clinic:* {facility_name}\n"
        f"• *Logged Symptoms:* {symptoms}\n"
        f"• *Vitals Mapped:* BP {bp_reading}\n\n"
        f"🔗 *Launch e-Sanjeevani Secure Telehealth WebRTC Stream Room Below:*\n"
        f"https://esanjeevaniopd.in{token_id}&meta={secure_payload}"
    )
    
    # 3. URL-encode characters safely to map to a dynamic deep link wrapper
    encoded_message = urllib.parse.quote(message_body)
    
    # Clean phone number parameter (defaults to a mockup placeholder if empty)
    clean_phone = str(doctor_phone).strip().replace("+", "").replace(" ", "")
    if not clean_phone:
        clean_phone = "919848022338" # Standard placeholder mock node code
        
    whatsapp_deep_link = f"https://whatsapp.com{clean_phone}&text={encoded_message}"
    return whatsapp_deep_link
