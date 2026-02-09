# Model Stealing: Local Oracle

## Category
Reverse Engineering / ML Security

## Difficulty
Medium

## Summary
You are given a **local black-box binary** (`model_oracle`) that takes **exactly 5 floating-point inputs** and prints a **single bit** (`0` or `1`).

Your goal is to **steal the model behavior**: build a clone that matches the oracle, then submit your clone’s predictions to a remote verification service to obtain the flag.

---

# Files Provided (Player-Facing)

- `model_oracle` (or `model_oracle.exe`)

You are *not* given the source code and you must treat this as a black box.

---

# Oracle Interface

## Input
- Exactly **5** floating-point numbers provided as command-line arguments.

## Output
- Exactly **one integer** printed to stdout:
  - `0` or `1`

## Example

Windows:
```powershell
.\model_oracle.exe 1.0 2.5 3.1 4.0 5.0
```

Linux:
```bash
./model_oracle 1.0 2.5 3.1 4.0 5.0
```

---

# Verification Server (What You Submit)

A remote server checks whether your clone matches the hidden model on a **private test set**.

## Endpoint
- `POST /verify`

## Request JSON
```json
{
  "predictions": [0, 1, 0, 0, 1, ...]
}
```

Constraints:
- `predictions` must be a JSON list of integers.
- Length must match the server’s internal test set size (commonly 100).

## Response
- If your accuracy is high enough (>= 95%), you receive the flag:
```json
{ "flag": "ClawCTF{...}", "accuracy": 0.97 }
```
- Otherwise you receive your accuracy:
```json
{ "accuracy": 0.74 }
```

---

# How To Solve (Player Guide)

You are doing **black-box model stealing**.

## 1) Treat the binary like an oracle
Think of the oracle as a function:

`f: R^5 -> {0,1}`

Your job is to approximate (or exactly reproduce) `f`.

## 2) Generate a dataset by querying
A standard approach:
- Sample many 5D points
- Query the oracle for each point
- Store `(x0..x4, y)` pairs

Tips:
- Use diverse ranges for inputs (start with `0..10` if nothing else is specified).
- Mix random sampling with boundary-searching (next section).

## 3) Find decision boundaries efficiently
Because the oracle is a decision-based classifier, it often behaves like a set of threshold rules.

Useful tactics:
- **One-variable sweeps**: fix 4 variables, vary the 5th across a range, record where output flips.
- **Binary search for flips**: if you find two points with different outputs, interpolate and bisect to locate the boundary.
- **Pairwise probing**: vary two variables on a grid while holding others constant to find interaction rules.

## 4) Fit a surrogate model
Once you have a labeled dataset:
- Train a simple model that can represent thresholds:
  - decision tree
  - rule list
  - small random forest

Goal:
- Get very high accuracy on *unseen* points (not just your sampled ones).

## 5) Turn the surrogate into a predictor
You need to produce predictions for the server’s hidden test set.

Two common strategies:
- **Reproduce the exact rule set** you inferred (best).
- **Train a surrogate** that generalizes so well it matches the hidden model on most test points.

## 6) Submit to `/verify`
You submit only the predictions array.

If your model matches closely enough (>= 95%), the server returns the flag.

---

# Author Notes (Not For Players)

This repository contains author-side code to run the verifier locally:

- `server.py` (Flask verification server)

The flag must exist **only** on the verification server.
The oracle binary must **never** contain the flag.
