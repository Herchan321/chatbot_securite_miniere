import unittest
from rag_bot import RAGSystem

class TestRAGSystem(unittest.TestCase):
    def setUp(self):
        self.rag = RAGSystem()
        self.rag.initialize()
    
    def test_basic_query(self):
        result = self.rag.query("Quels sont les EPI obligatoires ?")
        self.assertIn("answer", result)
        self.assertNotIn("error", result)
    
    def test_empty_query(self):
        result = self.rag.query("")
        self.assertTrue("error" in result or len(result["answer"]) > 0)

if __name__ == "__main__":
    unittest.main()