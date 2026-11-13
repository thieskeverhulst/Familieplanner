import streamlit as st
from datetime import datetime
import json
import os

BESTANDSNAAM = "agenda.json"

st.set_page_config(
    page_title="Familieplanner",
    page_icon="👨‍👩‍👧‍👦",
    layout="centered"
)

def laad_agenda():
    if os.path.exists(BESTANDSNAAM):
        with open(BESTANDSNAAM, "r", encoding="utf-8") as bestand:
            return json.load(bestand)
    return []

def sla_agenda_op(agenda):
    with open(BESTANDSNAAM, "w", encoding="utf-8") as bestand:
        json.dump(agenda, bestand, indent=4, ensure_ascii=False)

familie_agenda = laad_agenda()

# ==========================================
# ZIJKANT (SIDEBAR) VOOR INVOER
# ==========================================
with st.sidebar:
    st.header("➕ Nieuwe afspraak")
    st.write("Vul hieronder de gegevens in.")
    
    taak = st.text_input("Taak/Afspraak?")
    datum = st.date_input("Datum")
    tijd = st.time_input("Tijd")

    if st.button("Afspraak opslaan", type="primary"):
        if taak:
            nieuwe_afspraak = {
                "taak": taak,
                "datum": str(datum),
                "tijd": str(tijd)
            }
            familie_agenda.append(nieuwe_afspraak)
            sla_agenda_op(familie_agenda)
            
            st.success("Opgeslagen!")
            st.rerun()
        else:
            st.warning("Vul alstublieft een taak in.")

# ==========================================
# HOOFDSCHERM (MAANDOVERZICHT & AGENDA)
# ==========================================
st.title("👨‍👩‍👧‍👦 Onze Familieplanner")
st.write("Welkom bij de gezinsagenda. Hieronder zie je het overzicht per maand.")
st.divider()

if familie_agenda:
    # Sorteer de afspraken netjes op datum
    familie_agenda_gesorteerd = sorted(familie_agenda, key=lambda x: x['datum'])

    # Handig lijstje voor de Nederlandse maandnamen
    maanden_nl = {
        1: "Januari", 2: "Februari", 3: "Maart", 4: "April", 
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Augustus", 
        9: "September", 10: "Oktober", 11: "November", 12: "December"
    }

    # Groepeer afspraken per maand en jaar
    maanden_dict = {}
    for afspraak in familie_agenda_gesorteerd:
        dt = datetime.strptime(afspraak['datum'], "%Y-%m-%d")
        maand_naam = maanden_nl[dt.month]
        jaar = dt.year
        maand_jaar = f"{maand_naam} {jaar}"
        
        if maand_jaar not in maanden_dict:
            maanden_dict[maand_jaar] = []
        maanden_dict[maand_jaar].append(afspraak)

    # Toon per maand het overzicht
    for maand, afspraken_in_maand in maanden_dict.items():
        st.subheader(f"🗓️ Maandoverzicht: {maand}")
        
        for afspraak in afspraken_in_maand:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### 📌 {afspraak['taak']}")
                with col2:
                    st.markdown(f"**{afspraak['datum']}**")
                    st.caption(f"Om {afspraak['tijd']} uur")
        
        st.write("") # Witregeltje
else:
    st.info("Nog geen afspraken gepland. Voeg er eentje toe via het menu aan de linkerkant! 👈")