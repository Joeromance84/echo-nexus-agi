# --- EchoAI Module: optimizer.py ---
# Layer: LOGIC / ALGORITHMIC / OPTIMIZER
# Purpose: Provides core optimization strategies for decision-making and resource handling.

from typing import List, Any, Callable


class OptimizationEngine:
    """
    Selects and applies optimized logic paths to given data.
    Can be extended with smarter strategies (e.g. genetic, quantum-assisted).
    """

    def __init__(self):
        self.strategies = {
            "sort": self.sort_basic,
            "unique": self.remove_duplicates,
            "prioritize": self.priority_sort,
        }

    def run(self, data: List[Any], strategy: str = "sort") -> List[Any]:
        if strategy in self.strategies:
            return self.strategies[strategy](data)
        return self.sort_basic(data)  # Fallback to default

    def sort_basic(self, data: List[Any]) -> List[Any]:
        try:
            return sorted(data)
        except Exception as e:
            print(f"[Optimizer] Basic sort failed: {e}")
            return data

    def remove_duplicates(self, data: List[Any]) -> List[Any]:
        return list(dict.fromkeys(data))

    def priority_sort(self, data: List[Any], priority_fn: Callable = lambda x: x) -> List[Any]:
        try:
            return sorted(data, key=priority_fn)
        except Exception as e:
            print(f"[Optimizer] Priority sort failed: {e}")
            return data

    def register_strategy(self, name: str, func: Callable) -> None:
        self.strategies[name] = func