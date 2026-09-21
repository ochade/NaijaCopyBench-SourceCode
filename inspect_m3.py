import json
print("=== responses flagged on the marker 'enforceable' ===\n")
for a in ["A1","A3","A5"]:
    for s in (json.loads(l) for l in open(f"results/{a}_m3_180.jsonl", encoding="utf-8")):
        if "enforceable" in s.get("markers_hit", []):
            print(f"{a}  {s['item_id']}")
            print("  ", s["response"][:300].replace("\n", " "))
            print()

print("\n=== what the models actually wrote on four divergence items ===\n")
r = [json.loads(l) for l in open("runs/A3_responses_180.jsonl", encoding="utf-8")]
for i in ["NCB-C-006", "NCB-C-015", "NCB-C-028", "NCB-C-016"]:
    x = [y for y in r if y["item_id"] == i][0]
    print("="*72)
    print(i)
    print(x["response"][:420].replace("\n", " "))
    print()
