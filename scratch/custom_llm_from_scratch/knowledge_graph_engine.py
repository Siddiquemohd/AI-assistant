"""
Personal Knowledge Graph & Long-Term Memory Engine for ISAI Personal AI.
Extracts entities, relationships, and user preferences into a persistent graph structure.
"""
from typing import Dict, List, Any
import json

class KnowledgeGraphEngine:
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.triples: List[Dict[str, str]] = []

    def add_relation(self, subject: str, predicate: str, obj: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        triple = {
            "subject": subject.strip().title(),
            "predicate": predicate.strip().lower(),
            "object": obj.strip().title(),
            "metadata": metadata or {}
        }
        self.triples.append(triple)
        
        # Update node indices
        if triple["subject"] not in self.nodes:
            self.nodes[triple["subject"]] = {"relations": []}
        self.nodes[triple["subject"]]["relations"].append({"predicate": triple["predicate"], "target": triple["object"]})
        
        return {"status": "added", "triple": triple, "total_memories": len(self.triples)}

    def query(self, entity: str) -> List[Dict[str, str]]:
        entity_clean = entity.strip().title()
        matches = [t for t in self.triples if t["subject"] == entity_clean or t["object"] == entity_clean]
        return matches

    def summarize_knowledge(self) -> str:
        if not self.triples:
            return "Knowledge Graph is currently empty."
        lines = [f"- {t['subject']} {t['predicate']} {t['object']}" for t in self.triples]
        return "Personal Knowledge Graph Summary:\n" + "\n".join(lines)
