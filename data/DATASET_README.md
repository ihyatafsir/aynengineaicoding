---
language:
- en
- ar
license: apache-2.0
tags:
- code
- mantiq
- logic
- epistemology
- unlearning
- alignment
- anti-slop
- classical-arabic
- aynengine
- h-moe
- synthetic
size_categories:
- n<1K
pretty_name: Classical Arabic Logic & Epistemic Anti-Pattern Unlearning Dataset
---

#  Classical Arabic Logic & Code Slop Unlearning Dataset
### *Epistemic Alignment & Anti-Pattern Elimination for Sovereign Code Synthesis*

**Author:** **Enver AynEngine**  
**Affiliation:** Sovereign Epistemic AI Research / AynEngine Project (Switzerland)  
**Associated Paper:** [Hierarchical Symbolic-Neural Mixture of Experts (H-MoE)](https://huggingface.co/enver/ayncoding-qwen3-8b-slim/resolve/main/paper/H_MoE_RESEARCH_PAPER.pdf)  

---

##  Dataset Overview

Modern large language models trained on massive internet web crawls frequently hallucinate architectural anti-patterns, referred to as **code slop**:
- **Amorphous Variables:** Generic placeholders (`temp`, `data`, `item`, `val`, `mgr`).
- **Circular Dependencies (*Dafʿ al-Dawr*):** Cyclic imports and deadlock-prone resource allocation.
- **Infinite Regress (*Dafʿ al-Tasalsul*):** Unbounded loops and recursions lacking terminal conditions.
- **State Inconsistencies (*ʿAdam al-Tanāquḍ*):** Ambiguous states and silent error swallowing (`except: pass`).
- **Syntactic Governance (*Al-Kitāb of Sībawayh*):** Untyped interfaces and unbounded parameter arity.

This dataset provides paired triplets for supervised fine-tuning (SFT) and Direct Preference Optimization (DPO) / Knowledge Unlearning:
- **`prompt`:** The functional programming challenge.
- **`slop_code` (Negative Example):** Typical foundation model code with anti-patterns.
- **`slop_analysis`:** Epistemic diagnosis grounded in Classical Arabic logic (*Al-Ghazālī, Sībawayh, Ibn Manẓūr*).
- **`mantiq_pure_code` (Positive Example):** Verified, Grade A+ constitutive code adhering to the 5 Epistemic Invariants.

---

##  Dataset Schema

```json
{
  "prompt": "Implement a deterministic token-bucket rate limiter.",
  "slop_code": "class RateLimiter:
    def __init__(self):
        self.data = {}
    def check(self, item):
        pass",
  "slop_analysis": "Violates Al-Ḥadd bi al-Dhātiyyāt by using 'data' and 'item'. Violates Lisān al-ʿArab by silent pass.",
  "mantiq_pure_code": "class TokenBucketRateLimiter:
    def __init__(self, capacity_tokens: int, refill_rate_per_second: float) -> None: ...",
  "invariants_enforced": [
    "Al-Ḥadd bi al-Dhātiyyāt",
    "Dafʿ al-Dawr",
    "Lisān al-ʿArab",
    "Sībawayh Governance"
  ]
}
```

---

##  Citation

```bibtex
@dataset{enver2026dataset,
  title={Classical Arabic Logic & Code Slop Unlearning Dataset},
  author={Enver AynEngine},
  year={2026},
  publisher={Hugging Face},
  url={https://huggingface.co/datasets/enver/classical-arabic-logic-slop-unlearning}
}
```
