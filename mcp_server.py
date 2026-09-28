import sys
import json
from client import SelfRefineOptimizer

optimizer = SelfRefineOptimizer(max_iterations=3)

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "self_refine_loop",
                        "description": "Execute Self-Refine critique and revision cycle on text draft",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "draft": {"type": "string"},
                                "target_min_length": {"type": "integer", "default": 20}
                            },
                            "required": ["draft"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "self_refine_loop":
            d = args["draft"]
            min_len = args.get("target_min_length", 20)
            def critique(text):
                score = 1.0 if len(text) >= min_len else (len(text) / min_len)
                crit = "Meets length criteria" if score >= 1.0 else "Expand explanation with more context"
                return score, crit
            def refine(text, crit):
                return text + " [elaborated detail]"
            best, hist = optimizer.refine(d, critique, refine, quality_threshold=0.99)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"final_result": best, "iterations": len(hist), "history": hist})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
