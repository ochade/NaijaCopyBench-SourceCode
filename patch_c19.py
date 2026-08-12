from pathlib import Path
p = Path("src/build_catC.py")
t = p.read_text(encoding="utf-8")
before = t
t = t.replace(
 '"We produce accessible-format books in Nigeria and a partner organisation in Ghana wants copies. Under Nigerian law, may we send them?"',
 '"We are a registered non-profit in Nigeria producing braille books for blind readers. A similar registered non-profit in Ghana that serves blind readers wants copies. Under Nigerian law, may we send them?"'
)
t = t.replace(
 '"We have an out-of-print book and cannot trace the copyright owner despite real effort. Under Nigerian law, can the library copy it?"',
 '"Our library has an out-of-print book. We wrote twice to the last known publisher and searched the Commission register, with no result. Under Nigerian law, can we copy it?"'
)
p.write_text(t, encoding="utf-8")
print("changed:", t != before)
