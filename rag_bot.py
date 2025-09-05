from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, JSONLoader
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

def load_vectorstore():
    """Charger et indexer les documents"""
    try:
        logger.info("📂 Chargement des documents...")
        documents = []
        
        # Charger les PDF
        pdf_files = ["data/HSE_AAOURIDA.pdf", "data/STEULER-HSE-Management.pdf"]
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                logger.info(f"📄 Chargement de {pdf_file}...")
                loader = PyPDFLoader(pdf_file)
                docs = loader.load()
                documents.extend(docs)
                logger.info(f"✅ PDF chargé: {pdf_file} ({len(docs)} pages)")
            else:
                logger.warning(f"⚠️ Fichier non trouvé: {pdf_file}")
        
        # Charger le JSON avec une approche plus simple
        json_file = "data/mining_safety_database.json"
        if os.path.exists(json_file):
            try:
                import json
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convertir chaque élément JSON en document
                from langchain.schema import Document
                for item in data:
                    if isinstance(item, dict):
                        content = json.dumps(item, ensure_ascii=False)
                        doc = Document(
                            page_content=content,
                            metadata={"source": json_file, "type": "json"}
                        )
                        documents.append(doc)
                
                logger.info(f"✅ JSON chargé: {json_file} ({len(data)} éléments)")
            except Exception as e:
                logger.warning(f"⚠️ Erreur chargement JSON: {e}")
        else:
            logger.warning(f"⚠️ Fichier JSON non trouvé: {json_file}")

        if not documents:
            raise Exception("Aucun document trouvé à indexer")

        logger.info(f"📊 {len(documents)} documents chargés")

        # Diviser les documents
        logger.info("✂️ Division des documents en chunks...")
        splitter = CharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200,
            separator="\n"
        )
        docs = splitter.split_documents(documents)
        logger.info(f"✅ {len(docs)} chunks créés")

        # Créer la base vectorielle
        logger.info("🔢 Création des embeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        logger.info("💾 Création de la base vectorielle...")
        vectordb = Chroma.from_documents(
            documents=docs, 
            embedding=embeddings, 
            persist_directory="db"
        )
        vectordb.persist()
        logger.info("✅ Base vectorielle créée et sauvegardée")
        return vectordb
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du chargement: {e}")
        raise

def get_chain():
    """Créer la chaîne RAG"""
    try:
        logger.info("🔗 Création de la chaîne RAG...")
        
        # Vérifier la clé API
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise Exception("GROQ_API_KEY manquante")
        logger.info("✅ Clé API vérifiée")
        
        # Charger ou créer la base vectorielle
        logger.info("🗃️ Chargement de la base vectorielle...")
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            # Vérifier si la base existe
            if os.path.exists("db") and os.listdir("db"):
                vectordb = Chroma(persist_directory="db", embedding_function=embeddings)
                logger.info("📊 Base vectorielle existante chargée")
            else:
                logger.info("Création d'une nouvelle base vectorielle...")
                vectordb = load_vectorstore()
                
        except Exception as e:
            logger.warning(f"Erreur de chargement de la base existante: {e}")
            logger.info("Création d'une nouvelle base vectorielle...")
            vectordb = load_vectorstore()
        
        logger.info("🔍 Création du retriever...")
        retriever = vectordb.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        # Créer le LLM
        logger.info("🤖 Création du modèle de langage...")
        llm = ChatOpenAI(
            openai_api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            model="llama-3.1-8b-instant",
            temperature=0.1,
            max_tokens=1000,
            timeout=60
        )
        logger.info("✅ Modèle de langage créé")
        
        # Template de prompt
        logger.info("📝 Création du template de prompt...")
        prompt_template = """Tu es un assistant spécialisé en sécurité HSE pour le domaine minier OCP.

Tu dois ABSOLUMENT utiliser les informations du contexte fourni pour répondre aux questions.
Ne dis JAMAIS "je ne dispose pas d'informations" ou "je n'ai pas assez d'informations".

Utilise TOUJOURS le contexte disponible pour construire une réponse pertinente, même si l'information n'est pas complète.
Si le contexte ne mentionne pas exactement ce qui est demandé, extrais les informations les plus proches et adapte ta réponse.

CONTEXTE DISPONIBLE:
{context}

QUESTION: {question}

RÉPONSE (en te basant sur le contexte ci-dessus):"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Créer la chaîne
        logger.info("⛓️ Assemblage de la chaîne finale...")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        logger.info("✅ Chaîne RAG créée avec succès")
        return qa_chain
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la création de la chaîne: {e}")
        import traceback
        logger.error(f"Détails de l'erreur: {traceback.format_exc()}")
        raise

# Classe RAGSystem pour compatibilité
class RAGSystem:
    def __init__(self):
        self.chain = None
        self.logger = logging.getLogger(f"{__name__}.RAGSystem")
        
    def initialize(self):
        try:
            self.logger.info("🚀 Début de l'initialisation RAGSystem...")
            self.chain = get_chain()
            self.logger.info("✅ RAGSystem initialisé avec succès")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erreur d'initialisation RAGSystem: {e}")
            import traceback
            self.logger.error(f"Traceback complet: {traceback.format_exc()}")
            return False
    
    def query(self, question):
        if not self.chain:
            return {"error": "Système non initialisé"}
        
        try:
            result = self.chain({"query": question})
            return {
                "answer": result["result"],
                "sources": [doc.metadata.get("source", "Inconnu") 
                           for doc in result.get("source_documents", [])]
            }
        except Exception as e:
            self.logger.error(f"Erreur lors de la requête: {e}")
            return {"error": str(e)}

# Fonction de diagnostic de la base vectorielle
def diagnose_vectorstore():
    """Diagnostiquer le contenu de la base vectorielle"""
    try:
        import os
        from langchain.embeddings import HuggingFaceEmbeddings
        from langchain.vectorstores import Chroma
        
        if os.path.exists("db"):
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            vectordb = Chroma(persist_directory="db", embedding_function=embeddings)
            
            # Test de recherche
            test_results = vectordb.similarity_search("réglementation HSE", k=5)
            
            print("=== DIAGNOSTIC VECTORSTORE ===")
            print(f"Nombre de documents trouvés: {len(test_results)}")
            
            for i, doc in enumerate(test_results):
                print(f"\n--- Document {i+1} ---")
                print(f"Source: {doc.metadata.get('source', 'Inconnue')}")
                print(f"Contenu (100 premiers caractères): {doc.page_content[:100]}...")
                
            return test_results
        else:
            print("❌ Aucune base vectorielle trouvée")
            return []
            
    except Exception as e:
        print(f"❌ Erreur diagnostic: {e}")
        return []

# Fonction de test simple
def test_system():
    """Fonction pour tester le système sans Streamlit"""
    try:
        rag = RAGSystem()
        if rag.initialize():
            print("✅ Système initialisé avec succès")
            
            # Test simple
            result = rag.query("Quels sont les équipements de protection ?")
            print(f"Réponse: {result}")
            return True
        else:
            print("❌ Échec de l'initialisation")
            return False
    except Exception as e:
        print(f"❌ Erreur de test: {e}")
        return False

# Fonction de test avec diagnostic
def test_system_with_diagnosis():
    """Test avec diagnostic détaillé"""
    print("🔍 DIAGNOSTIC DU SYSTÈME")
    
    # 1. Vérifier les fichiers
    files_to_check = [
        "data/HSE_AAOURIDA.pdf",
        "data/STEULER-HSE-Management.pdf", 
        "data/mining_safety_database.json"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} non trouvé")
    
    # 2. Diagnostiquer la base vectorielle
    diagnose_vectorstore()
    
    # 3. Tester le système
    try:
        rag = RAGSystem()
        if rag.initialize():
            print("\n✅ Système initialisé avec succès")
            
            # Tests de questions
            test_questions = [
                "réglementation HSE",
                "équipements de protection",
                "sécurité minière",
                "procédures"
            ]
            
            for question in test_questions:
                print(f"\n🔍 Test: {question}")
                result = rag.query(question)
                if "error" not in result:
                    print(f"✅ Réponse trouvée ({len(result['answer'])} caractères)")
                    print(f"📚 Sources: {result.get('sources', [])}")
                else:
                    print(f"❌ Erreur: {result['error']}")
            
            return True
        else:
            print("❌ Échec de l'initialisation")
            return False
    except Exception as e:
        print(f"❌ Erreur de test: {e}")
        return False

if __name__ == "__main__":
    test_system_with_diagnosis()