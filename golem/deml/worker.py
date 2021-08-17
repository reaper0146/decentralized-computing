#!/usr/bin/env python3
"""
This file contains the script that will be run on provider nodes executing our task.
It is included in the image built from this project's Dockerfile.
"""

import json
from pathlib import Path
from typing import List
from hashlib import sha256

ENCODING = "utf-8"

HASH_PATH = Path("data/hash-short.json")
WORDS_PATH = Path("data/words-short.json")
RESULT_PATH = Path("data")

if __name__ == "__main__":
    result = ""

    with HASH_PATH.open() as f:
        target_hash: str = json.load(f)

    with WORDS_PATH.open() as f:
        words: List[str] = json.load(f)
        # TODO Compare target hash with sha256 of each word
        for line in words:
            line_bytes = bytes(line.strip(), ENCODING)
            line_hash = sha256(line_bytes).hexdigest()
            if line_hash == target_hash:
                result = line
                break

    with RESULT_PATH.open(mode="w", encoding=ENCODING) as f:
        json.dump(result, f)
