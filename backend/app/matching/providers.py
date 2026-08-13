import json
import os
from typing import Dict, List, Set

from app.matching.normalizer import normalize_term


class ConceptProvider:
    def __init__(self, filepath: str):
        self.concepts: Dict[str, Dict[str, List[str]]] = {}
        # reverse mappings mapping a specific string to its root concepts
        self.alias_to_concept: Dict[str, Set[str]] = {}
        self.tech_to_concept: Dict[str, Set[str]] = {}
        self.course_to_concept: Dict[str, Set[str]] = {}

        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                raw_data = json.load(f)

            for concept, data in raw_data.items():
                norm_concept = normalize_term(concept)
                self.concepts[norm_concept] = {
                    "aliases": [normalize_term(a) for a in data.get("aliases", [])],
                    "technologies": [
                        normalize_term(t) for t in data.get("technologies", [])
                    ],
                    "coursework": [
                        normalize_term(c) for c in data.get("coursework", [])
                    ],
                }

                # Build reverse mappings
                for a in self.concepts[norm_concept]["aliases"]:
                    self.alias_to_concept.setdefault(a, set()).add(norm_concept)
                for t in self.concepts[norm_concept]["technologies"]:
                    self.tech_to_concept.setdefault(t, set()).add(norm_concept)
                for c in self.concepts[norm_concept]["coursework"]:
                    self.course_to_concept.setdefault(c, set()).add(norm_concept)

    def get_aliases(self, term: str) -> Set[str]:
        """Returns all known aliases for a term, including the term itself."""
        norm_term = normalize_term(term)
        aliases = {norm_term}

        # If the term is a root concept
        if norm_term in self.concepts:
            aliases.update(self.concepts[norm_term]["aliases"])

        # If the term is an alias, get its root concepts and their aliases
        if norm_term in self.alias_to_concept:
            for root_concept in self.alias_to_concept[norm_term]:
                aliases.add(root_concept)
                aliases.update(self.concepts[root_concept]["aliases"])

        return aliases

    def get_concepts_for_technology(self, tech_term: str) -> Set[str]:
        """Given a technology like 'spring boot', returns concepts like 'backend development'."""
        norm_tech = normalize_term(tech_term)
        return self.tech_to_concept.get(norm_tech, set())

    def get_technologies_for_concept(self, concept_term: str) -> Set[str]:
        """Given a concept, returns all technologies under it (and any of its aliases)."""
        aliases = self.get_aliases(concept_term)
        techs = set()
        for alias in aliases:
            if alias in self.concepts:
                techs.update(self.concepts[alias]["technologies"])
        return techs

    def get_concepts_for_coursework(self, course_term: str) -> Set[str]:
        """Given a course string, returns any matching concepts."""
        norm_course = normalize_term(course_term)
        concepts = set()
        for known_course, mapped_concepts in self.course_to_concept.items():
            if known_course in norm_course:
                concepts.update(mapped_concepts)
        return concepts


# Singleton
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
concept_provider = ConceptProvider(
    os.path.join(BASE_DIR, "data", "concepts", "v1.json")
)
