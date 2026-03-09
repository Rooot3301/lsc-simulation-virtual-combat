"""
Ordonnanceur pour gérer l'exécution des tâches de la simulation.
"""

from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any
from enum import Enum


class Priority(Enum):
    """Priorités d'exécution des tâches."""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class ScheduledTask:
    """Représente une tâche planifiée."""
    name: str
    callback: Callable
    priority: Priority = Priority.NORMAL
    enabled: bool = True
    args: List[Any] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)

    def execute(self):
        """Exécute la tâche."""
        if self.enabled:
            return self.callback(*self.args, **self.kwargs)
        return None


class Scheduler:
    """
    Ordonnanceur pour gérer l'ordre d'exécution des tâches à chaque tick.
    """

    def __init__(self):
        self.tasks: List[ScheduledTask] = []

    def add_task(
        self,
        name: str,
        callback: Callable,
        priority: Priority = Priority.NORMAL,
        args: List[Any] = None,
        kwargs: Dict[str, Any] = None
    ):
        """Ajoute une tâche à l'ordonnanceur."""
        task = ScheduledTask(
            name=name,
            callback=callback,
            priority=priority,
            args=args or [],
            kwargs=kwargs or {}
        )
        self.tasks.append(task)
        self._sort_tasks()

    def remove_task(self, name: str):
        """Retire une tâche de l'ordonnanceur."""
        self.tasks = [t for t in self.tasks if t.name != name]

    def enable_task(self, name: str):
        """Active une tâche."""
        for task in self.tasks:
            if task.name == name:
                task.enabled = True

    def disable_task(self, name: str):
        """Désactive une tâche."""
        for task in self.tasks:
            if task.name == name:
                task.enabled = False

    def execute_all(self):
        """Exécute toutes les tâches activées selon leur priorité."""
        results = {}
        for task in self.tasks:
            if task.enabled:
                results[task.name] = task.execute()
        return results

    def _sort_tasks(self):
        """Trie les tâches par priorité."""
        self.tasks.sort(key=lambda t: t.priority.value)

    def get_task_count(self) -> int:
        """Retourne le nombre de tâches actives."""
        return len([t for t in self.tasks if t.enabled])

    def clear(self):
        """Supprime toutes les tâches."""
        self.tasks.clear()
