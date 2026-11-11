#!/usr/bin/env python3
"""Reads a log.txt from the 3DS (UZDoom, and other ports that use the same format) and
prints a short summary, so the analysis starts from facts and not from 400 raw lines.

    python3 analiza-log.py log.txt [uzdoom-pruebaNN.elf] [--addr2line PATH]

With the ELF of the SAME test, every address in the log is turned into function and line.

Summary:
  - which test and commit the log comes from (line "Test:");
  - the last lines reached (where it stopped);
  - the heap in use along the log (the [KB] at the start of each line), with its peak;
  - large allocations and failures, with their callers resolved;
  - FATAL lines, [C3D] lines (backend diagnostics), GPU HANG;
  - odd lines (bytes that are not text, lines glued together).
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

ADDR = re.compile(r"\b(00[0-9a-f]{6})\b")


def find_addr2line(explicit):
    if explicit:
        return explicit
    for cand in ("arm-none-eabi-addr2line",
                 "/opt/devkitpro/devkitARM/bin/arm-none-eabi-addr2line"):
        if shutil.which(cand) or os.path.exists(cand):
            return cand
    return None


def resolve(addr2line, elf, addrs):
    if not addrs:
        return {}
    out = subprocess.run([addr2line, "-f", "-C", "-e", elf] + ["0x" + a for a in addrs],
                         capture_output=True, text=True).stdout.splitlines()
    res = {}
    for i, a in enumerate(addrs):
        func = out[2 * i] if 2 * i < len(out) else "?"
        loc = out[2 * i + 1] if 2 * i + 1 < len(out) else "?"
        loc = re.sub(r".*/(src|libraries)/", r"\1/", loc)
        loc = re.sub(r".*/include/c\+\+/[^/]+/", "c++/", loc)
        if len(func) > 70:
            func = func[:67] + "..."
        res[a] = f"{func} @ {loc}"
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("log")
    ap.add_argument("elf", nargs="?")
    ap.add_argument("--addr2line")
    ap.add_argument("--tail", type=int, default=12, help="last lines to show (12)")
    args = ap.parse_args()

    raw = open(args.log, "rb").read()
    text = raw.decode("utf-8", errors="replace")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    print(f"== {args.log}: {len(lines)} lines, {len(raw)} bytes")

    test = [l for l in lines[:6] if l.startswith("Test:")]
    print("Test:", test[0][5:].strip() if test else "NOT SAYING (built without build-test.sh: the code it ran is unknown)")
    build = [l for l in lines[:12] if l.startswith("Build:") or "for Nintendo 3DS" in l]
    for b in build:
        print("  " + b.strip())

    # Heap (and, from test 31 on, elapsed time) along the log.
    # Old prefix: "[ 13226] text" (heap KB). New: "[T+  1234  heap=13226KB] text".
    heap, timed = [], []
    for i, l in enumerate(lines):
        m = re.match(r"\[T\+\s*(\d+)\s+heap=\s*(\d+)KB\]\s?(.*)", l)
        if m:
            heap.append((i + 1, int(m.group(2))))
            timed.append((int(m.group(1)), m.group(3).strip(), i + 1))
            continue
        m = re.match(r"T\+(\d+) ms: (.*)", l)
        if m:
            timed.append((int(m.group(1)), m.group(2).strip(), i + 1))
            continue
        m = re.match(r"\[\s*(\d+)\]", l)
        if m:
            heap.append((i + 1, int(m.group(1))))
    if heap:
        peak = max(heap, key=lambda x: x[1])
        print(f"Heap in use: start {heap[0][1]} KB, end {heap[-1][1]} KB, peak {peak[1]} KB (line {peak[0]})"
              f" of 72184 KB")

    # Load phases: time between consecutive timed lines, slowest first.
    if timed:
        timed.sort(key=lambda t: (t[0], t[2]))
        total = timed[-1][0]
        phases = []
        for (t0, txt0, n0), (t1, txt1, n1) in zip(timed, timed[1:]):
            phases.append((t1 - t0, txt0, n0))
        phases.sort(reverse=True)
        print(f"-- load phases (from the T+ms marks; last mark at {total / 1000:.1f} s)")
        print("   (each row: time from that line until the next timed line; [T+...] is ms, heap= is KB)")
        for dt, txt, n in phases[:10]:
            pct = 100.0 * dt / total if total else 0
            print(f"  {dt / 1000:7.1f} s {pct:5.1f}%  line {n}: {txt[:90]}")
        print("   If this total does not match what Alex timed on the console, find out why before concluding.")
    else:
        print("-- no T+ms marks: this log cannot tell times (the [N] prefix is heap KB, not time)")

    # Milestones.
    marks = ["Init complete", "V_Init", "C3D: backend ready", "StartScreen", "D_DoomLoop", "Exit:"]
    for mk in marks:
        hit = [i + 1 for i, l in enumerate(lines) if mk in l]
        print(f"  {'yes' if hit else 'no ':3} {mk}" + (f" (line {hit[0]})" if hit else ""))

    # Interesting lines.
    def show(title, pred, limit=40):
        sel = [(i + 1, l) for i, l in enumerate(lines) if pred(l)]
        if sel:
            print(f"-- {title} ({len(sel)})")
            for n, l in sel[:limit]:
                print(f"  {n:5}: {l[:220]}")
            if len(sel) > limit:
                print(f"  ... {len(sel) - limit} more")
    show("FATAL / errors", lambda l: "FATAL" in l or "FAILED" in l or "rror" in l)
    show("GPU HANG", lambda l: "GPU HANG" in l)
    show("[C3D] diagnostics", lambda l: l.startswith("[C3D]"), 60)
    if any(re.match(r"\[C3D\] frame \d+:", l) for l in lines):
        print("   NOTE: [C3D] frame summaries cover only the first 12 frames and draw details the first 8 draws:"
              " anything later does not appear, so its absence proves nothing (hechos-3ds.md, T3).")
    show("odd lines (non-text bytes or glued markers)",
         lambda l: "�" in l or re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", l) or l.count("TEST") > 1, 10)

    # Addresses.
    if args.elf:
        a2l = find_addr2line(args.addr2line)
        if not a2l:
            print("!! arm-none-eabi-addr2line not found: install devkitARM or pass --addr2line")
        else:
            traced = [(i + 1, l) for i, l in enumerate(lines) if "malloc" in l or "alloc" in l or "PC" in l or "LR" in l]
            addrs = sorted({a for _, l in traced for a in ADDR.findall(l)})
            res = resolve(a2l, args.elf, addrs)
            seen = set()
            print(f"-- callers of large allocations and failures (ELF {os.path.basename(args.elf)})")
            for n, l in traced:
                key = tuple(ADDR.findall(l))
                if not key or key in seen:
                    continue
                seen.add(key)
                print(f"  line {n}: {l.split(':')[0][:60]}")
                for a in key[:8]:
                    print(f"      {a}  {res.get(a, '?')}")
    else:
        print("(no ELF given: addresses not resolved)")

    print(f"-- last {args.tail} lines (where it stopped)")
    for l in lines[-args.tail:]:
        print("  " + l[:220])


main()
