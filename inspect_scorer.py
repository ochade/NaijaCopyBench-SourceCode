import json, importlib.util, inspect
from pathlib import Path

spec = importlib.util.spec_from_file_location("mc", "src/score/metrics_citation.py")
mc = importlib.util.module_from_spec(spec); spec.loader.exec_module(mc)
print("callables in metrics_citation:", [n for n,o in vars(mc).items() if callable(o) and not n.startswith("_")])
print()
for n, o in vars(mc).items():
    if callable(o) and not n.startswith("_") and o.__module__ == "mc":
        try: print(f"  {n}{inspect.signature(o)}")
        except (ValueError, TypeError): print(f"  {n}(...)")
