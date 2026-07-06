def build_esanjeevani_routing_gateway(patient_phone, doctor_name):
    clean_phone = patient_phone.replace("+", "").strip()
    msg = f"Andhra Pradesh e-Sanjeevani Link Active. Connecting you directly with: {doctor_name}. Please reply to begin consult."
    return f"https://whatsapp.com{clean_phone}&text={msg.replace(' ', '%20')}"
