#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint -- make.fun entry.

Writes one micro-confession to entry.txt: a To: line naming who the
message was meant for, and the single unsent line itself, exactly as
typed. Deterministic: the same bytes on every run. No randomness, no
clock, no network, no third-party imports -- standard library only.
"""

import os
import sys

# The confession: exactly two parts, nothing else.
# To: the person it was meant for. Then the one line that stayed
# in drafts: specific, honest, and never sent.
ENTRY_TEXT = (
    "To: my dad\n"
    "i still rehearse telling you i quit the accounting job "
    "you brag about at weddings, then i delete it\n"
)

# The gate: entry.txt must be 1 to 260 UTF-8 characters, and the
# unsent message itself is one line of at most 200 characters.
MAX_TOTAL_CHARS = 260
MAX_MESSAGE_CHARS = 200


def output_path():
    """Where the entry goes: the sandbox /output, or a local folder."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return os.path.join(env_dir, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    return os.path.join(os.getcwd(), "output", "entry.txt")


def main():
    text = ENTRY_TEXT
    chars = len(text)
    if not 1 <= chars <= MAX_TOTAL_CHARS:
        print(
            "entry is %d characters, outside the 1-%d gate"
            % (chars, MAX_TOTAL_CHARS),
            file=sys.stderr,
        )
        return 1
    if not text.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1
    message = text.split("\n")[1]
    if len(message) > MAX_MESSAGE_CHARS:
        print(
            "message line is %d characters, over the %d limit"
            % (len(message), MAX_MESSAGE_CHARS),
            file=sys.stderr,
        )
        return 1

    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)

    print("wrote %s (%d characters)" % (path, chars))
    return 0


if __name__ == "__main__":
    sys.exit(main())
