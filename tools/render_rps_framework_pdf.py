from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


OUT = Path("docs/cryptography/research-notes/recursive-phased-state-signature-framework.pdf")


def add_wrapped(ax, text: str, x: float, y: float, width: int = 96, size: int = 9.6,
                weight: str = "normal", color: str = "#222222", leading: float = 0.035) -> float:
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            y -= leading * 0.6
            continue
        for line in textwrap.wrap(paragraph, width=width, break_long_words=False):
            ax.text(x, y, line, transform=ax.transAxes, fontsize=size, weight=weight,
                    color=color, va="top", family="DejaVu Sans")
            y -= leading
    return y


def add_bullets(ax, bullets: list[str], x: float, y: float, width: int = 88,
                size: int = 9.4, leading: float = 0.033) -> float:
    for bullet in bullets:
        lines = textwrap.wrap(bullet, width=width, break_long_words=False)
        ax.text(x, y, "-", transform=ax.transAxes, fontsize=size, color="#222222",
                va="top", family="DejaVu Sans")
        ax.text(x + 0.025, y, lines[0], transform=ax.transAxes, fontsize=size,
                color="#222222", va="top", family="DejaVu Sans")
        y -= leading
        for line in lines[1:]:
            ax.text(x + 0.025, y, line, transform=ax.transAxes, fontsize=size,
                    color="#222222", va="top", family="DejaVu Sans")
            y -= leading
        y -= leading * 0.15
    return y


def add_math(ax, tex: str, x: float, y: float, size: int = 12) -> float:
    ax.text(x, y, f"${tex}$", transform=ax.transAxes, fontsize=size, color="#111111",
            va="top", family="DejaVu Sans")
    return y - 0.055


def add_code(ax, code: str, x: float, y: float, size: int = 8.5) -> float:
    for line in code.splitlines():
        ax.text(x, y, line, transform=ax.transAxes, fontsize=size, color="#111111",
                va="top", family="DejaVu Sans Mono")
        y -= 0.03
    return y - 0.012


def page(pdf: PdfPages, title: str, body):
    fig = plt.figure(figsize=(8.5, 11))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.text(0.08, 0.94, title, transform=ax.transAxes, fontsize=17, weight="bold",
            color="#111111", va="top", family="DejaVu Sans")
    ax.plot([0.08, 0.92], [0.905, 0.905], transform=ax.transAxes, color="#444444", lw=0.8)
    body(ax)
    pdf.savefig(fig)
    plt.close(fig)


def cover(pdf: PdfPages):
    fig = plt.figure(figsize=(8.5, 11))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.text(0.08, 0.86, "Recursive Phased-State Signatures",
            transform=ax.transAxes, fontsize=25, weight="bold", va="top", family="DejaVu Sans")
    ax.text(0.08, 0.805, "Problem/Solution Analysis and Mathematical Framework",
            transform=ax.transAxes, fontsize=15, color="#333333", va="top", family="DejaVu Sans")
    ax.text(0.08, 0.755, "Research note - May 28, 2026",
            transform=ax.transAxes, fontsize=10.5, color="#555555", va="top", family="DejaVu Sans")
    ax.plot([0.08, 0.92], [0.725, 0.725], transform=ax.transAxes, color="#444444", lw=0.9)
    y = 0.675
    y = add_wrapped(ax,
        "This document defines a research framework for a recursive phased-state "
        "post-quantum signature scheme. It is not a production-ready cryptosystem. "
        "The objective is to turn a self-similar key-generation idea into finite "
        "mathematics, implementation interfaces, proof obligations, and attack targets.",
        0.08, y, width=92, size=10.8, leading=0.039)
    y -= 0.025
    y = add_math(ax, r"s \rightarrow S_{\epsilon} \rightarrow \{S_v:v\in\mathcal{T}_{D,b}\} \rightarrow \{P_v\} \rightarrow PK", 0.12, y, size=13)
    y -= 0.02
    add_bullets(ax, [
        "Conservative base design: SHAKE256 expansion, phase-separated Merkle commitments, and WOTS+/FORS-like leaf signatures.",
        "Experimental path: replace hash-only expansion with finite geometric recursive maps after the security games are testable.",
        "Main research question: does self-similar phased key generation improve compression, agility, or batch verification without exploitable cross-scale structure?",
    ], 0.10, y, width=86, size=10.2, leading=0.037)
    pdf.savefig(fig)
    plt.close(fig)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(OUT) as pdf:
        cover(pdf)

        page(pdf, "1. Problem Analysis", lambda ax: problem_page(ax))
        page(pdf, "2. Solution Model", lambda ax: solution_page(ax))
        page(pdf, "3. Mathematical Framework", lambda ax: framework_page(ax))
        page(pdf, "4. Algorithms", lambda ax: algorithms_page(ax))
        page(pdf, "5. Security Games and Proof Sketch", lambda ax: security_page(ax))
        page(pdf, "6. Finite-Geometric Variant", lambda ax: geometric_page(ax))
        page(pdf, "7. Implementation and Evaluation", lambda ax: implementation_page(ax))


def problem_page(ax):
    y = 0.86
    y = add_wrapped(ax,
        "Current post-quantum signature choices create unavoidable tradeoffs. "
        "ML-DSA is practical but keeps deployment concentrated in structured lattices. "
        "SLH-DSA is conservative and hash-based, but signatures are larger. "
        "Falcon/FN-DSA is compact, but implementation is more delicate. Additional "
        "candidate families diversify assumptions, yet many rely on complex proof "
        "systems, active multivariate assumptions, or novel isogeny machinery.",
        0.08, y)
    y -= 0.018
    ax.text(0.08, y, "Target gap", transform=ax.transAxes, fontsize=11.5, weight="bold",
            va="top", family="DejaVu Sans")
    y -= 0.04
    y = add_bullets(ax, [
        "Compact seed-derived private keys.",
        "Explicitly separated signing phases for domains, security levels, validity windows, or aggregation layers.",
        "Recursive, self-similar finite state generation rather than real-valued chaotic maps.",
        "Public commitments that bind all phases to one public key.",
        "A credible path to batch verification or aggregation.",
        "Concrete attack surfaces: related-phase leakage, recurrence recovery, phase confusion, and state reuse.",
    ], 0.10, y)
    y -= 0.018
    ax.text(0.08, y, "Non-goal", transform=ax.transAxes, fontsize=11.5, weight="bold",
            va="top", family="DejaVu Sans")
    y -= 0.04
    add_wrapped(ax,
        "The framework does not claim that fractal or chaotic behavior is itself a "
        "hardness assumption. The cryptographic object must be finite, parameterized, "
        "and expressible as security games that can be attacked by the community.",
        0.08, y)


def solution_page(ax):
    y = 0.86
    y = add_wrapped(ax,
        "A root seed generates a tree of secret states. A phase is a labeled depth "
        "or slice of that tree. Each state has a public projection. A public key "
        "commits to all phase roots. A signature proves that one valid phase-local "
        "secret signed the message and belongs to the committed public key.",
        0.08, y)
    y -= 0.016
    y = add_math(ax, r"\Phi=\{\phi_0,\phi_1,\ldots,\phi_D\}", 0.12, y)
    y = add_math(ax, r"P_v=\Pi_{\phi_{|v|}}(S_v)", 0.12, y)
    y = add_math(ax, r"C_i=\mathrm{MerkleRoot}(\{P_v:|v|=i\})", 0.12, y)
    y = add_math(ax, r"PK=H(\mathrm{RPS\_pk}\parallel C_0\parallel\cdots\parallel C_D)", 0.12, y)
    y -= 0.01
    ax.text(0.08, y, "Design rule", transform=ax.transAxes, fontsize=11.5, weight="bold",
            va="top", family="DejaVu Sans")
    y -= 0.04
    y = add_wrapped(ax,
        "Use standard cryptographic expansion for entropy. Let the self-similar idea "
        "define the recursive finite structure and phase schedule, not a custom PRG. "
        "This keeps the first prototype conservative and makes later geometric variants "
        "easier to isolate and analyze.",
        0.08, y)
    y -= 0.018
    add_bullets(ax, [
        "RPS-H: conservative hash-based construction with Merkle commitments and one-time/few-time leaf signatures.",
        "RPS-G: experimental finite-geometric construction where states live in a finite vector space and projections encode a hidden recursive relation.",
    ], 0.10, y)


def framework_page(ax):
    y = 0.86
    y = add_wrapped(ax,
        "Let lambda be the target security parameter, D the recursion depth, b the "
        "branching factor, and T_{D,b} the rooted b-ary tree of depth D. A node is "
        "a path v=(j_1,...,j_i) with |v|=i.",
        0.08, y)
    y -= 0.012
    y = add_math(ax, r"s \leftarrow_R \{0,1\}^{\lambda}", 0.12, y)
    y = add_math(ax, r"S_{\epsilon}=H(\mathrm{RPS\_root}\parallel s)", 0.12, y)
    y = add_math(ax, r"S_{v\parallel j}=H(\mathrm{RPS\_child}\parallel S_v\parallel \phi_i\parallel j\parallel v)", 0.12, y)
    y = add_math(ax, r"P_v=H(\mathrm{RPS\_public}\parallel\phi_i\parallel v\parallel S_v)", 0.12, y)
    y -= 0.01
    y = add_wrapped(ax,
        "The expansion is self-similar because the same child relation is used at "
        "every scale. Domain strings, phase labels, and canonical path encodings are "
        "mandatory; without them, different phases may become related-key domains.",
        0.08, y)
    y -= 0.015
    ax.text(0.08, y, "Private/public material", transform=ax.transAxes, fontsize=11.5,
            weight="bold", va="top", family="DejaVu Sans")
    y -= 0.042
    y = add_math(ax, r"SK=s\quad\mathrm{or}\quad SK=(s,\{S_v\}_{v\in\mathcal{C}})", 0.12, y)
    add_math(ax, r"PK=H(\mathrm{RPS\_pk}\parallel C_0\parallel C_1\parallel\cdots\parallel C_D)", 0.12, y)


def algorithms_page(ax):
    y = 0.86
    ax.text(0.08, y, "KeyGen", transform=ax.transAxes, fontsize=11.5, weight="bold",
            va="top", family="DejaVu Sans")
    y -= 0.035
    y = add_code(ax, """sample s <- {0,1}^lambda
derive S_epsilon and all S_v by recursive expansion
for each phase i:
    L_i = { P_v : |v| = i }
    C_i = MerkleRoot(L_i)
PK = H(\"RPS-pk\" || C_0 || ... || C_D)
return (PK, SK=s)""", 0.10, y)
    y -= 0.008
    ax.text(0.08, y, "Sign", transform=ax.transAxes, fontsize=11.5, weight="bold",
            va="top", family="DejaVu Sans")
    y -= 0.035
    y = add_code(ax, """select unused path v with |v| = i
derive S_v from seed s
x_v = H(\"RPS-ots-secret\" || S_v || H(m))
sigma_ots = OTS.Sign(x_v, m)
P_v = H(\"RPS-public\" || phi_i || v || S_v)
pi_v = MerkleAuthPath(P_v, C_i)
return sigma = (i, v, sigma_ots, P_v, pi_v)""", 0.10, y)
    y -= 0.008
    ax.text(0.08, y, "Verify", transform=ax.transAxes, fontsize=11.5, weight="bold",
            va="top", family="DejaVu Sans")
    y -= 0.035
    add_code(ax, """check |v| == i
check OTS.Verify(P_v, m, sigma_ots)
check MerkleVerify(P_v, pi_v, C_i)
check PK == H(\"RPS-pk\" || C_0 || ... || C_D)
accept only if all checks pass""", 0.10, y)


def security_page(ax):
    y = 0.86
    y = add_wrapped(ax,
        "The minimum security model is RPS-EUF-CMA: the adversary gets the public "
        "key and signing access for chosen messages and phases, subject to path-use "
        "rules. The adversary wins by producing a valid signature for a new message "
        "or a new authorized path/message pair.",
        0.08, y)
    y -= 0.012
    ax.text(0.08, y, "Cross-scale one-wayness", transform=ax.transAxes, fontsize=11.5,
            weight="bold", va="top", family="DejaVu Sans")
    y -= 0.04
    y = add_math(ax, r"\Pr[A(\{P_v:v\in Q\})=S_u]\leq 2^{-\lambda}+\epsilon(\lambda)", 0.12, y, size=11)
    y = add_wrapped(ax,
        "This captures the key new risk: parent, child, and sibling projections "
        "must not make any hidden state easier to recover.",
        0.08, y)
    y -= 0.014
    ax.text(0.08, y, "Proof sketch for RPS-H", transform=ax.transAxes, fontsize=11.5,
            weight="bold", va="top", family="DejaVu Sans")
    y -= 0.04
    add_bullets(ax, [
        "If a forgery uses a projection outside the committed phase root, it breaks Merkle collision resistance.",
        "If it uses a committed but unused projection, it forges the one-time/few-time signature.",
        "If it changes the phase, explicit phase labels and canonical encodings force a distinct random-oracle domain.",
        "If it reuses an exposed leaf, the implementation failed state management; a stateless variant must replace the leaf mechanism.",
    ], 0.10, y, width=86)


def geometric_page(ax):
    y = 0.86
    y = add_wrapped(ax,
        "The geometric variant replaces hash-only child generation with a recursive "
        "finite-space transformation. This should be treated as a second-stage "
        "research problem after RPS-H has been implemented and measured.",
        0.08, y)
    y -= 0.014
    y = add_math(ax, r"S_v\in\mathbb{F}_q^n", 0.12, y)
    y = add_math(ax, r"S_{v\parallel j}=H_{\mathbb{F}_q^n}(A_{\phi_i,j}S_v+B_{\phi_i,j}+N_{\phi_i,j}(S_v)\;\mathrm{mod}\;q)", 0.12, y, size=10.5)
    y -= 0.01
    ax.text(0.08, y, "Hidden Recursive Embedding Problem", transform=ax.transAxes,
            fontsize=11.5, weight="bold", va="top", family="DejaVu Sans")
    y -= 0.04
    y = add_wrapped(ax,
        "Given public projections of a recursively generated finite geometric object, "
        "recover a secret state, a hidden path, or a trapdoor relation linking two "
        "phases. A candidate is not credible until this problem is parameterized and "
        "attacked directly.",
        0.08, y)
    y -= 0.018
    add_bullets(ax, [
        "Expected attacks: linearization, Groebner bases, cycle finding, meet-in-the-middle, related-key analysis, and quantum amplitude amplification.",
        "The design should avoid real-number chaos and floating point; all objects should live over finite fields, rings, graphs, codes, or lattices.",
        "If the finite-geometric relation collapses into an existing hard problem, it should be presented honestly under that family.",
    ], 0.10, y, width=86)


def implementation_page(ax):
    y = 0.86
    y = add_wrapped(ax,
        "A minimal implementation should expose four functions and keep the first "
        "prototype stateful so leaf reuse is easy to detect during testing.",
        0.08, y)
    y -= 0.012
    y = add_math(ax, r"(PK,SK)\leftarrow \mathrm{RPS.KeyGen}(\lambda,D,b)", 0.12, y)
    y = add_math(ax, r"\sigma\leftarrow \mathrm{RPS.Sign}(SK,m,i)", 0.12, y)
    y = add_math(ax, r"\{0,1\}\leftarrow \mathrm{RPS.Verify}(PK,m,\sigma)", 0.12, y)
    y = add_math(ax, r"\{0,1\}\leftarrow \mathrm{RPS.BatchVerify}(PK,\{m_k,\sigma_k\}_k)", 0.12, y)
    y -= 0.01
    ax.text(0.08, y, "Evaluation checklist", transform=ax.transAxes, fontsize=11.5,
            weight="bold", va="top", family="DejaVu Sans")
    y -= 0.04
    y = add_bullets(ax, [
        "Measure public key size, private key size, signature size, signing time, verification time, and batch verification savings.",
        "Test phase misuse, phase confusion, duplicate leaf use, malformed authentication paths, and non-canonical encodings.",
        "Run cross-phase statistical checks and structural leakage tests before considering any finite-geometric variant.",
        "Document exact assumptions: OTS security, Merkle collision resistance, random-oracle domain separation, and state-management constraints.",
    ], 0.10, y, width=86)
    y -= 0.012
    add_wrapped(ax,
        "References: NIST Post-Quantum Cryptography Standardization Project; NIST Round 3 "
        "Additional Digital Signature Schemes; NIST IR 8610, 2026.",
        0.08, y, width=92, size=8.8, color="#555555")


if __name__ == "__main__":
    main()
