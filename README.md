# RPS-SIG

Recursive phased-state signature research framework for self-similar post-quantum cryptography.

[![Repository](https://img.shields.io/badge/repo-exocognosis%2Frps--sig-informational.svg)](https://github.com/exocognosis/rps-sig)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-research%20prototype-orange.svg)](#status-and-security-posture)
[![PQC](https://img.shields.io/badge/topic-post--quantum%20cryptography-6f42c1.svg)](#research-focus)
[![Digital Signatures](https://img.shields.io/badge/topic-digital%20signatures-0b7285.svg)](#research-focus)
[![Hash Based](https://img.shields.io/badge/topic-hash--based%20signatures-495057.svg)](#framework-summary)
[![Merkle](https://img.shields.io/badge/topic-Merkle%20commitments-1864ab.svg)](#mathematical-model-at-a-glance)
[![PDF](https://img.shields.io/badge/read-framework%20PDF-2b8a3e.svg)](docs/cryptography/research-notes/recursive-phased-state-signature-framework.pdf)

## Abstract

`rps-sig` is a research repository for **Recursive Phased-State Signatures**: a proposed framework for studying self-similar, phase-separated key generation in post-quantum digital signature schemes.

The central question is whether recursive key-state generation can provide useful structure for compact seed-derived private keys, phase-specific signing domains, and future batch or aggregate verification without creating exploitable cross-scale correlations.

This repository is meant to be informative, attackable, and precise. It does not claim that self-similarity or fractal structure is inherently secure. The goal is to express the idea as finite mathematics, security games, implementation interfaces, and testable proof obligations.

## Research Focus

Current post-quantum signature schemes involve difficult tradeoffs:

- **ML-DSA:** practical and standardized, but keeps deployment concentrated in structured lattices.
- **SLH-DSA:** conservative and hash-based, but signatures are comparatively large.
- **Falcon/FN-DSA:** compact, but implementation and side-channel discipline are more delicate.
- **Additional NIST candidates:** promising, but many rely on younger assumptions, complex proof systems, or active multivariate/isogeny/MPCitH research.

RPS-SIG explores an architectural gap rather than proposing a finished replacement for any standardized scheme:

> Can recursive, self-similar phased key generation improve key compression, signature agility, or batch verification without introducing exploitable cross-scale structure?

## Framework Paper

The initial problem/solution analysis and mathematical framework are available here:

[Recursive Phased-State Signatures: Problem/Solution Analysis and Mathematical Framework](docs/cryptography/research-notes/recursive-phased-state-signature-framework.pdf)

LaTeX source:

[recursive-phased-state-signature-framework.tex](docs/cryptography/research-notes/recursive-phased-state-signature-framework.tex)

The paper introduces:

- the motivation for studying recursive phased-state signatures;
- the problem gap in current PQC signature research;
- a conservative hash-based construction path, `RPS-H`;
- an experimental finite-geometric construction path, `RPS-G`;
- recursive state generation from a root seed;
- phase-local public projections and Merkle commitments;
- global public-key binding across phase roots;
- signing and verification algorithms;
- RPS-EUF-CMA security framing;
- cross-scale one-wayness and phase-binding definitions;
- proof sketches for the conservative hash-based variant;
- implementation and evaluation criteria.

## Framework Summary

The core idea is to derive a tree of secret signing states from one root seed. Each phase corresponds to a labeled depth or slice of that tree. Public projections of phase-local states are committed into phase roots, and the global public key binds those roots into one verification domain.

```text
root seed -> recursive state tree -> phase public projections -> public key
```

The framework separates two tracks:

- **RPS-H:** a conservative hash-based construction using SHAKE-style domain-separated expansion, Merkle commitments, and one-time or few-time leaf signatures.
- **RPS-G:** an experimental finite-geometric track where recursive states live over discrete spaces such as finite fields, rings, lattices, codes, or graphs.

The conservative track exists to make the architecture testable before introducing new hardness assumptions. The experimental track asks whether finite self-similar structure can become a useful cryptographic object rather than only a key-generation pattern.

## Mathematical Model At A Glance

Let `s` be a root secret seed, `D` a recursion depth, `b` a branching factor, and `phi_i` a phase label. A node is a path `v` in a rooted `b`-ary tree.

The conservative model derives recursive secret states:

```text
S_empty = H("RPS-root" || s)
S_(v || j) = H("RPS-child" || S_v || phi_i || j || v)
```

Each secret state has a phase-bound public projection:

```text
P_v = H("RPS-public" || phi_i || v || S_v)
```

Each phase commits to its public projections:

```text
C_i = MerkleRoot({ P_v : |v| = i })
```

The global public key binds all phase commitments:

```text
PK = H("RPS-pk" || C_0 || C_1 || ... || C_D)
```

This creates a concrete attack target: public views across phases must not make it easier to recover a secret state, forge a signature, reinterpret a signature under another phase, or exploit related-state structure.

## Security Questions

RPS-SIG is organized around questions that reviewers and implementers can test:

- Can cross-phase public projections leak information about parent, child, or sibling states?
- Can a signature produced for one phase be replayed or reinterpreted under another phase?
- Can self-similar state generation create low-rank, cyclic, or recurrence-based shortcuts?
- Can batch verification be added without creating aggregate forgery paths?
- Can a stateful prototype prevent leaf reuse reliably?
- Can a stateless version preserve the same phase-binding guarantees?
- Can an experimental finite-geometric variant survive linearization, Gröbner-basis, cycle-finding, meet-in-the-middle, related-key, and quantum-amplification attacks?

## Status And Security Posture

This repository is **research-stage**.

No construction in this repository should be used for production signing, key management, consensus, software updates, identity, certificates, or any other security-critical deployment.

Current priorities:

1. Publish the framework paper and LaTeX source.
2. Define security games and proof obligations.
3. Prototype the conservative `RPS-H` construction.
4. Add deterministic test vectors.
5. Add misuse tests for phase confusion, malformed paths, and leaf reuse.
6. Benchmark key size, signature size, signing time, verification time, and batch-verification behavior.
7. Evaluate whether finite-geometric variants deserve implementation.
8. Invite external review and cryptanalysis.

## Repository Map

- `docs/cryptography/research-notes/`: framework paper, LaTeX source, and related research notes.
- `tools/`: local generation or rendering utilities for research artifacts.
- `LICENSE`: project license.
- `README.md`: project overview and navigation.

## Suggested GitHub Topics

`post-quantum`, `cryptography`, `digital-signatures`, `signature-schemes`, `hash-based-signatures`, `recursive-signatures`, `self-similar`, `pqc`, `merkle-tree`, `finite-fields`, `lattice-cryptography`, `code-based-cryptography`, `signature-aggregation`, `research`

## Search Tags

`RPS-SIG`, `Recursive Phased-State Signatures`, `post-quantum cryptography`, `PQC`, `digital signatures`, `self-similar cryptography`, `fractal-inspired cryptography`, `recursive key generation`, `hash-based signatures`, `Merkle commitments`, `finite-geometric cryptography`, `signature aggregation`, `cryptography research`

## Contributing

Contributions should keep security claims precise. Research proposals, attacks, reductions, benchmarks, misuse tests, and clearer mathematical formulations are preferred over broad claims of novelty or security.

Before proposing an implementation, define the assumption, public problem, attacker model, parameter set, and expected failure modes.
