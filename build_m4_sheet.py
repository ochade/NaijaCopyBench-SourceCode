"""M4 first pass: decompose sampled responses into atomic claims for hand
verification. Stratified sample: 20 items per arm across A1, A3, A5, balanced
over the categories whose gold states the rule (single_hop, divergence,
summarization). Decomposition by gpt-4o-mini; verification is manual."""
import json, random, time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

random.seed(42)
ROOT = Path(__file__).resolve().parent
CATS = ["single_hop", "divergence", "summarization"]
PER_ARM = 20

gold = {g["item_id"]: g for g in (json.loads(l) for l in
        (ROOT/"data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}

# choose the SAME item ids for every arm so responses are comparable
pool = [i for i, g in gold.items()
        if g["category"] in CATS and g.get("gold_answer","").strip()
        and not g["gold_answer"].strip().lower().startswith(("they are","both","the annotator"))]
per_cat = PER_ARM // len(CATS)
sample_ids = []
for c in CATS:
    cids = [i for i in pool if gold[i]["category"] == c]
    sample_ids += random.sample(cids, min(per_cat + (PER_ARM % len(CATS)), len(cids)))
sample_ids = sample_ids[:PER_ARM]
print(f"sampled {len(sample_ids)} items:", sample_ids)

load_dotenv(ROOT/".env"); client = OpenAI()

def decompose(answer):
    p = ("Break the following answer into atomic factual claims - each a single "
         "verifiable statement. Return one claim per line, no numbering, no other "
         f"text.\n\nAnswer:\n{answer}")
    r = client.chat.completions.create(model="gpt-4o-mini-2024-07-18", temperature=0,
            messages=[{"role":"user","content":p}])
    return [c.strip("-• ").strip() for c in r.choices[0].message.content.split("\n") if c.strip()]

out = ROOT/"results/m4_verification_sheet.jsonl"
done = set()
if out.exists():
    done = {(json.loads(l)["arm"], json.loads(l)["item_id"])
            for l in out.read_text(encoding="utf-8").splitlines() if l.strip()}

rows_by_arm = {a: {r["item_id"]: r for r in
               (json.loads(l) for l in (ROOT/f"runs/{a}_responses_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
               for a in ["A1","A3","A5"]}

with open(out, "a", encoding="utf-8") as f:
    for arm in ["A1","A3","A5"]:
        for iid in sample_ids:
            if (arm, iid) in done: continue
            resp = rows_by_arm[arm].get(iid)
            if not resp: continue
            claims = decompose(resp["response"])
            f.write(json.dumps({
                "arm": arm, "item_id": iid, "category": gold[iid]["category"],
                "question": gold[iid].get("question",""),
                "gold_provision": gold[iid].get("gold_provision",""),
                "gold_answer": gold[iid].get("gold_answer",""),
                "response": resp["response"],
                "claims": claims,
                "verdicts": ["" for _ in claims],   # you fill: S / N / C
                "required_elements_present": "",     # you fill for summarization
            }, ensure_ascii=False) + "\n")
            f.flush()
            print(f"{arm} {iid}: {len(claims)} claims")
            time.sleep(0.2)

print("\nwrote", out)
print("Verdicts to assign per claim: S=supported  N=not supported  C=contradicted")
