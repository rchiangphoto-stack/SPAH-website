"""
SPAH Blog AI Detection Checker
================================
Extracts prose text from batch-4 blog HTML files and submits to Sapling.ai API.
Reports AI probability scores so you can verify each post is below the threshold.

SETUP (one-time):
1. Sign up for a free account at https://sapling.ai  (no credit card required)
2. Go to https://sapling.ai/user/settings — copy your API key
3. Run once to save your key:
   python scripts/check_ai_detection.py --save-key YOUR_KEY_HERE

Then just run:
   python scripts/check_ai_detection.py

Optional: check a single post
   python scripts/check_ai_detection.py --file blog/pet-limping.html

Optional: override key on the command line
   python scripts/check_ai_detection.py --key YOUR_API_KEY

Results are printed to console and saved to scripts/ai_detection_results.txt
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

SAPLING_ENDPOINT = "https://api.sapling.ai/api/v1/aidetect"


# ── HTML -> plain text ─────────────────────────────────────────────────────────
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


# ── Sapling.ai API call ───────────────────────────────────────────────────────
def check_sapling(text, api_key):
    """
    Calls Sapling.ai AI detection API.
    Returns a dict:
      {
        "score":            float,      # 0-1, overall AI probability (1 = fully AI)
        "ai_sentences":     int,        # sentences scored >= 0.5
        "total_sentences":  int,
        "predicted_class":  str,        # "AI" | "MIXED" | "HUMAN"
        "error":            str|None
      }
    """
    payload = json.dumps({"key": api_key, "text": text}).encode("utf-8")
    req = urllib.request.Request(
        SAPLING_ENDPOINT,
        data=payload,
        headers={
            "Content-Type": "application/json",
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

    score = data.get("score", 0)
    sentence_scores = data.get("sentence_scores", [])

    # sentence_scores is a list of {"sentence": str, "score": float} dicts
    ai_sentences = [s for s in sentence_scores if s.get("score", 0) >= 0.5]

    if score >= 0.8:
        predicted_class = "AI"
    elif score >= 0.4:
        predicted_class = "MIXED"
    else:
        predicted_class = "HUMAN"

    return {
        "score":           score,
        "ai_sentences":    len(ai_sentences),
        "total_sentences": len(sentence_scores),
        "predicted_class": predicted_class,
        "error":           None,
    }


# ── Scoring display ───────────────────────────────────────────────────────────
def score_label(prob):
    """Return a text label + pass/fail indicator."""
    pct = prob * 100
    if pct < 20:
        return f"{pct:.1f}%  [VERY LOW - OK]"
    elif pct < 40:
        return f"{pct:.1f}%  [LOW - OK]"
    elif pct < 60:
        return f"{pct:.1f}%  [MODERATE - REVIEW]"
    elif pct < 80:
        return f"{pct:.1f}%  [HIGH - REWRITE]"
    else:
        return f"{pct:.1f}%  [VERY HIGH - REWRITE]"


def short_name(filepath):
    return os.path.basename(filepath).replace(".html", "")


# ── Main ──────────────────────────────────────────────────────────────────────
KEY_FILE_NAME = ".sapling_key"


def load_key(cli_key, root):
    """Return API key from CLI arg -> key file -> env var, in that order."""
    if cli_key:
        return cli_key.strip()

    key_path = os.path.join(root, "scripts", KEY_FILE_NAME)
    if os.path.exists(key_path):
        with open(key_path, encoding="utf-8") as f:
            key = f.read().strip()
        if key:
            return key

    env_key = os.environ.get("SAPLING_API_KEY", "").strip()
    if env_key:
        return env_key

    return None


def main():
    parser = argparse.ArgumentParser(description="SPAH AI Detection Checker (Sapling.ai)")
    parser.add_argument("--key",  default=None, help="Sapling.ai API key (or save to scripts/.sapling_key)")
    parser.add_argument("--file", default=None, help="Check a single HTML file instead of all batch-4")
    parser.add_argument("--root", default=None, help="Path to SPAH-website root (auto-detected if omitted)")
    parser.add_argument("--save-key", default=None, metavar="KEY",
                        help="Save this API key to scripts/.sapling_key and exit")
    args = parser.parse_args()

    # Locate project root
    if args.root:
        root = args.root
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root = os.path.dirname(script_dir)

    # --save-key: write key to file and exit
    if args.save_key:
        key_path = os.path.join(root, "scripts", KEY_FILE_NAME)
        with open(key_path, "w", encoding="utf-8") as f:
            f.write(args.save_key.strip())
        print(f"API key saved to: {key_path}")
        print("You can now run:  python scripts/check_ai_detection.py")
        return

    api_key = load_key(args.key, root)
    if not api_key:
        print("ERROR: No API key found.")
        print()
        print("To set up your key (one-time):")
        print("  1. Sign up free at https://sapling.ai  (no credit card needed)")
        print("  2. Go to https://sapling.ai/user/settings to copy your key")
        print("  3. Run: python scripts/check_ai_detection.py --save-key YOUR_KEY_HERE")
        print()
        sys.exit(1)

    files = [args.file] if args.file else [os.path.join(root, p) for p in BATCH_4_POSTS]

    lines = []
    header = f"SPAH AI Detection Report  --  {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    lines.append(header)
    lines.append("=" * len(header))
    lines.append(f"Using Sapling.ai API | Checking {len(files)} post(s)")
    lines.append("")

    print(header)
    print("=" * len(header))
    print()

    for filepath in files:
        if not os.path.exists(filepath):
            msg = f"[!] File not found: {filepath}"
            print(msg)
            lines.append(msg)
            continue

        name = short_name(filepath)
        print(f"Checking: {name} ...", end=" ", flush=True)

        text = extract_prose(filepath)
        if len(text) < 100:
            msg = f"  [!] Could not extract prose text from {name}"
            print(msg)
            lines.append(msg)
            continue

        # Truncate to ~5000 chars to stay within free-tier limits
        if len(text) > 5000:
            text = text[:5000]

        result = check_sapling(text, api_key)
        time.sleep(1.5)  # stay within free-tier rate limits

        if result.get("error"):
            msg = f"  ERROR -- {result['error']}"
            print(msg)
            lines.append(f"{name}: {msg}")
            continue

        score = result["score"]
        cls   = result["predicted_class"]
        ai_s  = result["ai_sentences"]
        tot_s = result["total_sentences"]

        row = (
            f"  {name}\n"
            f"    Class:           {cls}\n"
            f"    AI score:        {score_label(score)}\n"
            f"    AI sentences:    {ai_s} / {tot_s}\n"
        )
        print(f"done  [{cls} -- {score*100:.1f}%]")
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
