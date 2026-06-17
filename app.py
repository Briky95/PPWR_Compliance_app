import streamlit as st
import pandas as pd

# Configurazione della pagina
st.set_page_config(page_title="SaaS Compliance PPWR", page_icon="📦", layout="wide")

# Titolo Principale
st.title("📦 PPWR Compliance Dashboard")
st.subheader("Settore Alimentare - Controllo di Conformità Packaging")
st.markdown("---")

# --- SIMULAZIONE DATABASE INTERNO (Dati di esempio) ---
if 'componenti' not in st.session_state:
    st.session_state.componenti = [
        {"prodotto": "Bevanda Vegetale Avena 1L", "componente": "Corpo Brik Multistrato", "livello": "Primario", "materiale": "Poliaccoppiato", "peso": 32, "contatto_alim": True, "moca": "🔴 Mancante", "pfas": "🔴 Mancante", "metalli": "🟢 Approvato", "riciclo": "🟡 In Revisione"},
        {"prodotto": "Bevanda Vegetale Avena 1L", "componente": "Tappo a vite", "livello": "Primario", "materiale": "Plastica (HDPE)", "peso": 3, "contatto_alim": True, "moca": "🟢 Approvato", "pfas": "🟢 Approvato", "metalli": "🟢 Approvato", "riciclo": "🟢 Approvato"},
        {"prodotto": "Bevanda Vegetale Avena 1L", "componente": "Scatola di cartone (x12)", "livello": "Secondario", "materiale": "Carta/Cartone", "peso": 150, "contatto_alim": False, "moca": "N/A", "pfas": "N/A", "metalli": "🟢 Approvato", "riciclo": "🟢 Approvato"},
        {"prodotto": "Bevanda Vegetale Avena 1L", "componente": "Film termoretraibile pallet", "livello": "Terziario", "materiale": "Plastica (LDPE)", "peso": 250, "contatto_alim": False, "moca": "N/A", "pfas": "N/A", "metalli": "🟢 Approvato", "riciclo": "🔴 Mancante"}
    ]

# --- SIDEBAR: Selezione Prodotto e Caricamento Excel ---
st.sidebar.header("Navigazione & Onboarding")
prodotto_selezionato = st.sidebar.selectbox("Seleziona Prodotto", ["Bevanda Vegetale Avena 1L", "Nuovo Prodotto..."])

st.sidebar.markdown("---")
st.sidebar.subheader("Importazione Massiva")
uploaded_file = st.sidebar.file_uploader("Carica Excel della distinta base (BOM)", type=["xlsx", "csv"])
if uploaded_file is not None:
    st.sidebar.success("File caricato con successo! (Funzione di importazione in attivazione)")

# --- MAIN PAGE: Vista Prodotto Selezionato ---
if prodotto_selezionato == "Bevanda Vegetale Avena 1L":
    st.header(f"🍎 Prodotto: {prodotto_selezionato}")
    
    # Calcolo rapido dello stato globale
    comp_filtrati = [c for c in st.session_state.componenti if c["prodotto"] == prodotto_selezionato]
    mancanti = any(c["moca"] == "🔴 Mancante" or c["pfas"] == "🔴 Mancante" or c["riciclo"] == "🔴 Mancante" for c in comp_filtrati)
    
    if mancanti:
        st.error("⚠️ STATO GLOBALE: NON CONFORME (Ci sono documenti mancanti o requisiti non soddisfatti)")
    else:
        st.success("🟢 STATO GLOBALE: CONFORME")

    # Layout a schede per i livelli di imballaggio
    tab1, tab2, tab3 = st.tabs(["🔹 Imballaggio Primario", "🔸 Imballaggio Secondario", "🚚 Imballaggio Terziario"])

    levels = {"Primario": tab1, "Secondario": tab2, "Terziario": tab3}

    for livello, tab in levels.items():
        with tab:
            st.subheader(f"Componenti del packaging {livello.lower()}")
            for i, c in enumerate(st.session_state.componenti):
                if c["prodotto"] == prodotto_selezionato and c["livello"] == livello:
                    with st.expander(f"🔍 {c['componente']} ({c['materiale']} - {c['peso']}g)"):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        # Mostra lo stato attuale dei documenti
                        col1.markdown(f"**MOCA (Alimentare):** \n {c['moca']}")
                        col2.markdown(f"**PFAS (Art. 5):** \n {c['pfas']}")
                        col3.markdown(f"**Metalli Pesanti:** \n {c['metalli']}")
                        col4.markdown(f"**Riciclabilità (Art. 6):** \n {c['riclo'] if 'riclo' in c else c['riciclo']}")
                        
                        st.markdown(" ")
                        
                        # Logica di Alert Specifici (L'intelligenza del software)
                        if c["materiale"] == "Poliaccoppiato":
                            st.warning("⚠️ **Alert PPWR (Art. 6):** I materiali accoppiati sono a forte rischio riciclabilità dal 2030. Verificare i test di laboratorio del fornitore.")
                        if c["contatto_alim"] and c["pfas"] == "🔴 Mancante":
                            st.error("🚫 **Blocco Legale PFAS (Art. 5):** Vietato l'uso intenzionale di PFAS in imballaggi alimentari. Richiedere subito la dichiarazione al fornitore.")
                        if c["livello"] == "Terziario" and c["materiale"] == "Plastica (LDPE)":
                            st.info("💡 **Obbligo PCR (Art. 7):** Dal 2030 questo film plastico dovrà contenere almeno il 35% di plastica riciclata post-consumo.")
                        
                        # Azione rapida: Task per il fornitore
                        if c["moca"] == "🔴 Mancante" or c["pfas"] == "🔴 Mancante" or c["riciclo"] == "🔴 Mancante":
                            if st.button(f"Invia Task di Compliance a Fornitore per {c['componente']}", key=f"btn_{i}"):
                                st.success(f"📧 Magic Link generato e inviato al fornitore di: {c['componente']}!")

elif prodotto_selezionato == "Nuovo Prodotto...":
    st.header("➕ Censimento Nuovo Prodotto")
    nuovo_nome = st.text_input("Nome Prodotto Finito")
    nuovo_brand = st.text_input("Brand / Linea")
    if st.button("Salva Prodotto"):
        st.success(f"Prodotto '{nuovo_nome}' creato! Ora puoi caricare la sua distinta base.")
