"""Generate the fine-tuning set for arm A2.

Two-pass: a question is generated from one provision, then an answer generated
from that provision in a separate call. Pairs not answerable from the provision
alone are discarded. Ten sections are withheld entirely as a memorisation probe.
"""
import json, random, time, sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent
MODEL = "gpt-4o-mini-2024-07-18"
random.seed(42)

secmap = json.loads((ROOT/"data/derived/section_map.json").read_text(encoding="utf-8"))
sections = {k: v for k, v in secmap.items() if k != "SCHEDULE"}

# hold out ten sections entirely: probe for memorisation vs generalisation
HELD_OUT = sorted(random.sample(sorted(sections), 10), key=int)
print("held out:", HELD_OUT)

train_secs = [s for s in sorted(sections, key=int) if s not in HELD_OUT]

load_dotenv(ROOT/".env"); client = OpenAI()
OUT = ROOT/"data/ft/ft_pairs.jsonl"
OUT.parent.mkdir(parents=True, exist_ok=True)

done = set()
if OUT.exists():
    done = {json.loads(l)["source_section"] + "|" + str(json.loads(l)["n"])
            for l in OUT.read_text(encoding="utf-8").splitlines() if l.strip()}
    print(f"resuming: {len(done)} pairs done")

PER_SECTION = 12      # 99 sections x 12 ~ 1200 pairs before discards

with open(OUT, "a", encoding="utf-8") as f:
    for si, sec in enumerate(train_secs, 1):
        body = sections[sec]["text"][:2500]
        title = sections[sec]["title"]
        if f"{sec}|{PER_SECTION-1}" in done:
            continue
        qprompt = (f"Here is section {sec} of the Nigerian Copyright Act 2022, titled "
                   f"\"{title}\":\n\n{body}\n\n"
                   f"Write {PER_SECTION} distinct questions that this section alone answers. "
                   "Write them in the everyday language a non-lawyer would use, not in "
                   "statutory language. Do not mention section numbers in the questions. "
                   "Return one question per line, no numbering, no other text.")
        try:
            qr = client.chat.completions.create(model=MODEL, temperature=0.7,
                    messages=[{"role":"user","content":qprompt}])
            questions = [q.strip("-• ").strip() for q in qr.choices[0].message.content.split("\n") if q.strip()]
        except Exception as e:
            print(f"s.{sec} question-gen FAILED: {e}"); continue

        for n, q in enumerate(questions[:PER_SECTION]):
            if f"{sec}|{n}" in done: continue
            aprompt = (f"Section {sec} of the Nigerian Copyright Act 2022, titled \"{title}\":\n\n"
                       f"{body}\n\nQuestion: {q}\n\n"
                       "Answer using only this provision. Cite it as s."
                       f"{sec}, with the subsection or paragraph where the provision has one. "
                       "If this provision alone does not answer the question, reply exactly: "
                       "NOT ANSWERABLE")
            try:
                ar = client.chat.completions.create(model=MODEL, temperature=0,
                        messages=[{"role":"user","content":aprompt}])
                a = ar.choices[0].message.content.strip()
            except Exception as e:
                print(f"  s.{sec} q{n} FAILED: {e}"); continue
            if a.upper().startswith("NOT ANSWERABLE"):
                continue
            f.write(json.dumps({"source_section": sec, "n": n,
                                "question": q, "answer": a}, ensure_ascii=False) + "\n")
            f.flush()
            time.sleep(0.15)
        print(f"[{si:3}/{len(train_secs)}] s.{sec} done")

pairs = [json.loads(l) for l in OUT.read_text(encoding="utf-8").splitlines() if l.strip()]
(ROOT/"data/ft/held_out_sections.json").write_text(json.dumps(HELD_OUT), encoding="utf-8")
print(f"\n{len(pairs)} pairs written to {OUT}")
print(f"held-out sections recorded: {HELD_OUT}")
