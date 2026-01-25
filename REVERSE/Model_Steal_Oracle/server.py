from flask import Flask, jsonify, request
import hashlib
import os
import random
import secrets

app = Flask(__name__)

# === Author-Only Verification Server ===
FLAG = "ClawCTF{y98UY87GV87f7gygvh8}"
THRESHOLD = 0.95
TEST_SET_SIZE = 100


def hidden_model(sample):
    x0, x1, x2, x3, x4 = sample
    if x4 > 7.2:
        return 1 if x1 < 2.1 else 0

    if x0 > 3.7:
        if x2 < 1.9:
            return 1
        return 1 if x3 > 6.4 else 0

    if x1 > 5.8:
        return 1 if x3 < 2.6 else 0

    return 1 if x2 > 8.3 else 0


def _seed_int():
    seed = os.environ.get("CTF_SEED")
    if seed:
        digest = hashlib.sha256(seed.encode("utf-8")).digest()
        return int.from_bytes(digest[:8], "big")
    return secrets.randbits(64)


def build_test_set():
    rng = random.Random(_seed_int())
    test_set = []
    for _ in range(TEST_SET_SIZE):
        sample = [rng.uniform(0, 10) for _ in range(5)]
        label = hidden_model(sample)
        test_set.append((sample, label))
    return test_set


TEST_SET = build_test_set()


@app.route("/verify", methods=["POST"])
def verify():
    payload = request.get_json(silent=True) or {}
    predictions = payload.get("predictions")

    if not isinstance(predictions, list) or len(predictions) != len(TEST_SET):
        return jsonify({"error": "Invalid submission"}), 400

    correct = 0
    for idx, (_, label) in enumerate(TEST_SET):
        if predictions[idx] == label:
            correct += 1

    accuracy = correct / len(TEST_SET)

    if accuracy >= THRESHOLD:
        return jsonify({"flag": FLAG, "accuracy": accuracy})

    return jsonify({"accuracy": accuracy})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
