from client import SelfRefineOptimizer

optimizer = SelfRefineOptimizer(max_iterations=4)

def critique_fn(code):
    has_doc = '"""' in code
    has_type = 'def ' in code and '->' in code
    score = (0.5 if has_doc else 0.0) + (0.5 if has_type else 0.0)
    critique = []
    if not has_doc: critique.append("Add docstring")
    if not has_type: critique.append("Add return type annotations")
    return score, "; ".join(critique) if critique else "Code is well formatted"

def refine_fn(code, crit):
    res = code
    if "docstring" in crit:
        res = '"""Calculates output."""\n' + res
    if "return type" in crit:
        res = res.replace("def compute(x):", "def compute(x) -> float:")
    return res

draft = "def compute(x): return x * 2.0"
best, history = optimizer.refine(draft, critique_fn, refine_fn, quality_threshold=0.95)
print(f"Final output after {len(history)} revisions:\n{best}")
