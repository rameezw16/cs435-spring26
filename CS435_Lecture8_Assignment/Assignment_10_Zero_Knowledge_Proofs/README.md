# Zero-Knowledge Proof (ZKP) 

## Overview

This project demonstrates a Zero-Knowledge Proof — a way for a prover to convince a verifier that they know a secret without actually revealing it.

- **Prover:** The person who knows the secret.
- **Verifier:** The person who wants proof without learning the secret.

The protocol is interactive: the prover and verifier exchange values for several rounds.

## Protocol Flow

Each round has three main steps:

### 1. Commitment (Prover → Verifier)

The prover picks a random number `r` and computes a commitment:

```
t = G^r mod P
```

The prover sends `t` to the verifier. This hides the secret while still "locking in" a value for the round.

### 2. Challenge (Verifier → Prover)

The verifier randomly chooses a challenge `c = 0 or 1` and sends `c` to the prover.

### 3. Response (Prover → Verifier)

The prover computes:

```
s = r + c * x mod Q
```

- If `c = 0` → `s = r`
- If `c = 1` → `s = r + x`

The prover sends `s` back to the verifier.

### 4. Verification (Verifier checks)

The verifier checks if:

```
G^s = t * Y^c mod P
```

If it matches → round accepted. Otherwise → rejected.

## How It Works Intuitively

- **Real prover:** always passes, because they know `x` and can compute `s` for any challenge.
- **Fake prover:** doesn't know `x`, so can only guess the challenge in advance.
  - Success probability per round = 50%
  - Multiple rounds → probability decreases exponentially:

```
Success probability = (1/2)^(number of rounds)
```

## The Experiment

We ran multiple rounds to test:

### 1. Honest prover

Always passes all rounds. Demonstrates that knowing the secret guarantees success.

### 2. Fake prover

Randomly guesses challenges. Success rate drops as the number of rounds increases. Matches the theoretical probability `(1/2)^n`.

### 3. Visualization

We plotted acceptance rate vs number of rounds:

- Honest prover → ~100% success
- Fake prover → drops exponentially
- Confirms the security principle of repeated ZKP rounds.

## How to Run

Install the required library:

```
pip install matplotlib
```

Then run the script:

```
python protocol.py
```