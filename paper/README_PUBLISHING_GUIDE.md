# H-MoE Research Paper Publishing & Submission Guide

This guide details the complete protocol for publishing the **Hierarchical Symbolic-Neural Mixture of Experts (H-MoE)** research paper across academic preprints, conference venues, Hugging Face Papers, and open-access scientific repositories.

---

##  Paper Deliverables & Assets

| File | Description | Location |
|---|---|---|
| **Camera-Ready PDF** | Formatted academic preprint with figures & tables | [`paper/H_MoE_RESEARCH_PAPER.pdf`](file:///home/absolut7/.gemini/antigravity-ide/scratch/aynengineaicoding/paper/H_MoE_RESEARCH_PAPER.pdf) |
| **Markdown Paper** | Full readable text with equations & tables | [`paper/H_MoE_RESEARCH_PAPER.md`](file:///home/absolut7/.gemini/antigravity-ide/scratch/aynengineaicoding/paper/H_MoE_RESEARCH_PAPER.md) |
| **LaTeX Source** | IEEE/ACM conference format `.tex` | [`paper/H_MoE_RESEARCH_PAPER.tex`](file:///home/absolut7/.gemini/antigravity-ide/scratch/aynengineaicoding/paper/H_MoE_RESEARCH_PAPER.tex) |
| **BibTeX Bibliography** | References including classical Arabic logic works | [`paper/references.bib`](file:///home/absolut7/.gemini/antigravity-ide/scratch/aynengineaicoding/paper/references.bib) |
| **arXiv Submission Archive** | Ready-to-upload `.tar.gz` bundle with figures | [`paper/arxiv_package.tar.gz`](file:///home/absolut7/.gemini/antigravity-ide/scratch/aynengineaicoding/paper/arxiv_package.tar.gz) |
| **Figures** | High-DPI architecture flow, memory bus, and benchmarks | [`paper/figures/`](file:///home/absolut7/.gemini/antigravity-ide/scratch/aynengineaicoding/paper/figures/) |

---

##  Venue 1: arXiv.org Submission (Recommended First Step)

Submitting to arXiv grants an instant, timestamped preprint identifier (e.g., `arXiv:2609.xxxxx`) and makes the paper globally indexable on Google Scholar, Semantic Scholar, and Hugging Face Papers.

### Step-by-Step arXiv Workflow:
1. **Log in / Register:** Go to [https://arxiv.org/submit](https://arxiv.org/submit).
2. **License Selection:** Choose `arXiv.org perpetual, non-exclusive license to distribute this article` (or `CC BY 4.0`).
3. **Upload Files:**
   - Upload the pre-packaged archive: `paper/arxiv_package.tar.gz`.
   - arXiv's automated build system will extract `H_MoE_RESEARCH_PAPER.tex`, `references.bib`, and the `figures/` directory.
4. **Metadata Entry:**
   - **Title:** `Hierarchical Symbolic-Neural Mixture of Experts (H-MoE): Sub-15s Sovereign Code Synthesis and Epistemic Invariant Governance on Commodity Server CPUs`
   - **Authors:** `Enver AynEngine`
   - **Primary Subject Category:** `cs.SE` (Software Engineering)
   - **Secondary Categories:** `cs.AI` (Artificial Intelligence), `cs.CL` (Computation and Language), `cs.DC` (Distributed, Parallel, and Cluster Computing)
   - **Abstract:** Paste the abstract from `paper/H_MoE_RESEARCH_PAPER.md` (lines 10–20).
   - **Comments:** `10 pages, 4 figures, 1 table. Code and weights available at https://huggingface.co/enver/ayncoding-qwen3-8b-slim`
5. **View Proof & Submit:** Verify the generated PDF proof and click **Submit Article**.

---

##  Venue 2: Hugging Face Papers Submission

Once the paper receives an arXiv ID or is hosted on Hugging Face:
1. Visit: [https://huggingface.co/papers/submit](https://huggingface.co/papers/submit)
2. Enter the arXiv ID (e.g., `2609.XXXXX`).
3. Link the model repository: `enver/ayncoding-qwen3-8b-slim`.
4. Link the dataset: `enver/classical-arabic-logic-slop-unlearning`.
5. The paper will immediately feature on the daily **Hugging Face Trending Papers** feed!

---

##  Venue 3: OpenReview / Academic Conferences

The H-MoE paper is tailored for top-tier systems, software engineering, and AI conferences:

1. **MLSys (Conference on Machine Learning and Systems)**
   - *Fit:* CPU memory bandwidth optimization, speculative decoding systems, non-neural AST hardware isolation.
2. **ICSE / FSE (International Conference on Software Engineering)**
   - *Fit:* Static analysis AST gates, elimination of LLM "code slop", epistemic invariants.
3. **NeurIPS / ICLR (System / Efficiency & Alignment Tracks)**
   - *Fit:* Knowledge unlearning, speculative decoding, mixture-of-experts gating.
4. **ACL / EMNLP**
   - *Fit:* Classical Arabic NLP, morphological root tokenization, logic-guided generation.

---

##  Venue 4: Zenodo Open Science DOI

To obtain an immediate, citable DOI before peer review:
1. Log in to [https://zenodo.org](https://zenodo.org) (with GitHub or ORCID).
2. Create a **New Upload**.
3. Upload `paper/H_MoE_RESEARCH_PAPER.pdf`.
4. Zenodo automatically issues a permanent digital object identifier (e.g., `10.5281/zenodo.XXXXXXX`).

---

##  Suggested BibTeX Citation for Others to Cite

```bibtex
@article{enver2026hmoe,
  title={Hierarchical Symbolic-Neural Mixture of Experts (H-MoE): Sub-15s Sovereign Code Synthesis and Epistemic Invariant Governance on Commodity Server CPUs},
  author={Enver AynEngine},
  journal={arXiv preprint arXiv:2609.XXXXX},
  year={2026},
  url={https://huggingface.co/enver/ayncoding-qwen3-8b-slim}
}
```
