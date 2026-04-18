"""
SPAH Blog AI Detection Checker
================================
Extracts prose text from batch-4 blog HTML files and submits to GPTZero API.
Reports AI probability scores so you can verify each post is below the threshold.

SETUP:
1. Get a free API key at https://gptzero.me  (Settings → API)
2. Run:  python scripts/check_ai_detection.py --key YOUR_API_KEY

Optional: check a single post
   python scripts/check_ai_detection.py --key YOUR_API_KEY --file blog/pet-limping.html

Results are printed to console and saved to scripts\ai_detection_results.txt
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from html.parser import HTMLParser


# ── Blog posts to check ──────────────────────────────────────────────────────
BATCH_4_POSTS = [
    "blog/pet-vomiting-diarrhea.html",
    "blog/pet-limping.html",
    "blog/pet-lethargy.html",
    "blog/pet-fever.html",
    "blog/pet-skin-rashes.html",
    "blog/pet-eye-ear-problems.html",
    "blog/pet-coughing-sneezing.html",
    "blog/pet-wounds-cuts.html",
    "blog/cat-dog-urinary-problems.html",
    "blog/dog-urinary-problems.html",
    "blog/pet-euthanasia-guide.html",
]

GPTZERO_ENDPOINT = "https://api.gptzero.me/v2/predict/text"


# ── HTML → plain text ─────────────────────────────────────────────────────────
class ProseExtractor(HTMLParser):
    """Extracts text from inside <div class="prose"> ... </div>."""

    def __init__(self):
        super().__init__()
        self.in_prose = False
        self.depth = 0
        self.chunks = []
        self._skip_tags = {"script", "style", "nav", "footer", "header"}
        self._current_skip = 0

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "div" and "prose" in attr_dict.get("class", ""):
            self.in_prose = True
            self.depth = 0
        if self.in_prose:
            if tag == "div":
                self.depth += 1
            if tag in self._skip_tags:
                self._current_skip += 1

    def handle_endtag(self, tag):
        if tag in self._skip_tags and self._current_skip > 0:
            self._current_skip -= 1
        if self.in_prose and tag == "div":
            self.depth -= 1
            if self.depth <= 0:
                self.in_prose = False

    def handle_data(self, data):
        if self.in_prose and self._current_skip == 0:
            text = data.strip()
            if text:
                self.chunks.append(text)

    def get_text(self):
        raw = " ".join(self.chunks)
        # collapse multiple spaces / newlines
        raw = re.sub(r"\s+", " ", raw).strip()
        return raw


def extract_prose(filepath):
    with open(filepath, encoding="utf-8") as f:
        html = f.read()
    parser = ProseExtractor()
    parser.feed(html)
    text = parser.get_text()
    return text


# ── GPTZero API call ──────────────────────────────────────────────────────────
def check_gptzero(text, api_key):
    """
    Returns a dict:
      {
        "completely_generated_prob": float,   # 0–1, probability entire doc is AI
        "average_generated_prob":   float,    # average sentence-level AI probability
        "ai_sentences":             int,      # count of sentences flagged as AI
        "total_sentences":          int,
        "predicted_class":          str,      # "ai" | "mixed" | "human"
        "error":                    str|None
      }
    """
    payload = json.dumps({"document": text}).encode("utf-8")
    req = urllib.request.Request(
        GPTZERO_ENDPOINT,
        data=payload,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}: {body[:200]}"}
    except Exception as e:
        return {"error": str(e)}

    doc = data.get("documents", [{}])[0]
    sentences = doc.get("sentences", [])
    ai_sentences = [s for s in sentences if s.get("generated_prob", 0) >= 0.5]

    return {
        "completely_generated_prob": doc.get("completely_generated_prob", 0),
        "average_generated_prob":    doc.get("average_generated_prob", 0),
        "ai_sentences":              len(ai_sentences),
        "total_sentences":           len(sentences),
        "predicted_class":           doc.get("predicted_class", "unknown"),
        "error":                     None,
    }


# ── Scoring display ───────────────────────────────────────────────────────────
def score_label(prob):
    """Return a text label + pass/fail indicator."""
    pct = prob * 100
    if pct < 20:
        return f"{pct:.1f}%  ✅ VERY LOW"
    elif pct < 40:
        return f"{pct:.1f}%  ✅ LOW"
    elif pct < 60:
        return f"{pct:.1f}%  ⚠️  MODERATE"
    elif pct < 80:
        return f"{pct:.1f}%  ❌ HIGH"
    else:
        return f"{pct:.1f}%  ❌ VERY HIGH"


def short_name(filepath):
    return os.path.basename(filepath).replace(".html", "")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="SPAH AI Detection Checker (GPTZero)")
    parser.add_argument("--key",  required=True, help="GPTZero API key (free at gptzero.me)")
    parser.add_argument("--file", default=None,  help="Check a single HTML file instead of all batch-4")
    parser.add_argument("--root", default=None,  help="Path to SPAH-website root (auto-detected if omitted)")
    args = parser.parse_args()

    # Locate project root
    if args.root:
        root = args.root
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root = os.path.dirname(script_dir)

    files = [args.file] if args.file else [os.path.join(root, p) for p in BATCH_4_POSTS]

    lines = []
    header = f"SPAH AI Detection Report  —  {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    lines.append(header)
    lines.append("=" * len(header))
    lines.append(f"Using GPTZero API | Checking {len(files)} post(s)")
    lines.append("")

    print(header)
    print("=" * len(header))
    print()

    for filepath in files:
        if not os.path.exists(filepath):
            msg = f"⚠️  File not found: {filepath}"
            print(msg)
            lines.append(msg)
            continue

        name = short_name(filepath)
        print(f"Checking: {name} …", end=" ", flush=True)

        text = extract_prose(filepath)
        if len(text) < 100:
            msg = f"  ⚠️  Could not extract prose text from {name}"
            print(msg)
            lines.append(msg)
            continue

        # Truncate to GPTZero free-tier limit (~5000 chars) if needed
        if len(text) > 5000:
            text = text[:5000]

        result = check_gptzero(text, args.key)
        time.sleep(1.2)  # stay within free-tier rate limits

        if result.get("error"):
            msg = f"  ERROR — {result['error']}"
            print(msg)
            lines.append(f"{name}: {msg}")
            continue

        cg  = result["completely_generated_prob"]
        avg = result["average_generated_prob"]
        cls = result["predicted_class"].upper()
        ai_s  = result["ai_sentences"]
        tot_s = result["total_sentences"]

        row = (
            f"  {name}\n"
            f"    Class:           {cls}\n"
            f"    Doc AI score:    {score_label(cg)}\n"
            f"    Avg sentence:    {score_label(avg)}\n"
            f"    AI sentences:    {ai_s} / {tot_s}\n"
        )
        print(f"done  [{cls} — {cg*100:.1f}%]")
        lines.append(row)

    # Save results
    out_path = os.path.join(root, "scripts", "ai_detection_results.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print()
    print(f"Results saved to: {out_path}")
    print()
    for l in lines[3:]:
        print(l)


if __name__ == "__main__":
    main()
