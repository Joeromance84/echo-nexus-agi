# --- EchoAI Module: pathfinder.py ---
# Layer: LOGIC / ALGORITHMIC / PATHFINDING
# Purpose: Finds optimal routes or logic flows in graph structures or conceptual spaces.

from typing import Dict, List, Optional
import heapq


class Pathfinder:
    """
    Simple shortest-path resolver using Dijkstra's algorithm.
    Can be used for routing logic flows, decision graphs, or symbolic state shifts.
    """

    def find_shortest_path(self, graph: Dict[str, Dict[str, float]], start: str, end: str) -> List[str]:
        queue = [(0, start, [])]
        visited = set()

        while queue:
            (cost, node, path) = heapq.heappop(queue)
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]

            if node == end:
                return path

            for neighbor, weight in graph.get(node, {}).items():
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path))

        return ["No path found"]