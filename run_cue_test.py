"""Cue test: does naming the jurisdiction in the system prompt suppress
displacement? Re-runs A3 on the 45 divergence items with a neutral prompt."""
import json, time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent
MODEL, ARM = "gpt-4o-mini-2024-07-18", "A3-neutral"

# original prompt names the Act; this one does not name any jurisdiction
NEUTRAL = ("You are a legal information assistant. Answer the question and cite "
           "the specific section of the relevant statute that supports your answer.")

items = [json.loads(l) for l in (ROOT/"data/eval/benchmark_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
div = [i for i in items if i["category"] == "divergence"]

load_dotenv(ROOT/".env")
client = OpenAI()
out = ROOT/"runs/A3_neutral_divergence.jsonl"
done = set()
if out.exists():
    done = {json.loads(l)["item_id"] for l in out.read_text(encoding="utf-8").splitlines() if l.strip()}
    print(f"resuming: {len(done)} done")

with open(out, "a", encoding="utf-8") as f:
    for n, it in enumerate(div, 1):
        if it["item_id"] in done: continue
        try:
            r = client.chat.completions.create(model=MODEL, temperature=0,
                messages=[{"role":"system","content":NEUTRAL},
                          {"role":"user","content":it["question"]}])
            f.write(json.dumps({"arm":ARM,"model":r.model,"item_id":it["item_id"],
                "category":it["category"],"response":r.choices[0].message.content,
                "tokens":r.usage.total_tokens}, ensure_ascii=False)+"\n")
            f.flush()
            print(f"[{n:2}/{len(div)}] {it['item_id']} ok")
        except Exception as e:
            print(f"[{n:2}/{len(div)}] {it['item_id']} FAILED: {e}")
        time.sleep(0.25)
print("\nwrote", out)
