"""
Système de mémoire de XANA.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime


class MemoryType(Enum):
    """Types de mémoires."""
    OBSERVATION = "observation"
    SUCCESS = "succès"
    FAILURE = "échec"
    PATTERN = "pattern"
    THREAT = "menace"
    OPPORTUNITY = "opportunité"
    ADAPTATION = "adaptation"


@dataclass
class MemoryEntry:
    """Entrée dans la mémoire de XANA."""

    id: str
    memory_type: MemoryType
    tick: int
    timestamp: str
    data: Dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5  # 0.0 à 1.0
    relevance: float = 1.0  # Diminue avec le temps
    tags: List[str] = field(default_factory=list)

    def decay_relevance(self, amount: float = 0.01):
        """Diminue la pertinence avec le temps."""
        self.relevance = max(0.0, self.relevance - amount)

    def is_relevant(self) -> bool:
        """Détermine si la mémoire est encore pertinente."""
        return self.relevance > 0.1


class XANAMemory:
    """Système de mémoire de XANA."""

    def __init__(self, max_size: int = 1000):
        self.memories: List[MemoryEntry] = []
        self.max_size = max_size
        self.memory_counter = 0

    def add_memory(
        self,
        memory_type: MemoryType,
        tick: int,
        timestamp: str,
        data: Dict[str, Any],
        importance: float = 0.5,
        tags: List[str] = None
    ):
        """Ajoute une mémoire."""
        memory = MemoryEntry(
            id=f"MEM_{self.memory_counter:04d}",
            memory_type=memory_type,
            tick=tick,
            timestamp=timestamp,
            data=data,
            importance=importance,
            tags=tags or []
        )

        self.memories.append(memory)
        self.memory_counter += 1

        # Limite la taille de la mémoire
        if len(self.memories) > self.max_size:
            self._cleanup_old_memories()

    def get_memories_by_type(self, memory_type: MemoryType) -> List[MemoryEntry]:
        """Récupère toutes les mémoires d'un type donné."""
        return [m for m in self.memories if m.memory_type == memory_type and m.is_relevant()]

    def get_memories_by_tag(self, tag: str) -> List[MemoryEntry]:
        """Récupère toutes les mémoires avec un tag donné."""
        return [m for m in self.memories if tag in m.tags and m.is_relevant()]

    def get_recent_memories(self, count: int = 10) -> List[MemoryEntry]:
        """Récupère les N mémoires les plus récentes."""
        return sorted(self.memories, key=lambda m: m.tick, reverse=True)[:count]

    def get_important_memories(self, threshold: float = 0.7) -> List[MemoryEntry]:
        """Récupère les mémoires importantes."""
        return [m for m in self.memories if m.importance >= threshold and m.is_relevant()]

    def find_patterns(self, min_occurrences: int = 3) -> Dict[str, int]:
        """Identifie des patterns dans les mémoires."""
        patterns = {}

        for memory in self.memories:
            if not memory.is_relevant():
                continue

            for tag in memory.tags:
                patterns[tag] = patterns.get(tag, 0) + 1

        return {k: v for k, v in patterns.items() if v >= min_occurrences}

    def decay_all_memories(self, amount: float = 0.01):
        """Diminue la pertinence de toutes les mémoires."""
        for memory in self.memories:
            memory.decay_relevance(amount)

    def _cleanup_old_memories(self):
        """Nettoie les vieilles mémoires peu pertinentes."""
        # Garde les mémoires importantes et récentes
        self.memories.sort(key=lambda m: m.importance * m.relevance, reverse=True)
        self.memories = self.memories[:self.max_size]

    def get_success_rate_for_goal(self, goal_type: str) -> float:
        """Calcule le taux de réussite pour un type d'objectif."""
        successes = len([m for m in self.memories
                        if m.memory_type == MemoryType.SUCCESS
                        and goal_type in m.tags])
        failures = len([m for m in self.memories
                       if m.memory_type == MemoryType.FAILURE
                       and goal_type in m.tags])

        total = successes + failures
        if total == 0:
            return 0.5
        return successes / total

    def clear(self):
        """Efface toutes les mémoires."""
        self.memories.clear()
        self.memory_counter = 0

    def get_memory_count(self) -> int:
        """Retourne le nombre de mémoires actives."""
        return len([m for m in self.memories if m.is_relevant()])
