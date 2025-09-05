import streamlit as st
from rag_bot import RAGSystem
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Chatbot Sécurité Minière ",
    page_icon="🛡️",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.chat-message {
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}
.user-message {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
}
.assistant-message {
    background-color: #f1f8e9;
    border-left: 4px solid #4caf50;
}
.safety-tip {
    background-color: #fff3cd;
    padding: 1rem;
    border-left: 4px solid #ffc107;
    border-radius: 5px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('''
<div class="main-header">
    <h1>🛡️ Assistant Sécurité Minière </h1>
    <p>Expert en HSE pour l'industrie minière - Posez vos questions sur la sécurité</p>
</div>
''', unsafe_allow_html=True)

# Sidebar avec informations
with st.sidebar:
    st.header("ℹ️ Domaines d'expertise")
    st.info("""
    **Je peux vous aider avec :**
    - 🦺 Équipements de protection individuelle (EPI)
    - ⚠️ Procédures de sécurité minière
    - 🔥 Gestion des risques et dangers
    - 🚨 Protocoles d'urgence
    - 📋 Réglementation HSE
    - 💥 Sécurité des explosifs
    - 🚛 Sécurité des équipements lourds
    """)
    
    st.header("🚨 Numéros d'urgence")
    st.error("""
    **En cas d'urgence :**
    - 🚑 SAMU : 15
    - 🚒 Pompiers : 18
    - 👮 Police : 17
    - 📞 Urgences : 112
    
    **Évacuez immédiatement en cas de danger !**
    """)
    
    st.header("💡 Conseils sécurité")
    st.success("""
    - Portez toujours vos EPI
    - Respectez les consignes
    - Signalez les dangers
    - Restez vigilant
    """)

# Initialisation du système RAG
@st.cache_resource
def init_rag_system():
    try:
        with st.spinner("🔄 Initialisation du système..."):
            # Vérifier la clé API
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error("❌ GROQ_API_KEY manquante dans le fichier .env")
                return None
            
            rag = RAGSystem()
            if rag.initialize():
                st.success("✅ Système initialisé avec succès")
                return rag
            else:
                st.error("❌ Échec de l'initialisation du système RAG")
                return None
                
    except Exception as e:
        st.error(f"❌ Erreur lors de l'initialisation: {str(e)}")
        return None

# Initialiser le système
rag_system = init_rag_system()

if not rag_system:
    st.error("❌ Impossible d'initialiser le système. Vérifiez votre configuration.")
    st.info("💡 Vérifiez que votre clé API GROQ est correcte dans le fichier .env")
    st.stop()

# Interface de chat
st.header("💬 Chat Assistant")

# Initialisation des messages
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": """Bonjour ! 👋 

Je suis votre assistant spécialisé en **sécurité HSE pour l'industrie minière**.

🔍 **Comment puis-je vous aider ?**
- Questions sur les équipements de protection
- Procédures de sécurité spécifiques
- Gestion des risques miniers
- Protocoles d'urgence
- Réglementation HSE

Posez-moi votre question !"""
    })

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("💬 Posez votre question sur la sécurité minière..."):
    # Validation de l'input
    if len(prompt.strip()) < 3:
        st.warning("⚠️ Veuillez poser une question plus détaillée.")
        st.stop()
    
    # Afficher la question de l'utilisateur
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Générer et afficher la réponse
    with st.chat_message("assistant"):
        with st.spinner("🔍 Recherche dans la base de connaissances..."):
            try:
                # Interroger le système RAG
                result = rag_system.query(prompt)
                
                if "error" in result:
                    response = f"❌ Une erreur est survenue : {result['error']}"
                    st.error(response)
                else:
                    response = result["answer"]
                    st.markdown(response)
                    
                    # Afficher les sources consultées
                    if result.get("sources") and len(result["sources"]) > 0:
                        with st.expander("📚 Sources consultées", expanded=False):
                            sources = list(set(result["sources"]))  # Supprimer les doublons
                            for i, source in enumerate(sources, 1):
                                if source != "Inconnu":
                                    st.text(f"{i}. {source}")
                    
                    # Ajouter une note de sécurité
                    if any(keyword in prompt.lower() for keyword in ['urgence', 'accident', 'danger', 'blessure']):
                        st.warning("⚠️ **IMPORTANT :** En cas de situation d'urgence réelle, contactez immédiatement les secours (15, 18, ou 112) !")
                
            except Exception as e:
                response = f"❌ Une erreur technique est survenue : {str(e)}"
                st.error(response)
                st.info("💡 Veuillez réessayer ou reformuler votre question.")
    
    # Ajouter la réponse à l'historique
    st.session_state.messages.append({"role": "assistant", "content": response})

# Bouton pour effacer l'historique
with st.sidebar:
    st.markdown("---")
    if st.button("🗑️ Effacer l'historique", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    🛡️ Assistant Sécurité Minière OCP - Développé pour la sécurité au travail<br>
    ⚠️ Cet assistant fournit des informations générales. En cas d'urgence, contactez les secours.
</div>
""", unsafe_allow_html=True)
