"""Self-Refine Iterative Critique Optimization Loop.
100% Python Standard Library.
"""

class SelfRefineOptimizer:
    """Self-Refine critique-and-refinement loop optimizing generated artifacts."""
    def __init__(self, max_iterations=3):
        self.max_iterations = max_iterations

    def refine(self, initial_output, critique_func, refine_func, quality_threshold=0.9):
        current = initial_output
        history = []

        for i in range(self.max_iterations):
            score, critique = critique_func(current)
            history.append({"iteration": i, "output": current, "score": score, "critique": critique})
            if score >= quality_threshold:
                break
            current = refine_func(current, critique)

        return current, history
