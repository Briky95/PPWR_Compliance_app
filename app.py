import streamlit as st
import pandas as pd

# Configurazione della pagina per un look moderno ed elegante
st.set_page_config(page_title="SaaS Compliance PPWR", page_icon="📦", layout="wide")

# --- STILE CSS PERSONALIZZATO ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #1E293B; /* Sfondo scuro elegante in stile dashboard */
        border: 1px solid #334155;
        padding: 20px; 
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); 
        text-align: center;
    }
    .metric-card h3 {
        color: #94A3B8 !important; /* Grigio chiaro per il sottotitolo */
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    .metric-card h2 {
        color: #F8FAFC !important; /* Bianco brillante per il numero */
        font-size: 2.5rem;
        margin-top: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- STATO DELL'APPLICAZIONE (Database temporaneo in memoria) ---
if 'prodotti' not in st.session_state:
    st.session_state.prodotti = [
        {"id": "PROD-001", "nome": "Bevanda Vegetale Avena 1L", "brand": "Linea Bio"}
    ]

if 'componenti' not in st.session_state:
    st.session_state.componenti = [
        {"prodotto_id": "PROD-001", "componente": "Corpo Brik Multistrato", "livello": "Primario", "materiale": "Poliaccoppiato", "peso": 32, "contatto_alim": True, "moca": "🔴 Mancante", "pfas": "🔴 Mancante", "metalli": "🟢 Approvato", "riciclo": "🟡 In Revisione"},
        {"prodotto_id": "PROD-001", "componente": "Tappo a vite", "livello": "Primario", "materiale": "Plastica (HDPE)", "peso": 3, "contatto_alim": True, "moca": "🟢 Approvato", "pfas": "🟢 Approvato", "metalli": "🟢 Approvato", "riciclo": "🟢 Approvato"},
        {"prodotto_id": "PROD-001", "componente": "Scatola di cartone (x12)", "livello": "Secondario", "materiale": "Carta/Cartone", "peso": 150, "contatto_alim": False, "moca": "N/A", "pfas": "N/A", "metalli": "🟢 Approvato", "riciclo": "🟢 Approvato"},
        {"prodotto_id": "PROD-001", "componente": "Film termoretraibile pallet", "livello": "Terziario", "materiale": "Plastica (LDPE)", "peso": 250, "contatto_alim": False, "moca": "N/A", "pfas": "N/A", "metalli": "🟢 Approvato", "riciclo": "🔴 Mancante"}
    ]

# --- NAVIGAZIONE PRINCIPALE ---
st.title("🌱 PPWR Compliance & Material Mapping SaaS")
menu = st.sidebar.radio("VISTE APPLICAZIONE", ["📊 Dashboard Globale", "➕ Inserisci Prodotto & BOM", "🔍 Analisi di Prodotto"])
st.sidebar.markdown("---")
st.sidebar.info("💡 **CTO Note:** Questa interfaccia simula il flusso di lavoro definitivo per il settore alimentare.")

# ==========================================
# 1. FUNZIONALITÀ: DASHBOARD GLOBALE
# ==========================================
if menu == "📊 Dashboard Globale":
    st.header("Anzianità e Stato della Conformità Aziendale")
    
    # KPI Top Cards
    tot_prod = len(st.session_state.prodotti)
    tot_comp = len(st.session_state.componenti)
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown(f"<div class='metric-card'><h3>Prodotti a Catalogo</h3><h2>{tot_prod}</h2></div>", unsafe_allow_html=True)
    with col_kpi2:
        st.markdown(f"<div class='metric-card'><h3>Componenti Packaging Mappati</h3><h2>{tot_comp}</h2></div>", unsafe_allow_html=True)
    with col_kpi3:
        st.markdown("<div class='metric-card'><h3>Rating Conformità Medio</h3><h2>72%</h2></div>", unsafe_allow_html=True)

    st.markdown("### 📋 Elenco Prodotti e Stato di Avanzamento")
    
    for p in st.session_state.prodotti:
        comp_p = [c for c in st.session_state.componenti if c["prodotto_id"] == p["id"]]
        verdi = sum(1 for c in comp_p for k in ["moca", "pfas", "metalli", "riciclo"] if c[k] == "🟢 Approvato")
        tot_doc_p = len(comp_p) * 4 if len(comp_p) > 0 else 1
        percentuale = min(int((verdi / tot_doc_p) * 100), 100)
        
        col_p1, col_p2, col_p3 = st.columns([3, 4, 2])
        col_p1.subheader(f"🔹 {p['nome']} ({p['brand']})")
        col_p2.progress(percentuale / 100)
        col_p2.caption(f"{percentuale}% della documentazione PPWR raccolta")
        
        if percentuale == 100:
            col_p3.success("🟢 PRONTO PER IL MERCATO")
        else:
            col_p3.warning("🟡 CONFORMAZIONE IN CORSO")
        st.markdown("---")

# ==========================================
# 2. FUNZIONALITÀ: INSERIMENTO PRODOTTO & BOM
# ==========================================
elif menu == "➕ Inserisci Prodotto & BOM":
    st.header("📝 Procedura Guidata di Censimento Packaging")
    
    step = st.radio("Passo del Flusso", ["Passo 1: Anagrafica Prodotto Finito", "Passo 2: Costruzione Distinta Base (BOM)"], horizontal=True)
    
    if step == "Passo 1: Anagrafica Prodotto Finito":
        st.subheader("1️⃣ Identificazione del Prodotto Alimentare")
        with st.form("form_prodotto"):
            nuovo_id = f"PROD-00{len(st.session_state.prodotti)+1}"
            nome_p = st.text_input("Nome Commerciale del Prodotto", placeholder="Es. Olio Extra Vergine di Oliva 750ml")
            brand_p = st.text_input("Brand / Linea di appartenenza", placeholder="Es. Linea Premium GDO")
            
            submit_p = st.form_submit_button("Salva Prodotto e Procedi")
            if submit_p:
                if nome_p:
                    st.session_state.prodotti.append({"id": nuovo_id, "nome": nome_p, "brand": brand_p})
                    st.success(f"✅ Prodotto salvato con ID: {nuovo_id}. Passa ora al 'Passo 2' in alto per mappare i materiali!")
                else:
                    st.error("Il nome del prodotto è obbligatorio.")

    elif step == "Passo 2: Costruzione Distinta Base (BOM)":
        st.subheader("2️⃣ Associa Componenti di Packaging e attiva i Filtri PPWR")
        
        prod_target = st.selectbox("Seleziona il prodotto per cui stai inserendo i materiali:", 
                                   options=st.session_state.prodotti, 
                                   format_func=lambda x: f"{x['nome']} ({x['brand']})")
        
        with st.form("form_componente"):
            col_c1, col_c2 = st.columns(2)
            nome_c = col_c1.text_input("Nome del singolo componente", placeholder="Es. Tappo, Bottiglia in Vetro, Etichetta, Film...")
            livello_c = col_c1.selectbox("Livello Imballaggio (PPWR)", ["Primario", "Secondario", "Terziario"])
            materiale_c = col_c1.selectbox("Materiale Prevalente", ["Poliaccoppiato", "Plastica (PET)", "Plastica (HDPE)", "Plastica (LDPE)", "Carta/Cartone", "Vetro", "Alluminio/Acciaio"])
            
            peso_c = col_c2.number_input("Peso in grammi (Dato per minimizzazione Art.9)", min_value=1, value=10)
            contatto_c = col_c2.checkbox("È a contatto diretto con l'alimento? (Attiva vincolo MOCA e BAN PFAS)")
            
            submit_c = st.form_submit_button("Aggiungi Componente alla Distinta Base")
            if submit_c and nome_c:
                # Logica di pre-compilazione degli stati documentali
                nuovo_comp = {
                    "prodotto_id": prod_target["id"],
                    "componente": nome_c,
                    "livello": livello_c,
                    "materiale": materiale_c,
                    "peso": peso_c,
                    "contatto_alim": contatto_c,
                    "moca": "🔴 Mancante" if contatto_c else "N/A",
                    "pfas": "🔴 Mancante" if contatto_c else "N/A",
                    "metalli": "🔴 Mancante",
                    "riciclo": "🔴 Mancante"
                }
                st.session_state.componenti.append(nuovo_comp)
                st.success(f"✅ '{nome_c}' aggiunto con successo alla distinta base!")

        # Mostra la distinta base attuale del prodotto selezionato
        st.markdown("### Distinta base attuale per questo prodotto:")
        comp_attuali = [c for c in st.session_state.componenti if c["prodotto_id"] == prod_target["id"]]
        if comp_attuali:
            st.dataframe(pd.DataFrame(comp_attuali).drop(columns=["prodotto_id"]))
        else:
            st.info("Nessun componente ancora inserito per questo prodotto.")

# ==========================================
# 3. FUNZIONALITÀ: DETTAGLIO E ANALISI DI COMPLIANCE
# ==========================================
elif menu == "🔍 Analisi di Prodotto":
    st.header("🧐 Esame di Conformità e Gestione Documentale")
    prod_scelto = st.selectbox("Seleziona Prodotto da Esaminare", options=st.session_state.prodotti, format_func=lambda x: x['nome'])
    
    comp_filtrati = [c for c in st.session_state.componenti if c["prodotto_id"] == prod_scelto["id"]]
    
    if not comp_filtrati:
        st.info("Questo prodotto non ha ancora componenti associati. Vai nella scheda 'Inserisci Prodotto' per mapparli.")
    else:
        for i, c in enumerate(comp_filtrati):
            with st.expander(f"📦 {c['componente']} — Livello {c['livello']} ({c['materiale']})"):
                col1, col2, col3, col4 = st.columns(4)
                
                # Interfaccia di approvazione dei documenti
                c["moca"] = col1.selectbox("Stato MOCA", ["🔴 Mancante", "🟡 In Revisione", "🟢 Approvato", "N/A"], index=["🔴 Mancante", "🟡 In Revisione", "🟢 Approvato", "N/A"].index(c["moca"]), key=f"moca_{i}")
                c["pfas"] = col2.selectbox("Stato PFAS (Art.5)", ["🔴 Mancante", "🟡 In Revisione", "🟢 Approvato", "N/A"], index=["🔴 Mancante", "🟡 In Revisione", "🟢 Approvato", "N/A"].index(c["pfas"]), key=f"pfas_{i}")
                c["metalli"] = col3.selectbox("Metalli Pesanti", ["🔴 Mancante", "🟡 In Revisione", "🟢 Approvato"], index=["🔴 Mancante", "🟡 In Revisione", "🟢 Approvato"].index(c["metalli"]), key=f"met_{i}")
                c["riciclo"] = col4.selectbox("Design for Recycling", ["🔴 Mancante", "🟡 In Revisione", "🟢 Approvato"], index=["🔴 Mancante", "🟡 In Revisione", "🟢 Approvato"].index(c['riciclo']), key=f"ric_{i}")
                
                # Motore di regole e Alert Intelligenti
                if c["materiale"] == "Poliaccoppiato":
                    st.warning("⚠️ **Alert PPWR (Criteri 2030):** I materiali poliaccoppiati (carta/plastica/alluminio) dovranno dimostrare la riciclabilità su scala entro il 2030. Richiedere al fornitore il test di laboratorio.")
                if c["contatto_alim"] and c["pfas"] != "🟢 Approvato":
                    st.error("🚫 **Blocco Legale PFAS:** Il PPWR vieta i PFAS negli imballaggi alimentari. Senza la dichiarazione di assenza firmata, il lotto non è conforme.")
                
                # Pulsante di Invio Task
                if any(c[k] == "🔴 Mancante" for k in ["moca", "pfas", "metalli", "riciclo"]):
                    if st.button(f"Invia Link di Caricamento al Fornitore per {c['componente']}", key=f"btn_task_{i}"):
                        st.success(f"📩 Email di notifica generata per il fornitore. È stato creato un perno sicuro per l'upload del file.")
