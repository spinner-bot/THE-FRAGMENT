#!/usr/bin/env python3
"""Build 《THE FRAGMENT·残卷》解谜全书.html from docs/solution/*.md.

The output is a single, self-contained HTML file: no external fonts,
scripts, stylesheets, or images. All diagrams are inline SVG.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "solution"
TEMPLATE = Path(__file__).resolve().parent / "book" / "template.html"
OUT = ROOT / "《THE FRAGMENT·残卷》解谜全书.html"


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

PARTS = [
    dict(
        key="p0", num="0", kicker="PART 0 · ORIENTATION", en="Orientation", zh="导读",
        file="part-01-overview.md",
        prose_en="A map is not the territory, but it can teach you how to stand. Before the "
                 "first archive is opened, this book draws the shape of the whole descent: "
                 "three outer locks, five data questions, and the single chain of answers "
                 "that connects them.",
        prose_zh="地图不是疆域，但它能教会你如何站立。在第一层压缩包被打开之前，"
                 "这本书先画出整段下行的形状：三道外锁、五道数据题，以及把它们串起来的那一条答案链。",
    ),
    dict(
        key="p1", num="I", kicker="PART I · THE THRESHOLD", en="The Threshold", zh="入口与 P1",
        file="part-02-entry.md",
        prose_en="Every descent begins with a door that looks like ordinary packaging. "
                 "Here the door is a ZIP, a cover page, a manual that tells the truth and "
                 "does not, and a first answer so simple it feels like a kindness.",
        prose_zh="每一次下行，都从一扇看起来像普通包装的门开始。这里的门是一层 ZIP、"
                 "一页封面、一份既说真话又不完全说真话的说明书，以及一个简单得近乎善意的第一答案。",
    ),
    dict(
        key="p2", num="II", kicker="PART II · THE SELF-DESCRIBING LOCK", en="The Self-Describing Lock", zh="自描述锁 ITC2RECIPE",
        file="part-03-lock.md",
        prose_en="The lock does not hide its grammar. It writes the grammar on its own face, "
                 "then dares you to notice that the first line is both the name of the door "
                 "and the key that opens it.",
        prose_zh="这把锁并不隐藏自己的语法。它把语法写在自己的脸上，然后看你是否会发现："
                 "第一行既是门的名字，也是开门的那把钥匙。",
    ),
    dict(
        key="p3", num="III", kicker="PART III · THE SHIT LAYER", en="The SHIT Layer", zh="P2：SHIT 层",
        file="part-04-p2.md",
        prose_en="Q2 is where the package begins to lie in earnest. A container named after "
                 "refusal, a readable noise, a bitmap that is not an image: the surface "
                 "insults the reader while the mathematics waits underneath.",
        prose_zh="Q2 是包裹开始认真说谎的地方。一个以拒绝命名的容器、一段可读的噪音、"
                 "一张并不是图像的位图：表层在冒犯读者，而数学在下面等待。",
    ),
    dict(
        key="p4", num="IV", kicker="PART IV · THE NESTED LABYRINTH", en="The Nested Labyrinth", zh="P3 与嵌套结构",
        file="part-05-p3.md",
        prose_en="The labyrinth is made of names, not walls. P1-02C opens into B, B into A, "
                 "and A into two objects that pull the reader toward different kinds of ending.",
        prose_zh="迷宫由名字构成，而不是由墙构成。P1-02C 打开 B，B 打开 A，"
                 "A 再分成两个物件，把读者拉向不同种类的结局。",
    ),
    dict(
        key="p5", num="V", kicker="PART V · FIVE DATA QUESTIONS", en="Five Data Questions", zh="五题数据挑战",
        file="part-06-five-questions.md",
        prose_en="Five questions, five shapes. One counts triangles, one counts Fibonacci "
                 "lengths, one alternates increments, one writes its formula plainly, and "
                 "the last refuses to be answered by arithmetic alone.",
        prose_zh="五道题，五种形状。一道数三角，一道数 Fibonacci 长度，一道交替增量，"
                 "一道把公式直接写出，最后一道则拒绝只被算术回答。",
    ),
    dict(
        key="p6", num="VI", kicker="PART VI · REVERSE ENGINEERING Q5", en="Reverse Engineering Q5", zh="第 5 题逆向工程",
        file="part-07-q5.md",
        prose_en="The last question looks like weather: five hundred rows of numbers, "
                 "small local changes, a pattern that seems to move. It is not weather. "
                 "It is an index wearing the costume of a dynamical system.",
        prose_zh="最后一题看起来像天气：五百行数字、微小的局部变化、一种似乎在流动的模式。"
                 "它不是天气。它是一个索引，穿着动力系统的外衣。",
    ),
    dict(
        key="p7", num="VII", kicker="PART VII · AFTER THE SOLVE", en="After the Solve", zh="复盘与设计",
        file="part-08-review.md",
        prose_en="After the answer, the structure remains. This is the part where the book "
                 "turns around: what the solver saw, what the model missed, what the hints "
                 "actually bought, and why difficulty was never only mathematical.",
        prose_zh="答案之后，结构仍然留下。这是全书转身的部分：解题者看见了什么，"
                 "模型错过了什么，提示究竟买到了什么，以及为什么难度从来不只是数学。",
    ),
]

APPENDICES = [
    dict(id="appendix-a", letter="A", file="appendix-a-files.md",
         en="Complete File Tree and SHA-256", zh="完整文件树与 SHA-256",
         abstract="Every artifact, its size, its hash, and the audit table that shows where it is discussed."),
    dict(id="appendix-b", letter="B", file="appendix-b-decryptor.md",
         en="A Minimal Decryptor", zh="最小解密器",
         abstract="A standard-library decryptor, its usage, and test vectors for both outer locks."),
    dict(id="appendix-c", letter="C", file="appendix-c-p2-math.md",
         en="P2 Fast Exponentiation", zh="P2 快速幂计算",
         abstract="The closed form of the affine recurrence, the constants, and the computation of K."),
    dict(id="appendix-d", letter="D", file="appendix-d-q5-generator.md",
         en="Deobfuscated Q5 Generator", zh="第 5 题生成器去混淆版",
         abstract="The generator behind Q5, deobfuscated and verified against all five hundred output rows."),
    dict(id="appendix-e", letter="E", file="appendix-e-answers.md",
         en="Five Answers at a Glance", zh="五题答案速查",
         abstract="The five answers, their formulas, and the decoy files that impersonate them."),
    dict(id="appendix-f", letter="F", file="appendix-f-index.md",
         en="Archive Index and Glossary", zh="归档索引与术语表",
         abstract="The archive index, repository presentation layer, tooling, and the shared vocabulary of the book."),
]

PART_ROMAN = {"p0": "0", "p1": "I", "p2": "II", "p3": "III", "p4": "IV",
              "p5": "V", "p6": "VI", "p7": "VII", "p8": "A–F"}
PART_BY_FILE = {p["file"]: p for p in PARTS}
APPENDIX_BY_FILE = {a["file"]: a for a in APPENDICES}

CHAPTER_META = {
    1: ("What This Book Is",
        "A solution manual that is also a map: what it covers, who it is for, and how to read it without losing the thread."),
    2: ("The Whole Package on One Page",
        "The entire package at a glance: layers, answer chain, five stages, and the two tracks of exploration order and file structure."),
    3: ("Terms and Symbols",
        "The vocabulary of the lock: P and Q, recipe, payload, TAG, D and K, and the difference between a key and an answer."),
    4: ("The Master Route",
        "The decision tree from the first ZIP byte to the Q5 generator, with the shortest path and the main forks marked."),
    5: ("release/THE FRAGMENT.zip: Two Layers, Seven Pieces",
        "The outer archive is not a wrapper but a first puzzle: two layers, seven pieces, and an entry order that matters."),
    6: ("incipit: The Cover as Chapter Zero",
        "The cover is chapter zero: a readable surface that sets the tone and quietly explains how to stand before the fragment."),
    7: ("Let's go.7z and instruction.gz: The Manual Layer",
        "The action pack opens into four objects, each demanding a different operation; instruction.gz is the manual layer."),
    8: ("The Grammar of Truth and Lie in the Manual",
        "The manual mixes true rules with false certainty. R1–R6 and W1–W5 form a grammar of trust."),
    9: ("P1: 5050 and Answer Normalization",
        "P1 is deliberately simple: the sum 1..100, answer normalization, and the first handoff to a lock."),
    10: ("ITC2RECIPE: How a File Describes Itself",
         "ITC2RECIPE is a file that describes its own decryption: marker, recipe, body, and the idea of a self-describing lock."),
    11: ("Marker and Recipe: The Reversibility of XOR",
         "The first line is both magic and key; the second line is ciphertext that becomes a recipe under a repeating XOR."),
    12: ("Body: Framing base64, CIPHER, and TAG",
         "Base64 is only the envelope. The body splits into CIPHER and a sixteen-byte TAG, with all the framing rules that follow."),
    13: ("Key Derivation: S = SHA-256(ASCII(D))",
         "The answer becomes a key through SHA-256. Decimal formatting is part of the protocol."),
    14: ("The Block Stream: SHA-256(S ‖ uint64_be(i))",
         "CIPHER is encrypted in thirty-two-byte blocks by a SHA-256 stream keyed with S and a big-endian counter."),
    15: ("Verification: Encrypt-then-MAC",
         "Encrypt-then-MAC: verify the TAG before touching the plaintext, and never trust a failed check."),
    16: ("A Minimal Decryptor from Scratch",
         "A complete standard-library decryptor, explained line by line, with the pitfalls that break naive implementations."),
    17: ("Design Assessment: Why Not a 7z Password",
         "Why the package does not use a 7z password: security is not the goal; readable structure is."),
    18: ("Q2.zst: zstd and the First Lock",
         "Q2 arrives as zstd, not 7z. The first lock is a text file wearing the wrong extension."),
    19: ("Opening Q2 with 5050",
         "5050 opens the first lock. The TAG confirms the answer before the payload appears."),
    20: ("Q2 Payload: SHIT.tar.xz and map.bmp",
         "Inside Q2: a SHIT container, a fake bitmap, and two files that pull in opposite directions."),
    21: ("SHIT.README: Readable Noise",
         "SHIT.README is readable noise: corrupted spelling, contradictory instructions, and a few real clues buried in atmosphere."),
    22: ("SHIT.bz2: The Real Prompt",
         "SHIT.bz2 is the actual mathematical prompt: an affine recurrence with a misleading parameter sheet."),
    23: ("Affine Recurrence: From 10^18 Steps to One Power",
         "An affine map iterated ten to the eighteenth collapses into one modular exponentiation."),
    24: ("Computing K: A 77-Digit Integer",
         "K is a seventy-seven-digit answer and a 255-bit key; the arithmetic, the constants, and the moment the lock accepts it."),
    25: ("Independent Verification of K and the Handoff",
         "Independent verification: alternate derivations, TAG checks, and the handoff from Q2 to Q3."),
    26: ("Q3.7z: README and Lock",
         "Q3.7z contains a short README and a large text lock with a rhetorical filename."),
    27: ("Opening Q3 with K",
         "K opens Q3. What emerges is not the final question but a score table and another nested archive."),
    28: (".entrance: The Score Table Line by Line",
         ".entrance is a static text that behaves like a program: six checkpoints, six scores, and a grade ladder."),
    29: ("The Scoring Function: 60 + k(k+1)/2",
         "The progress score is sixty plus the k-th triangular number for the first five checkpoints, then a deliberate jump to one hundred."),
    30: ("Why B Is Unreachable: Reachable Grades",
         "Under checkpoint scoring, B and A are unreachable; only D, C and A+ can be reached."),
    31: ("The Hint Economy: F, Invalid, Unavailable",
         "Hints are an economy: base prices rise by two, yes/no questions are discounted, and invalid questions refund."),
    32: ("P1-02C → P1-02B: base64 Text Disguise",
         "P1-02C opens into P1-02B, a base64 text pretending to be the next stage; naming runs backwards."),
    33: ("P1-02A: content.tar and README.7z",
         "P1-02A splits into content.tar and README.7z: one leads to the questions, the other to a manifesto."),
    34: ("The 31-Digit Directory Name and README.json Codepoints",
         "A thirty-three-character directory name encodes ten to the thirtieth plus one and a half; README.json hides a long text in codepoints."),
    35: ("prompt.7z and puzzle.7z: The Original Five Questions",
         "prompt.7z and puzzle.7z deliver the original five-question challenge and its data."),
    36: ("Data Format and Parser",
         "The data format is deceptively simple: bracketed index and content, tolerant parsing, and five different shapes."),
    37: ("Question 1: Triangular Blocks",
         "Q1 is triangular blocking: row n has n consecutive integers."),
    38: ("Question 2: Fibonacci Lengths and Period ±1",
         "Q2 combines Fibonacci row lengths with a period-five sign pattern."),
    39: ("Question 3: Quadratic Blocks with Alternating Increments",
         "Q3 grows by quadratic row starts and alternating increments."),
    40: ("Question 4: Explicit Formula and Answer File",
         "Q4 has an explicit formula and a decoy answer file; the formula is the answer."),
    41: ("Question 5: Why It Is the Endpoint",
         "Q5 is the endpoint because it asks for a program, not a pattern."),
    42: ("The Difficulty Curve and Design Intent",
         "The difficulty curve is designed: observe, decompose, recurse, verify, reverse-engineer."),
    43: ("Data Shape: 500 Rows, 12 Fields, Negative Runs",
         "Q5's surface: five hundred rows, two to twelve raw fields, negative run lengths, and a fixed sparse support."),
    44: ("First Restoration: The Sparse Array",
         "Expand the negative runs and the data becomes an eighteen-wide sparse matrix with eight live buckets."),
    45: ("Triangular Encoding",
         "Every nonzero value is a triangular encoding of a group's count and sum."),
    46: ("Collatz Count C(n) and round R(n)",
         "The bucket key is not C(n) but R(n), obtained by applying C to C(n) exactly C(n) minus one times."),
    47: ("The Control Flow of calc: Three Recursive Branches",
         "calc compresses four phases into one recursive conditional: collect, summarize, encode, and compress."),
    48: ("Group Statistics and “Only One Column Changes”",
         "Each row changes exactly one bucket; the four hundred ninety-nine updates form two hundred fifty-one runs, not the older count."),
    49: ("Reverse Engineering from Data: Differences, Square Roots, Triangular Numbers, Buckets",
         "A data-only route: differences, square roots, triangular decoding, and the discovery of Collatz."),
    50: ("The Correct Model: Index-Driven, Not Dynamic",
         "The correct model is index-driven: row n depends only on n, not on row n minus one."),
    51: ("ChatGPT's Two Conversations: Timeline and Phases",
         "Two conversations, seven phases, and the long detour through statistical modelling."),
    52: ("The Key Error: Mistaking Statistical Fit for Mechanism",
         "Why precise local patterns can still mislead: fit describes output, not mechanism."),
    53: ("The Information Theory of the Hint System",
         "What seven hints actually bought: exclusions, meta-information, and a shrinking budget."),
    54: ("If We Started Over: The Shortest Path",
         "The shortest route through the package, layer by layer, with the main forks marked."),
    55: ("Designer's Retrospective: Structure Is Difficulty",
         "Structure as difficulty, decoys as content, and the last jump from C to A+."),
}

PROLOGUE = [
    ("I",
     "There is a kind of book that cannot be read from the beginning. It arrives after the event, "
     "when the seal is already broken and the first answer has already been spoken. What remains is "
     "not the original whole but the path through its pieces. This is that kind of book.",
     "有一种书无法从头读起。它在事件之后才到来，封印已经破裂，第一个答案已经被说出。"
     "留下来的不是原来的整体，而是穿过其碎片的那条路径。这本书就是这样的书。"),
    ("II",
     "The fragment does not ask to be restored. It asks to be read. A torn page is not a failed page; "
     "the tear is part of the instruction. The missing half tells you where to look, and the surviving "
     "half tells you what kind of thing you are looking for.",
     "残卷并不要求被复原。它要求被阅读。撕裂的一页不是失败的一页；裂口本身就是说明的一部分。"
     "缺失的那一半告诉你该往哪里看，幸存的那一半告诉你，你要找的是怎样一种东西。"),
    ("III",
     "This package was built around a single wager: that a lock can describe itself. Not merely store "
     "a key, not merely hide a payload, but write its own grammar on its face and trust the reader to "
     "notice. The first line of the file is the name of the door. It is also the key.",
     "这个包裹围绕一个赌注建成：一把锁可以描述它自己。不只是保存钥匙，不只是隐藏载荷，"
     "而是把自己的语法写在脸上，并相信读者会注意到。文件的第一行是门的名字，它同时也是钥匙。"),
    ("IV",
     "Every answer in the chain is a key, and every key is also a sentence. 5050 is not only a sum; "
     "it is the moment the reader learns that the package means what it says. K is not only a number; "
     "it is the point where arithmetic becomes architecture.",
     "答案链上的每一个答案都是一把钥匙，而每一把钥匙同时也是一句话。5050 不只是一个和；"
     "它是读者意识到“这个包裹说到做到”的那一刻。K 不只是一个数；它是算术变成建筑的那个点。"),
    ("V",
     "Two lines run through the whole descent. One is the order of exploration: what a solver actually "
     "does, in the order they do it, including the wrong turns. The other is the order of structure: "
     "the layers as they exist in the archive, independent of any reader. This book keeps both lines "
     "visible and shows where they cross.",
     "整段下行有两条线。一条是探索顺序：解题者实际做了什么，按他们做的顺序，包括那些错路。"
     "另一条是结构顺序：压缩包里的层级本身如何存在，与任何读者无关。这本书让两条线同时可见，"
     "并指出它们在哪里交叉。"),
    ("VI",
     "There is noise in the package, and the noise is not accidental. Readable noise is a test of "
     "attention: it rewards the reader who can hold a sentence at arm's length and ask not “is this "
     "true?” but “what would have to be true for this to be here?” The manual lies in a grammar, "
     "and the grammar is learnable.",
     "包裹里有噪音，而噪音并非偶然。可读的噪音是对注意力的测试：它奖励那些能把一句话举到一臂之外、"
     "不问“这是真的吗”，而问“它要成立，周围还必须有什么为真”的读者。说明书用一套语法说谎，"
     "而这套语法是可以学会的。"),
    ("VII",
     "The numbers in the last question look like weather. They move in small local gusts; they seem "
     "to remember the row before. But weather is a system with a state, and this is a system with an "
     "index. The difference is the whole difficulty, and the whole lesson.",
     "最后一题里的数字看起来像天气。它们在局部小阵风里移动，似乎记得上一行。但天气是有状态的系统，"
     "而这是一个有索引的系统。这个差别就是全部的难度，也是全部的教训。"),
    ("VIII",
     "You are holding the solution, which means you are holding the book after the book. Read it "
     "backwards if you like; read it as a record of how a structure was made. Either way, the fragment "
     "is still open. It stays open, and waits.",
     "你手里拿着解答，也就是说，你拿着书之后的那本书。你可以倒着读；也可以把它当作一份记录，"
     "看一个结构如何被制造出来。无论哪种读法，残卷仍然打开着。它保持打开，并等待。"),
]

EPILOGUE = [
    ("I",
     "The last lock is open, but the fragment has not become whole. That was never the promise. "
     "What was promised is a path, and the path is now visible from end to end: ZIP, cover, manual, "
     "5050, the self-describing lock, the SHIT layer, K, the score table, the nested names, the five "
     "questions, and the index-driven engine underneath the last one.",
     "最后一道锁已经打开，但残卷并没有变成整体。那从来不是承诺。承诺的是一条路径，"
     "而这条路径现在从头到尾都可见了：ZIP、封面、说明书、5050、自描述锁、SHIT 层、K、"
     "评分表、嵌套的名字、五道题，以及最后一题下面那台索引驱动的引擎。"),
    ("II",
     "What was solved was not only a number. A number can be checked, but a structure has to be "
     "inhabited. The solver who reaches the end has learned how this particular world expects to be "
     "read: where it tells the truth, where it performs a lie, and where it simply makes noise to see "
     "who is still listening.",
     "被解开的不仅是一个数。数可以被核对，但结构必须被居住。走到终点的解题者，"
     "已经学会了这个世界希望被怎样阅读：它在哪里说真话，在哪里表演谎言，"
     "又在哪里只是制造噪音，看看还有谁在听。"),
    ("III",
     "The difficulty was never only mathematical. It was the cost of holding two orders in mind at "
     "once, the cost of distrusting a pattern that fit too well, the cost of walking past a decoy "
     "that was designed to be walked past. The structure carried the difficulty, and the structure "
     "is the content.",
     "难度从来不只是数学的。它是同时把两种顺序放在心里的代价，是不信任一个拟合得太好的模式的代价，"
     "是走过一个本来就是为了被走过而设计的诱饵的代价。结构承载了难度，而结构就是内容。"),
    ("IV",
     "Returning is part of the route. The book you have just read is not a second fragment; it is the "
     "same fragment seen from the other side. The solver's wrong turns are preserved here because they "
     "are part of the artifact: a record of what the structure did to a mind trying to read it.",
     "返回是路线的一部分。你刚刚读完的这本书不是第二块残片；它是同一块残片从另一面被看见。"
     "解题者的错路被保留在这里，因为它们也是遗物的一部分：一份记录，记下结构对一个试图阅读它的心灵做了什么。"),
    ("V",
     "If you close the file now, the seal does not re-form. The answers remain answers; the keys "
     "remain keys. But the fragment keeps one last property, and it is the property that made the "
     "whole thing worth building: it can be entered again, by someone else, from the beginning.",
     "如果你现在关闭文件，封印不会重新形成。答案仍然是答案，钥匙仍然是钥匙。"
     "但残卷保留最后一个性质，也正是这个性质让整件事值得建造：它可以被另一个人，从头再进入一次。"),
    ("VI",
     "It stays open. It waits.",
     "它保持打开。它等待。"),
]


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

CHAPTER_RE = re.compile(r"^##\s*第\s*(\d+)\s*章")
HEADING_RE = re.compile(r"^(#{2,6})\s+(.*)$")


def slugify(text: str) -> str:
    s = text.strip().lower()
    out = []
    for ch in s:
        if ch.isalnum() or ch in "-_":
            out.append(ch)
        elif ch == " ":
            out.append("-")
    return "".join(out)


def strip_chapter_prefix(title: str) -> str:
    m = re.match(r"^第\s*[\dIVX]+\s*章\s*[：:]\s*(.*)$", title)
    return m.group(1) if m else title


def strip_appendix_prefix(title: str) -> str:
    m = re.match(r"^附录\s*[A-Z]\s*[：:]\s*(.*)$", title)
    return m.group(1) if m else title


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def parse_part(path: Path):
    lines = read(path).splitlines()
    part_title = lines[0].lstrip("# ").strip()
    starts = [i for i, line in enumerate(lines) if CHAPTER_RE.match(line)]
    intro = "\n".join(lines[1:starts[0]]).strip() if starts else ""
    chapters = []
    for j, start in enumerate(starts):
        end = starts[j + 1] if j + 1 < len(starts) else len(lines)
        m = CHAPTER_RE.match(lines[start])
        num = int(m.group(1))
        heading = lines[start].lstrip("#").strip()
        body = "\n".join(lines[start + 1:end]).strip()
        chapters.append(dict(num=num, heading=heading,
                             zh=strip_chapter_prefix(heading), body=body))
    return part_title, intro, chapters


def parse_appendix(path: Path):
    lines = read(path).splitlines()
    heading = lines[0].lstrip("#").strip()
    body = "\n".join(lines[1:]).strip()
    return heading, strip_appendix_prefix(heading), body


def collect_heading_slugs(text: str, target: str, mapping: dict[str, dict[str, str]]):
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            mapping.setdefault(target, {})[slugify(m.group(2))] = target


# ---------------------------------------------------------------------------
# Diagrams (inline SVG)
# ---------------------------------------------------------------------------

def diagram_chain() -> str:
    return """
<svg viewBox="0 0 920 300" role="img" aria-label="The answer chain from P1 to Q5">
  <defs>
    <radialGradient id="dgChainGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#c9a86a" stop-opacity=".18"/>
      <stop offset="100%" stop-color="#c9a86a" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="920" height="300" fill="url(#dgChainGlow)"/>
  <g opacity=".7">
    <circle cx="74" cy="64" r="1.2" fill="#c9a86a"/><circle cx="212" cy="44" r="1" fill="#e9dfc9"/>
    <circle cx="392" cy="62" r="1.1" fill="#74d6d3"/><circle cx="552" cy="38" r="1" fill="#c9a86a"/>
    <circle cx="724" cy="58" r="1.2" fill="#9a86e0"/><circle cx="846" cy="46" r="1" fill="#e9dfc9"/>
  </g>
  <path class="link" d="M122 176 C 176 120, 220 120, 278 164"/>
  <path class="link" d="M330 164 C 388 214, 430 214, 486 176"/>
  <path class="link" d="M538 176 C 594 120, 638 120, 694 164"/>
  <path class="link-b" d="M746 164 C 792 196, 820 196, 858 176"/>
  <g>
    <circle class="node-glow" cx="96" cy="176" r="34"/><circle class="node" cx="96" cy="176" r="20"/>
    <text x="96" y="180" text-anchor="middle" class="label">P1</text>
    <text x="96" y="218" text-anchor="middle" class="zhlabel">5050</text>
  </g>
  <g>
    <circle class="node-glow" cx="304" cy="156" r="30"/><circle class="node" cx="304" cy="156" r="17"/>
    <text x="304" y="160" text-anchor="middle" class="label">Q2</text>
    <text x="304" y="196" text-anchor="middle" class="zhlabel">SHIT / zstd</text>
  </g>
  <g>
    <circle class="node-glow" cx="512" cy="176" r="34"/><circle class="node" cx="512" cy="176" r="20"/>
    <text x="512" y="180" text-anchor="middle" class="label">K</text>
    <text x="512" y="218" text-anchor="middle" class="zhlabel">77 digits</text>
  </g>
  <g>
    <circle class="node-glow" cx="720" cy="156" r="30"/><circle class="node" cx="720" cy="156" r="17"/>
    <text x="720" y="160" text-anchor="middle" class="label">Q3</text>
    <text x="720" y="196" text-anchor="middle" class="zhlabel">.entrance</text>
  </g>
  <g>
    <circle class="node-glow" cx="872" cy="176" r="34"/><circle class="node" cx="872" cy="176" r="20"/>
    <text x="872" y="180" text-anchor="middle" class="label">Q1–5</text>
    <text x="872" y="218" text-anchor="middle" class="zhlabel">data</text>
  </g>
  <g class="label" fill="#8f7345">
    <text x="96" y="260" text-anchor="middle">ENTRY</text>
    <text x="512" y="260" text-anchor="middle">HANDOFF</text>
    <text x="872" y="260" text-anchor="middle">ENDPOINT</text>
  </g>
</svg>"""


def diagram_lock() -> str:
    return """
<svg viewBox="0 0 920 280" role="img" aria-label="Anatomy of the ITC2RECIPE lock">
  <text x="40" y="30" class="label" fill="#8f7345">ONE FILE, THREE VISIBLE PARTS</text>
  <g>
    <rect class="node" x="40" y="56" width="210" height="72" rx="2"/>
    <text x="56" y="84" class="label">MARKER</text>
    <text x="56" y="106" class="zhlabel">ITC2RECIPE · 10 bytes</text>
    <text x="56" y="120" class="zhlabel">name + XOR key</text>
  </g>
  <g>
    <rect class="node" x="286" y="56" width="210" height="72" rx="2"/>
    <text x="302" y="84" class="label">RECIPE</text>
    <text x="302" y="106" class="zhlabel">hex line → XOR</text>
    <text x="302" y="120" class="zhlabel">plaintext instructions</text>
  </g>
  <g>
    <rect class="node" x="532" y="56" width="348" height="72" rx="2"/>
    <text x="548" y="84" class="label">BODY</text>
    <text x="548" y="106" class="zhlabel">base64 → CIPHER</text>
    <text x="548" y="120" class="zhlabel">+ 16-byte TAG</text>
  </g>
  <path class="link" d="M250 92h36"/><path class="link" d="M496 92h36"/>
  <g>
    <rect x="40" y="176" width="210" height="58" rx="2" fill="none" stroke="rgba(116,214,211,.35)" stroke-width=".9"/>
    <text x="56" y="200" class="label" fill="#74d6d3">D → S</text>
    <text x="56" y="220" class="zhlabel">S = SHA-256(ASCII(D))</text>
  </g>
  <path class="link-b" d="M250 205h42"/>
  <g>
    <rect x="292" y="176" width="250" height="58" rx="2" fill="none" stroke="rgba(116,214,211,.35)" stroke-width=".9"/>
    <text x="308" y="200" class="label" fill="#74d6d3">BLOCK STREAM</text>
    <text x="308" y="220" class="zhlabel">SHA-256(S ‖ uint64_be(i))</text>
  </g>
  <path class="link-b" d="M542 205h42"/>
  <g>
    <rect x="584" y="176" width="296" height="58" rx="2" fill="none" stroke="rgba(116,214,211,.35)" stroke-width=".9"/>
    <text x="600" y="200" class="label" fill="#74d6d3">VERIFY, THEN DECRYPT</text>
    <text x="600" y="220" class="zhlabel">TAG = SHA-256(S ‖ 02 ‖ CIPHER)[:16]</text>
  </g>
  <g opacity=".6">
    <path class="dash" d="M145 128v30"/><path class="dash" d="M391 128v30"/><path class="dash" d="M706 128v30"/>
  </g>
</svg>"""


def diagram_affine() -> str:
    return """
<svg viewBox="0 0 920 290" role="img" aria-label="Affine recurrence collapsed into one exponentiation">
  <text x="40" y="30" class="label" fill="#8f7345">10^18 ITERATIONS → ONE MODULAR POWER</text>
  <path d="M70 214 C 190 214, 230 120, 360 126 S 520 196, 640 118 S 800 104, 858 72"
        fill="none" stroke="rgba(201,168,106,.55)" stroke-width="1.2"/>
  <g fill="#c9a86a">
    <circle cx="70" cy="214" r="2.4"/><circle cx="360" cy="126" r="2.4"/>
    <circle cx="640" cy="118" r="2.4"/><circle cx="858" cy="72" r="2.4"/>
  </g>
  <g class="zhlabel">
    <text x="70" y="240" text-anchor="middle">x₀</text>
    <text x="360" y="154" text-anchor="middle">x_n</text>
    <text x="640" y="146" text-anchor="middle">x_2n</text>
    <text x="858" y="100" text-anchor="middle">x_N</text>
  </g>
  <g opacity=".6" stroke="rgba(116,214,211,.4)" stroke-width=".8" stroke-dasharray="2 4">
    <path d="M70 214h788"/><path d="M70 72v142"/>
  </g>
  <g>
    <text x="70" y="62" class="label-b" fill="#e9dfc9">x_{n+1} = (a·x_n + b) mod m</text>
    <text x="70" y="84" class="zhlabel">naive: 10^18 steps</text>
  </g>
  <g>
    <text x="470" y="62" class="label-b" fill="#74d6d3">x_N = a^N x_0 + b·(a^N−1)/(a−1) mod m</text>
    <text x="470" y="84" class="zhlabel">closed form: log N steps</text>
  </g>
</svg>"""


def diagram_ladder() -> str:
    return """
<svg viewBox="0 0 920 290" role="img" aria-label="The score ladder and the unreachable grade">
  <text x="40" y="30" class="label" fill="#8f7345">CHECKPOINT SCORE → GRADE</text>
  <path d="M80 240h780" stroke="rgba(201,168,106,.25)" stroke-width=".8"/>
  <g stroke="rgba(201,168,106,.22)" stroke-width=".8">
    <path d="M120 240V196"/><path d="M280 240V186"/><path d="M440 240V162"/>
    <path d="M600 240V150"/><path d="M760 240V92"/>
  </g>
  <g>
    <rect x="86" y="172" width="68" height="24" fill="rgba(201,168,106,.06)" stroke="rgba(201,168,106,.4)"/>
    <text x="120" y="188" text-anchor="middle" class="label">60 · D</text>
    <rect x="246" y="158" width="68" height="28" fill="rgba(201,168,106,.06)" stroke="rgba(201,168,106,.4)"/>
    <text x="280" y="176" text-anchor="middle" class="label">63 · C</text>
    <rect x="406" y="130" width="68" height="32" fill="rgba(201,168,106,.02)" stroke="rgba(201,168,106,.2)" stroke-dasharray="3 4"/>
    <text x="440" y="150" text-anchor="middle" class="label" opacity=".5">66 · B</text>
    <rect x="566" y="116" width="68" height="34" fill="rgba(201,168,106,.06)" stroke="rgba(201,168,106,.4)"/>
    <text x="600" y="137" text-anchor="middle" class="label">70 · A</text>
    <rect x="700" y="62" width="120" height="30" fill="rgba(116,214,211,.07)" stroke="rgba(116,214,211,.5)"/>
    <text x="760" y="82" text-anchor="middle" class="label" fill="#74d6d3">100 · A+</text>
  </g>
  <g class="zhlabel">
    <text x="120" y="266" text-anchor="middle">start</text>
    <text x="440" y="266" text-anchor="middle">unreachable / 不可达</text>
    <text x="760" y="266" text-anchor="middle">final checkpoint</text>
  </g>
  <path d="M120 240 C 260 224, 360 200, 440 178" fill="none" stroke="rgba(116,214,211,.45)" stroke-width=".8" stroke-dasharray="2 4"/>
</svg>"""


def diagram_nested() -> str:
    return """
<svg viewBox="0 0 920 290" role="img" aria-label="Nested P1-02 entries">
  <text x="40" y="28" class="label" fill="#8f7345">NAMES RUN BACKWARDS</text>
  <rect x="40" y="48" width="840" height="210" rx="2" fill="rgba(201,168,106,.025)" stroke="rgba(201,168,106,.34)"/>
  <text x="58" y="72" class="label">P1-02C</text>
  <rect x="86" y="88" width="748" height="142" rx="2" fill="rgba(201,168,106,.025)" stroke="rgba(201,168,106,.26)"/>
  <text x="104" y="110" class="label">P1-02B</text>
  <rect x="132" y="126" width="656" height="72" rx="2" fill="rgba(201,168,106,.025)" stroke="rgba(201,168,106,.2)"/>
  <text x="150" y="148" class="label">P1-02A</text>
  <rect x="168" y="160" width="270" height="28" fill="rgba(116,214,211,.05)" stroke="rgba(116,214,211,.34)"/>
  <text x="182" y="179" class="label" fill="#74d6d3">content.tar</text>
  <rect x="462" y="160" width="270" height="28" fill="rgba(154,134,224,.05)" stroke="rgba(154,134,224,.34)"/>
  <text x="476" y="179" class="label" fill="#9a86e0">README.7z</text>
  <g class="zhlabel">
    <text x="40" y="282">each layer is a different operation, not a different size</text>
    <text x="760" y="282" text-anchor="end">层层不同其操作，而非不同其大小</text>
  </g>
</svg>"""


def diagram_q5() -> str:
    return """
<svg viewBox="0 0 920 240" role="img" aria-label="Q5 restoration pipeline">
  <text x="40" y="28" class="label" fill="#8f7345">Q5: FROM SURFACE TO GENERATOR</text>
  <g>
    <rect class="node" x="34" y="58" width="142" height="66" rx="2"/>
    <text x="105" y="84" text-anchor="middle" class="label">500 ROWS</text>
    <text x="105" y="106" text-anchor="middle" class="zhlabel">negative runs</text>
  </g>
  <g>
    <rect class="node" x="206" y="58" width="142" height="66" rx="2"/>
    <text x="277" y="84" text-anchor="middle" class="label">EXPAND</text>
    <text x="277" y="106" text-anchor="middle" class="zhlabel">18-wide sparse</text>
  </g>
  <g>
    <rect class="node" x="378" y="58" width="142" height="66" rx="2"/>
    <text x="449" y="84" text-anchor="middle" class="label">T-DECODE</text>
    <text x="449" y="106" text-anchor="middle" class="zhlabel">count + sum</text>
  </g>
  <g>
    <rect class="node" x="550" y="58" width="142" height="66" rx="2"/>
    <text x="621" y="84" text-anchor="middle" class="label">BUCKETS</text>
    <text x="621" y="106" text-anchor="middle" class="zhlabel">C(n) → R(n)</text>
  </g>
  <g>
    <rect class="node" x="722" y="58" width="164" height="66" rx="2"/>
    <text x="804" y="84" text-anchor="middle" class="label">GENERATOR</text>
    <text x="804" y="106" text-anchor="middle" class="zhlabel">index-driven</text>
  </g>
  <g class="link-b">
    <path d="M176 91h22"/><path d="M348 91h22"/><path d="M520 91h22"/><path d="M692 91h22"/>
  </g>
  <g class="zhlabel">
    <text x="105" y="160" text-anchor="middle">1. 读</text>
    <text x="277" y="160" text-anchor="middle">2. 展</text>
    <text x="449" y="160" text-anchor="middle">3. 解</text>
    <text x="621" y="160" text-anchor="middle">4. 分</text>
    <text x="804" y="160" text-anchor="middle">5. 生成</text>
  </g>
  <g opacity=".6">
    <path class="dash" d="M34 204h852"/>
    <text x="34" y="226" class="zhlabel">the surface is a compression of an index, not a trace of a system</text>
    <text x="886" y="226" text-anchor="end" class="zhlabel">表层是索引的压缩，不是系统的轨迹</text>
  </g>
</svg>"""


def diagram_timeline() -> str:
    return """
<svg viewBox="0 0 920 260" role="img" aria-label="Timeline of the two ChatGPT conversations">
  <text x="40" y="28" class="label" fill="#8f7345">TWO CONVERSATIONS, SEVEN PHASES</text>
  <path d="M60 132h800" stroke="rgba(201,168,106,.35)" stroke-width="1"/>
  <g fill="#c9a86a">
    <circle cx="90" cy="132" r="3"/><circle cx="210" cy="132" r="3"/><circle cx="330" cy="132" r="3"/>
    <circle cx="450" cy="132" r="3"/><circle cx="570" cy="132" r="3"/><circle cx="690" cy="132" r="3"/>
    <circle cx="810" cy="132" r="3"/>
  </g>
  <g class="zhlabel">
    <text x="90" y="108" text-anchor="middle">01 entry</text>
    <text x="210" y="164" text-anchor="middle">02 P1</text>
    <text x="330" y="108" text-anchor="middle">03 lock</text>
    <text x="450" y="164" text-anchor="middle">04 P2</text>
    <text x="570" y="108" text-anchor="middle">05 P3</text>
    <text x="690" y="164" text-anchor="middle">06 Q5</text>
    <text x="810" y="108" text-anchor="middle">07 review</text>
  </g>
  <g opacity=".65" stroke="rgba(201,168,106,.18)" stroke-width=".8">
    <path d="M90 126v12"/><path d="M210 126v12"/><path d="M330 126v12"/><path d="M450 126v12"/>
    <path d="M570 126v12"/><path d="M690 126v12"/><path d="M810 126v12"/>
  </g>
  <path d="M90 200 C 240 200, 330 190, 450 200 S 660 210, 810 196"
        fill="none" stroke="rgba(116,214,211,.3)" stroke-width=".8" stroke-dasharray="2 5"/>
  <text x="90" y="224" class="zhlabel">conversation 01</text>
  <text x="810" y="224" text-anchor="end" class="zhlabel">conversation 02</text>
</svg>"""


def diagram_entry() -> str:
    return """
<svg viewBox="0 0 920 280" role="img" aria-label="The outer ZIP and its two entries">
  <text x="40" y="28" class="label" fill="#8f7345">THE OUTER ZIP: TWO ENTRIES, NO README</text>
  <rect x="40" y="58" width="250" height="170" rx="2" fill="rgba(201,168,106,.025)" stroke="rgba(201,168,106,.38)"/>
  <text x="58" y="84" class="label">release/</text>
  <text x="58" y="108" class="label-b" fill="#e9dfc9">THE FRAGMENT.zip</text>
  <text x="58" y="132" class="zhlabel">28,828 bytes · L0</text>
  <rect x="74" y="150" width="182" height="52" rx="2" fill="rgba(201,168,106,.035)" stroke="rgba(201,168,106,.22)"/>
  <text x="88" y="172" class="label">THE FRAGMENT/</text>
  <text x="88" y="190" class="zhlabel">the only directory</text>
  <path class="link" d="M290 142h60"/>
  <g>
    <rect class="node" x="360" y="84" width="232" height="60" rx="2"/>
    <text x="376" y="108" class="label">incipit.7z</text>
    <text x="376" y="128" class="zhlabel">4,626 B · literature</text>
  </g>
  <g>
    <rect class="node" x="360" y="186" width="232" height="60" rx="2"/>
    <text x="376" y="210" class="label">Let's go.7z</text>
    <text x="376" y="230" class="zhlabel">23,617 B · action</text>
  </g>
  <path class="link-b" d="M622 114h50"/><path class="link-b" d="M622 216h50"/>
  <g>
    <text x="690" y="104" class="label">incipit.html</text>
    <text x="690" y="122" class="zhlabel">the cover · 封面</text>
    <text x="690" y="206" class="label">four objects</text>
    <text x="690" y="224" class="zhlabel">manual + locks · 说明书与锁</text>
  </g>
  <text x="360" y="272" class="zhlabel">the choice of which door to open first is already part of the puzzle</text>
</svg>"""


def diagram_shapes() -> str:
    return """
<svg viewBox="0 0 920 250" role="img" aria-label="Five data questions, five shapes">
  <text x="40" y="28" class="label" fill="#8f7345">FIVE QUESTIONS, FIVE SHAPES</text>
  <g>
    <text x="70" y="62" class="label">Q1 · TRIANGLE</text>
    <g fill="none" stroke="rgba(201,168,106,.55)" stroke-width=".8">
      <path d="M50 160l40-36 40 36z"/><path d="M50 160h80M70 142h40M90 124v36"/>
    </g>
    <text x="90" y="190" text-anchor="middle" class="zhlabel">1 / 2 3 / 4 5 6</text>
  </g>
  <g>
    <text x="220" y="62" class="label">Q2 · FIBONACCI</text>
    <g fill="none" stroke="rgba(201,168,106,.55)" stroke-width=".8">
      <path d="M200 160h20v-20h20v-20h40v40h-40v20h-40z"/>
      <path d="M320 160v-20h-20v-20"/>
    </g>
    <text x="270" y="190" text-anchor="middle" class="zhlabel">1 1 2 3 5 8</text>
  </g>
  <g>
    <text x="390" y="62" class="label">Q3 · QUADRATIC</text>
    <g fill="none" stroke="rgba(201,168,106,.55)" stroke-width=".8">
      <path d="M370 160c20-50 50-70 90-80M370 160c20-20 50-30 90-30M370 160c20 10 50 0 90 20"/>
    </g>
    <text x="415" y="190" text-anchor="middle" class="zhlabel">alternating increments</text>
  </g>
  <g>
    <text x="570" y="62" class="label">Q4 · EXPLICIT</text>
    <g stroke="rgba(116,214,211,.55)" stroke-width=".9" fill="none">
      <path d="M550 150h100M600 100v100"/>
      <path d="M566 166c14-40 34-40 48 0"/>
    </g>
    <text x="600" y="190" text-anchor="middle" class="zhlabel">formula is the answer</text>
  </g>
  <g>
    <text x="740" y="62" class="label">Q5 · INDEX</text>
    <g fill="none" stroke="rgba(154,134,224,.55)" stroke-width=".8">
      <path d="M720 160h40M740 140h40M760 120h40M780 100h40M800 80h40"/>
      <path d="M720 180h40M740 180h40M760 180h40"/>
    </g>
    <text x="800" y="205" text-anchor="middle" class="zhlabel">sparse · encoded</text>
  </g>
</svg>"""


def diagram_shortest() -> str:
    return """
<svg viewBox="0 0 920 230" role="img" aria-label="The shortest path through the package">
  <text x="40" y="28" class="label" fill="#8f7345">THE SHORTEST PATH</text>
  <path d="M60 120h800" stroke="rgba(201,168,106,.28)" stroke-width="1"/>
  <g fill="#c9a86a">
    <circle cx="80" cy="120" r="3"/><circle cx="210" cy="120" r="3"/><circle cx="340" cy="120" r="3"/>
    <circle cx="470" cy="120" r="3"/><circle cx="600" cy="120" r="3"/><circle cx="730" cy="120" r="3"/>
    <circle cx="850" cy="120" r="3"/>
  </g>
  <g class="zhlabel">
    <text x="80" y="96" text-anchor="middle">ZIP</text>
    <text x="210" y="150" text-anchor="middle">incipit</text>
    <text x="340" y="96" text-anchor="middle">manual</text>
    <text x="470" y="150" text-anchor="middle">5050</text>
    <text x="600" y="96" text-anchor="middle">SHIT → K</text>
    <text x="730" y="150" text-anchor="middle">Q3 → five Q</text>
    <text x="850" y="96" text-anchor="middle">Q5</text>
  </g>
  <g opacity=".6" stroke="rgba(116,214,211,.34)" stroke-width=".8" stroke-dasharray="2 5">
    <path d="M80 120h770"/>
  </g>
  <text x="80" y="198" class="zhlabel">every fork that does not change the next key is a decoy</text>
  <text x="850" y="198" text-anchor="end" class="zhlabel">每一个不改变下一把钥匙的分岔，都是诱饵</text>
</svg>"""


DIAGRAMS = {
    2: (diagram_chain(), "THE WHOLE PACKAGE", "全包一图：答案链与五个阶段"),
    5: (diagram_entry(), "THE OUTER ZIP", "外层 ZIP：两个入口，没有 README"),
    10: (diagram_lock(), "ANATOMY OF A SELF-DESCRIBING LOCK", "自描述锁的解剖：一行名字，一行语法，一段身体"),
    23: (diagram_affine(), "AFFINE COLLAPSE", "仿射坍缩：十的十八次方次迭代化为一次模幂"),
    28: (diagram_ladder(), "THE GRADE LADDER", "等级阶梯：为什么 B 不可达"),
    32: (diagram_nested(), "NESTED ENTRIES", "嵌套入口：名字倒着走"),
    36: (diagram_shapes(), "FIVE SHAPES", "五道题，五种形状"),
    43: (diagram_q5(), "Q5 PIPELINE", "第 5 题的还原管线"),
    51: (diagram_timeline(), "TWO CONVERSATIONS", "两段对话与七个阶段"),
    54: (diagram_shortest(), "THE SHORTEST PATH", "最短路径：哪些分岔不是诱饵"),
}


# ---------------------------------------------------------------------------
# Rail icons and part sigils
# ---------------------------------------------------------------------------

RAIL_ICONS = {
    "p0": '<circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="2.4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>',
    "p1": '<path d="M4 21V8l8-5 8 5v13"/><path d="M9 21v-7h6v7"/><circle cx="12" cy="10" r="1"/>',
    "p2": '<rect x="4" y="7" width="16" height="12" rx="1"/><path d="M8 7V4h8v3M8 12h8M8 15h5"/>',
    "p3": '<path d="M5 5h14v14H5z"/><path d="M5 10h14M5 14h9M9 5v5M14 14v5"/>',
    "p4": '<rect x="3" y="3" width="18" height="18"/><rect x="7" y="7" width="10" height="10"/><path d="M11 11h2v2h-2z"/>',
    "p5": '<circle cx="6" cy="16" r="1.4"/><circle cx="12" cy="7" r="1.4"/><circle cx="18" cy="14" r="1.4"/><path d="M6 16l6-9M12 7l6 7M6 16l12-2"/>',
    "p6": '<path d="M12 12c0-4 5-4 5 0s-8 4-8 0 6-6 6-2-9 5-9 1 8-8 8-3"/>',
    "p7": '<path d="M4 12h16M12 4v16"/><circle cx="12" cy="12" r="7" stroke-dasharray="2 3"/>',
    "p8": '<path d="M5 4h6a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5z"/><path d="M19 4h-6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h6z"/>',
}

PART_SIGILS = {
    "p0": """
<svg viewBox="0 0 400 400" aria-hidden="true">
  <circle class="draw" pathLength="1" cx="200" cy="200" r="170"/>
  <circle class="draw" pathLength="1" cx="200" cy="200" r="118" stroke-dasharray="1" style="animation-delay:.5s"/>
  <circle class="draw" pathLength="1" cx="200" cy="200" r="62" style="animation-delay:.9s"/>
  <path class="draw" pathLength="1" d="M200 10v380M10 200h380M66 66l268 268M334 66L66 334" style="animation-delay:1.1s"/>
  <circle cx="200" cy="200" r="2.5" fill="currentColor"/>
</svg>""",
    "p1": """
<svg viewBox="0 0 400 400" aria-hidden="true">
  <path class="draw" pathLength="1" d="M80 350V120l120-76 120 76v230"/>
  <path class="draw" pathLength="1" d="M140 350V190h120v160" style="animation-delay:.4s"/>
  <path class="draw" pathLength="1" d="M200 114v76M162 190h76" style="animation-delay:.8s"/>
  <path class="draw" pathLength="1" d="M40 350h320" style="animation-delay:1s"/>
</svg>""",
    "p2": """
<svg viewBox="0 0 400 400" aria-hidden="true">
  <rect class="draw" pathLength="1" x="60" y="90" width="280" height="220" rx="2"/>
  <path class="draw" pathLength="1" d="M60 150h280M120 90v220M120 150l60-60M200 150l60-60M280 150l60-60" style="animation-delay:.4s"/>
  <circle cx="90" cy="120" r="4" fill="currentColor"/><circle cx="120" cy="310" r="4" fill="currentColor"/>
  <circle cx="310" cy="260" r="4" fill="currentColor"/>
  <path class="draw" pathLength="1" d="M90 120h30M120 310v-30M310 260h-30" style="animation-delay:.9s"/>
</svg>""",
    "p3": """
<svg viewBox="0 0 400 400" aria-hidden="true">
  <path class="draw" pathLength="1" d="M90 70h220v260H90z"/>
  <path class="draw" pathLength="1" d="M90 130h150M90 176h220M90 222h100M90 268h180" style="animation-delay:.35s"/>
  <path class="draw" pathLength="1" d="M140 70v260" style="animation-delay:.7s"/>
  <circle cx="118" cy="100" r="4" fill="currentColor"/>
</svg>""",
    "p4": """
<svg viewBox="0 0 400 400" aria-hidden="true">
  <rect class="draw" pathLength="1" x="40" y="70" width="320" height="260"/>
  <rect class="draw" pathLength="1" x="84" y="108" width="232" height="184" style="animation-delay:.35s"/>
  <rect class="draw" pathLength="1" x="128" y="146" width="144" height="108" style="animation-delay:.7s"/>
  <path class="draw" pathLength="1" d="M200 70v260M40 200h320" style="animation-delay:1s"/>
</svg>""",
    "p5": """
<svg viewBox="0 0 400 400" aria-hidden="true">
  <circle class="draw" pathLength="1" cx="200" cy="200" r="150" stroke-dasharray="1"/>
  <g fill="currentColor">
    <circle cx="90" cy="110" r="5"/><circle cx="310" cy="130" r="4"/>
    <circle cx="120" cy="290" r="4"/><circle cx="280" cy="300" r="5"/>
    <circle cx="200" cy="200" r="6"/><circle cx="200" cy="70" r="3"/>
  </g>
  <path class="draw" pathLength="1" d="M90 110l110 90 110-70M120 290l80-90 80 100M200 70v130" style="animation-delay:.4s"/>
</svg>""",
    "p6": """
<svg viewBox="0 0 400 400" aria-hidden="true">
  <path class="draw" pathLength="1" d="M200 200c0-42 58-42 58 0s-88 58-88 0 118-88 118 0-158 118-158 0 188-148 188 0"
        style="animation-delay:.2s"/>
  <path class="draw" pathLength="1" d="M200 30v340M30 200h340" style="animation-delay:.8s" opacity=".4"/>
  <circle cx="200" cy="200" r="3" fill="currentColor"/>
</svg>""",
    "p7": """
<svg viewBox="0 0 400 400" aria-hidden="true">
  <path class="draw" pathLength="1" d="M200 50c86 0 150 70 150 150s-64 150-150 150"/>
  <path class="draw" pathLength="1" d="M200 90c66 0 110 54 110 110s-44 110-110 110" style="animation-delay:.4s"/>
  <path class="draw" pathLength="1" d="M200 350c-86 0-150-70-150-150S114 50 200 50" style="animation-delay:.7s"/>
  <path class="draw" pathLength="1" d="M200 200v-90M200 200l70 50" style="animation-delay:1s"/>
</svg>""",
    "p8": """
<svg viewBox="0 0 400 400" aria-hidden="true">
  <path class="draw" pathLength="1" d="M70 50h180a40 40 0 0 1 40 40v220H110a40 40 0 0 1-40-40z"/>
  <path class="draw" pathLength="1" d="M290 50h40v260h-40" style="animation-delay:.4s"/>
  <path class="draw" pathLength="1" d="M110 120h120M110 170h100M110 220h140M110 270h80" style="animation-delay:.7s"/>
</svg>""",
}


# ---------------------------------------------------------------------------
# Content generation
# ---------------------------------------------------------------------------

def md(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )


def demote(html_text: str, start: int = 3) -> str:
    """Shift heading levels down so the first markdown heading fits under the chapter title."""
    mapping = {}
    for level in range(start, 7):
        mapping[level] = min(level + 1, 6)
    for level in range(6, start - 1, -1):
        new = mapping[level]
        html_text = html_text.replace(f"<h{level}", f"<h{new}").replace(f"</h{level}>", f"</h{new}>")
    return html_text


def build_chapter(num: int, zh_title: str, body_md: str, part_key: str,
                  anchor_map: dict[str, dict[str, str]], file_name: str) -> str:
    en_title, abstract = CHAPTER_META[num]
    body_md = rewrite_links(body_md, file_name, anchor_map)
    body = md(body_md)
    body = demote(body, 3)
    body = re.sub(r"<h4([^>]*)>", r'<h4\1 class="reveal">', body)
    variant = num % 4

    diagram = ""
    if num in DIAGRAMS:
        svg, cap_en, cap_zh = DIAGRAMS[num]
        diagram = (
            '<figure class="diagram reveal" data-anim="scale">'
            + svg
            + '<figcaption><b>' + html.escape(cap_en) + '</b> · ' + html.escape(cap_zh) + '</figcaption></figure>'
        )

    return f"""
<section class="chapter v{variant}" id="chapter-{num}" data-part="{part_key}" data-chapter="{num}">
  <header class="chapter-head">
    <div class="chapter-num" aria-hidden="true">{num:02d}</div>
    <div class="chapter-head-main">
      <p class="chapter-kicker">CHAPTER {num:02d} · PART {PART_ROMAN.get(part_key, part_key.upper())}</p>
      <h3 class="chapter-en">{html.escape(en_title)}</h3>
      <h4 class="chapter-zh">{html.escape(zh_title)}</h4>
      <p class="chapter-abstract reveal" data-anim="fade">{html.escape(abstract)}</p>
    </div>
  </header>
  <div class="chapter-body">{diagram}{body}</div>
</section>"""


def build_part_opener(part: dict, intro_md: str, chapters: list[dict]) -> str:
    key = part["key"]
    first, last = chapters[0]["num"], chapters[-1]["num"]
    first_s = f"{first:02d}" if isinstance(first, int) else str(first)
    last_s = f"{last:02d}" if isinstance(last, int) else str(last)
    note = ""
    if intro_md.strip():
        note_html = md(rewrite_links(intro_md, part["file"], {}))
        note_html = re.sub(r"<h[1-6][^>]*>.*?</h[1-6]>", "", note_html, flags=re.S)
        note = f'<div class="part-note reveal">{note_html}</div>'
    return f"""
<section class="part-open" id="part-{key}" data-part="{key}">
  <div class="part-sigil" aria-hidden="true">{PART_SIGILS[key]}</div>
  <div class="part-inner">
    <p class="part-kicker reveal" data-anim="fade">{part['kicker']}</p>
    <h2 class="part-en reveal">{html.escape(part['en'])}</h2>
    <p class="part-zh reveal">{html.escape(part['zh'])}</p>
    <div class="part-prose reveal">
      <p class="en">{html.escape(part['prose_en'])}</p>
      <p class="zh">{html.escape(part['prose_zh'])}</p>
    </div>
    {note}
    <div class="part-meta reveal" data-anim="fade">
      <div><b>{len(chapters):02d}</b>Chapters / 章</div>
      <div><b>{first_s}–{last_s}</b>Range / 范围</div>
      <div><b>{'A–F' if key == 'p8' else key.upper()}</b>Layer / 层</div>
    </div>
  </div>
</section>"""


def build_appendix(app: dict, body_md: str, anchor_map: dict[str, dict[str, str]]) -> str:
    body_md = rewrite_links(body_md, app["file"], anchor_map)
    body = md(body_md)
    body = demote(body, 2)
    body = re.sub(r"<h4([^>]*)>", r'<h4\1 class="reveal">', body)
    variant = (ord(app["letter"]) - ord("A")) % 4
    return f"""
<section class="chapter v{variant}" id="{app['id']}" data-part="p8" data-chapter="{app['letter']}">
  <header class="chapter-head">
    <div class="chapter-num" aria-hidden="true">{app['letter']}</div>
    <div class="chapter-head-main">
      <p class="chapter-kicker">APPENDIX {app['letter']} · THE CODEX</p>
      <h3 class="chapter-en">{html.escape(app['en'])}</h3>
      <h4 class="chapter-zh">附录 {app['letter']}：{html.escape(app['zh'])}</h4>
      <p class="chapter-abstract">{html.escape(app['abstract'])}</p>
    </div>
  </header>
  <div class="chapter-body">{body}</div>
</section>"""


def rewrite_links(text: str, file_name: str,
                  anchor_map: dict[str, dict[str, str]]) -> str:
    def repl(m):
        label, target = m.group(1), m.group(2).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        fname, _, anchor = target.partition("#")
        base = fname.rsplit("/", 1)[-1]
        if base in anchor_map:
            if anchor and anchor in anchor_map[base]:
                new = "#" + anchor_map[base][anchor]
            else:
                new = "#" + anchor_map[base].get("", "contents")
        elif base in ("README.md", "00-outline.md"):
            new = "#contents"
        elif target.startswith("../../"):
            new = "#appendix-f"
        elif base.endswith(".md"):
            new = "#contents"
        else:
            return m.group(0)
        return f"[{label}]({new})"
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


def build_prose(section_id: str, kicker: str, title_en: str, title_zh: str,
                pairs, epilogue: bool = False, bilingual_note: bool = False) -> str:
    body = []
    for i, (glyph, en, zh) in enumerate(pairs):
        cls = "pair reveal first" if i == 0 else "pair reveal"
        body.append(
            f'<div class="{cls}" data-glyph="{glyph}"><p class="pair-en">{html.escape(en)}</p>'
            f'<p class="pair-zh">{html.escape(zh)}</p></div>'
        )
    mark = (
        '<div class="prose-mark"><svg viewBox="0 0 24 24">'
        '<path d="M12 3v18M4 8l8 4 8-4M4 16l8-4 8 4"/></svg></div>'
    )
    note = ""
    if bilingual_note:
        note = (
            '<div class="bilingual-note reveal" data-anim="fade">'
            '<p class="en">Each chapter opens with an English prelude; the full technical exposition follows in Chinese.</p>'
            '<p class="zh">每一章以英文引子开场，完整的技术正文随后以中文展开。</p>'
            '</div>'
        )
    coda = ""
    if epilogue:
        coda = (
            '<div class="prose-coda">The fragment is still open. It stays open, and waits.'
            '<span class="zh">残卷仍然打开。它保持打开，并等待。</span></div>'
        )
    return f"""
<section class="prose" id="{section_id}">
  <div class="prose-head">
    <p class="prose-kicker">{html.escape(kicker)}</p>
    <h2 class="prose-title">{html.escape(title_en)}</h2>
    <p class="prose-title-zh">{html.escape(title_zh)}</p>
    {mark}
  </div>
  {note}
  {''.join(body)}
  {coda}
</section>"""


def build_contents(parts_with_chapters) -> str:
    cards = []
    for part, chapters in parts_with_chapters:
        cards.append(f"""
<a class="toc-card" href="#part-{part['key']}" data-part="{part['key']}">
  <span class="num">{part['kicker'].split('·')[0].strip()} / {len(chapters):02d}</span>
  <span class="en">{html.escape(part['en'])}</span>
  <span class="zh">{html.escape(part['zh'])}</span>
  <span class="count">{part['num']}</span>
</a>""")
    return f"""
<section class="contents" id="contents">
  <div class="contents-head">
    <div>
      <p class="prose-kicker">THE MAP · 星图</p>
      <h2 class="contents-title">Contents</h2>
      <p class="contents-title-zh">全书目录</p>
    </div>
    <p style="max-width:320px;color:var(--parch-dim);font-size:12.5px;line-height:1.9;margin:0">
      Eight movements and one codex. Enter anywhere; the thread will hold.<br>
      <span style="font-family:var(--serif-zh)">八个乐章与一部法典。从任何一处进入，线索都会接住你。</span>
    </p>
  </div>
  <div class="contents-grid">{''.join(cards)}</div>
  <div class="paths">
    <a class="path" href="#appendix-e"><span><span class="en">Only the answers</span><span class="zh">只核对答案</span></span><span class="arrow">→</span></a>
    <a class="path" href="#chapter-1"><span><span class="en">The full descent</span><span class="zh">完整走一遍</span></span><span class="arrow">→</span></a>
    <a class="path" href="#chapter-10"><span><span class="en">Reproduce the unlock</span><span class="zh">复现解锁</span></span><span class="arrow">→</span></a>
    <a class="path" href="#chapter-43"><span><span class="en">Understand Q5</span><span class="zh">理解第 5 题</span></span><span class="arrow">→</span></a>
    <a class="path" href="#chapter-55"><span><span class="en">The design intent</span><span class="zh">设计意图</span></span><span class="arrow">→</span></a>
    <a class="path" href="#appendix-f"><span><span class="en">Archive and glossary</span><span class="zh">归档与术语</span></span><span class="arrow">→</span></a>
  </div>
</section>"""


def build_rail(parts_with_chapters) -> str:
    out = []
    for part, _chapters in parts_with_chapters:
        out.append(
            f'<a class="rail-node" href="#part-{part["key"]}" data-part="{part["key"]}" '
            f'aria-label="{html.escape(part["en"])} / {html.escape(part["zh"])}">'
            f'<svg viewBox="0 0 24 24">{RAIL_ICONS[part["key"]]}</svg>'
            f'<span class="rail-label"><b>{part["num"]}</b>{html.escape(part["en"])}<br>'
            f'<span style="font-family:var(--serif-zh);font-size:10px">{html.escape(part["zh"])}</span></span></a>'
        )
    out.append(
        '<a class="rail-node" href="#appendix-a" data-part="p8" aria-label="Appendices / 附录">'
        f'<svg viewBox="0 0 24 24">{RAIL_ICONS["p8"]}</svg>'
        '<span class="rail-label"><b>A–F</b>Appendices<br>'
        '<span style="font-family:var(--serif-zh);font-size:10px">附录</span></span></a>'
    )
    return "\n".join(out)


def build_toc(parts_with_chapters, appendices) -> str:
    groups = []
    for part, chapters in parts_with_chapters:
        links = []
        for ch in chapters:
            num = ch["num"]
            en, _ = CHAPTER_META[num]
            links.append(
                f'<button class="toc-link" type="button" data-target="chapter-{num}" '
                f'data-keys="{num} {html.escape(en).lower()} {html.escape(ch["zh"]).lower()}">'
                f'<span class="n">{num:02d}</span><span class="e">{html.escape(en)}</span>'
                f'<span class="z">{html.escape(ch["zh"])}</span></button>'
            )
        groups.append(
            f'<div class="toc-group" data-part="{part["key"]}">'
            f'<h3>{html.escape(part["en"])}<span class="zh">{html.escape(part["zh"])}</span></h3>'
            + ''.join(links) + '</div>'
        )
    links = []
    for app in appendices:
        links.append(
            f'<button class="toc-link" type="button" data-target="{app["id"]}" '
            f'data-keys="{app["letter"]} {html.escape(app["en"]).lower()} {html.escape(app["zh"]).lower()}">'
            f'<span class="n">{app["letter"]}</span><span class="e">{html.escape(app["en"])}</span>'
            f'<span class="z">附录 {app["letter"]}：{html.escape(app["zh"])}</span></button>'
        )
    groups.append(
        '<div class="toc-group" data-part="p8">'
        '<h3>The Codex<span class="zh">附录</span></h3>' + ''.join(links) + '</div>'
    )
    return "\n".join(groups)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    # Parse everything first, so the link map is complete.
    parsed = []
    anchor_map: dict[str, dict[str, str]] = {}
    for part in PARTS:
        title, intro, chapters = parse_part(DOCS / part["file"])
        parsed.append((part, intro, chapters))
        anchor_map.setdefault(part["file"], {})[slugify(title)] = f"part-{part['key']}"
        if chapters:
            anchor_map[part["file"]]["__default__"] = f"chapter-{chapters[0]['num']}"
        for ch in chapters:
            target = f"chapter-{ch['num']}"
            anchor_map[part["file"]][slugify(ch["heading"])] = target
            anchor_map[part["file"]][slugify(ch["zh"])] = target
            collect_heading_slugs(ch["body"], target, anchor_map)
        # make default accessible under the key used by rewrite_links
        if chapters:
            anchor_map[part["file"]][""] = f"chapter-{chapters[0]['num']}"

    parsed_apps = []
    for app in APPENDICES:
        heading, zh, body = parse_appendix(DOCS / app["file"])
        parsed_apps.append((app, body))
        anchor_map.setdefault(app["file"], {})[slugify(heading)] = app["id"]
        anchor_map[app["file"]][slugify(zh)] = app["id"]
        anchor_map[app["file"]]["__default__"] = app["id"]
        anchor_map[app["file"]][""] = app["id"]
        collect_heading_slugs(body, app["id"], anchor_map)

    # Render.
    content = []
    parts_with_chapters = []
    for part, intro, chapters in parsed:
        parts_with_chapters.append((part, chapters))
        content.append(build_part_opener(part, intro, chapters))
        for ch in chapters:
            content.append(build_chapter(ch["num"], ch["zh"], ch["body"],
                                         part["key"], anchor_map, part["file"]))

    # Appendices live under their own opener.
    appendix_chapters = [dict(num=a["letter"], zh=a["zh"]) for a, _ in parsed_apps]
    codex_part = dict(
        key="p8", num="A–F", kicker="APPENDIX · THE CODEX", en="The Codex", zh="附录",
        prose_en="A codex for the return journey: every file, every hash, every answer, "
                 "and the vocabulary needed to speak about them without ambiguity.",
        prose_zh="一部供返程使用的法典：每一个文件、每一个哈希、每一个答案，"
                 "以及谈论它们时所需的、不会含混的词汇。",
    )
    content.append(build_part_opener(codex_part, "", appendix_chapters))
    for app, body in parsed_apps:
        content.append(build_appendix(app, body, anchor_map))
    cards_with_chapters = parts_with_chapters + [(codex_part, appendix_chapters)]

    prologue = build_prose("prologue", "PROLOGUE · 序言", "Prologue", "序言", PROLOGUE,
                           bilingual_note=True)
    contents = build_contents(cards_with_chapters)
    epilogue = build_prose("epilogue", "EPILOGUE · 终章", "Epilogue", "终章", EPILOGUE, epilogue=True)
    # Appendix E is the answers jump target; the appendix section itself carries the id.

    template = read(TEMPLATE)
    out = (template
           .replace("<!--PROLOGUE-->", prologue + contents)
           .replace("<!--CONTENT-->", "\n".join(content))
           .replace("<!--EPILOGUE-->", epilogue)
           .replace("<!--RAIL-->", build_rail(parts_with_chapters))
           .replace("<!--TOC-->", build_toc(parts_with_chapters, [a for a, _ in parsed_apps])))

    # A few structural sanity checks.
    if "<!--" in out:
        print("warning: unresolved template placeholder remains", file=sys.stderr)
    OUT.write_text(out, encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({len(out):,} bytes, {out.count(chr(10)) + 1:,} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
