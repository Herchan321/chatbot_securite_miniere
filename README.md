# 🛡️ Assistant Sécurité Minière 

Un chatbot intelligent spécialisé en HSE (Hygiène, Sécurité, Environnement) pour l'industrie minière, développé avec LangChain, Streamlit et l'API Groq.

## 📋 Table des Matières

- [🎯 Objectif](#-objectif)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🛠️ Technologies](#️-technologies)
- [📁 Structure du Projet](#-structure-du-projet)
- [⚙️ Installation](#️-installation)
- [🚀 Lancement](#-lancement)
- [📚 Sources de Données](#-sources-de-données)
- [💬 Exemples d'Utilisation](#-exemples-dutilisation)
- [🔧 Configuration](#-configuration)
- [📊 Monitoring](#-monitoring)
- [🧪 Tests](#-tests)
- [🤝 Contribution](#-contribution)
- [📄 Licence](#-licence)

## 🎯 Objectif

Ce chatbot a été conçu pour aider les employés du secteur minier à :
- Comprendre les procédures de sécurité
- Identifier les équipements de protection requis
- Connaître les protocoles d'urgence
- Respecter les réglementations HSE
- Prévenir les accidents au travail

## ✨ Fonctionnalités

### 🤖 Intelligence Artificielle
- **RAG (Retrieval Augmented Generation)** : Combine recherche documentaire et génération de texte
- **Base vectorielle** : Indexation intelligente des documents HSE
- **Recherche sémantique** : Trouve les informations pertinentes même avec des formulations différentes

### 💻 Interface Utilisateur
- **Interface moderne** avec Streamlit
- **Chat en temps réel** avec historique
- **Affichage des sources** consultées
- **Alertes de sécurité** automatiques
- **Interface responsive** adaptée aux mobiles

### 🔍 Fonctionnalités Avancées
- **Monitoring des interactions** avec logging automatique
- **Diagnostic système** intégré
- **Gestion d'erreurs** robuste
- **Cache intelligent** pour des réponses rapides

## 🛠️ Technologies

| Technologie | Usage | Version |
|-------------|-------|---------|
| **Python** | Langage principal | 3.8+ |
| **Streamlit** | Interface web | Latest |
| **LangChain** | Framework RAG | Latest |
| **ChromaDB** | Base vectorielle | Latest |
| **HuggingFace** | Embeddings | transformers |
| **Groq API** | Modèle de langage | Llama 3.1 |
| **PyPDF** | Lecture PDF | Latest |

## 📁 Structure du Projet

```
securite_bot/
├── 📄 README.md                 # Documentation
├── 🐍 app.py                    # Interface Streamlit principale
├── 🔧 rag_bot.py                # Système RAG et logique métier
├── 📊 monitoring.py             # Système de logging et monitoring
├── ⚙️ config.py                 # Configuration centralisée (optionnel)
├── 📋 requirements.txt          # Dépendances Python
├── 🔐 .env                      # Variables d'environnement (à créer)
├── 📁 data/                     # Documents sources
│   ├── HSE_AAOURIDA.pdf         # Guide HSE spécifique
│   ├── STEULER-HSE-Management.pdf # Gestion HSE
│   ├── La sécurité et la santé.pdf # Documentation sécurité
│   └── mining_safety_database.json # Base de données sécurité
├── 🗃️ db/                       # Base vectorielle (généré automatiquement)
│   └── chroma.sqlite3
├── 📝 logs/                     # Fichiers de logs (généré automatiquement)
│   └── chatbot.log
└── 🧪 tests/                    # Tests unitaires (optionnel)
    └── test_rag.py
```

## ⚙️ Installation

### 1. Prérequis
- Python 3.8 ou supérieur
- Git
- Compte Groq (pour l'API)

### 2. Cloner le projet
```bash
git clone https://github.com/votre-username/securite_bot.git
cd securite_bot
```

### 3. Créer un environnement virtuel
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 5. Configuration des variables d'environnement
Créez un fichier `.env` dans le répertoire racine :
```env
GROQ_API_KEY=votre_clé_groq_ici
```

**🔑 Pour obtenir une clé Groq :**
1. Rendez-vous sur [console.groq.com](https://console.groq.com/)
2. Créez un compte gratuit
3. Générez une nouvelle clé API
4. Copiez-la dans votre fichier `.env`

## 🚀 Lancement

### Démarrage rapide
```bash
# Lancer l'application
streamlit run app.py
```

### Première utilisation
1. **Initialisation automatique** : Le système indexe automatiquement les documents au premier lancement
2. **Accès web** : Ouvrez votre navigateur à `http://localhost:8501`
3. **Test** : Posez votre première question sur la sécurité minière

### Tests et diagnostic
```bash
# Tester le système RAG
python rag_bot.py

# Diagnostic complet
python -c "from rag_bot import test_system_with_diagnosis; test_system_with_diagnosis()"
```

## 📚 Sources de Données

Le chatbot utilise les documents suivants comme base de connaissances :

| Document | Type | Contenu |
|----------|------|---------|
| `HSE_AAOURIDA.pdf` | PDF | Procédures HSE spécifiques OCP |
| `STEULER-HSE-Management.pdf` | PDF | Gestion et management HSE |
| `La sécurité et la santé.pdf` | PDF | Guide général sécurité |
| `mining_safety_database.json` | JSON | Base de données sécurité minière |

### Ajouter de nouveaux documents
1. Placez vos PDF dans le dossier `data/`
2. Modifiez la liste `pdf_files` dans `load_vectorstore()`
3. Relancez l'application pour réindexer

## 💬 Exemples d'Utilisation

### Questions sur les EPI
```
"Quels sont les équipements de protection obligatoires ?"
"Comment utiliser correctement un casque de sécurité ?"
"Quand porter des gants de protection ?"
```

### Questions sur les procédures
```
"Que faire en cas d'accident dans la mine ?"
"Quelles sont les procédures d'évacuation ?"
"Comment donner l'alerte en cas d'urgence ?"
```

### Questions sur les risques
```
"Quels sont les principaux risques miniers ?"
"Comment prévenir les éboulements ?"
"Quelles précautions avec les explosifs ?"
```

## 🔧 Configuration

### Paramètres RAG (dans `rag_bot.py`)
```python
# Taille des chunks de texte
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Nombre de documents récupérés
RETRIEVER_K = 5

# Paramètres du modèle
TEMPERATURE = 0.1
MAX_TOKENS = 1000
```

### Personnalisation de l'interface
Modifiez le CSS dans `app.py` section `st.markdown()` pour changer :
- Couleurs du thème
- Polices et tailles
- Mise en page

## 📊 Monitoring

### Logs automatiques
Le système enregistre automatiquement :
- **Interactions utilisateur** : Questions et réponses
- **Sources consultées** : Documents utilisés
- **Erreurs système** : Pour le débogage
- **Métriques de performance** : Temps de réponse

### Fichiers de logs
```
logs/
└── chatbot.log          # Log principal des interactions
```

### Analyse des logs
```python
from monitoring import ChatbotMonitor

monitor = ChatbotMonitor()
# Les interactions sont automatiquement loggées
```

## 🧪 Tests

### Tests de base
```bash
# Test du système RAG
python rag_bot.py

# Test avec diagnostic
python -c "from rag_bot import test_system_with_diagnosis; test_system_with_diagnosis()"
```

### Tests d'intégration
```bash
# Test de l'interface Streamlit
streamlit run app.py --headless
```

### Tests unitaires (optionnel)
```bash
python -m pytest tests/
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

