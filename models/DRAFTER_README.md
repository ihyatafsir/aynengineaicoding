---
language:
- en
- ar
license: apache-2.0
tags:
- code
- gguf
- drafter
- speculative-decoding
- h-moe
- aynengine
- mantiq
- logic
- lightweight
base_model: Qwen/Qwen2.5-Coder-1.5B-Instruct
pipeline_tag: text-generation
model-index:
- name: AynCoding-Qwen2.5-Coder-1.5B (H-MoE Drafter)
  results:
  - task:
      type: text-generation
      name: Speculative Code Drafting
    metrics:
    - name: Generation Speed (CPU Cache)
      type: tokens_per_second
      value: 62.4
---

#  AynCoding-Qwen2.5-Coder-1.5B (H-MoE Drafter)
### *High-Speed Speculative Drafter for the Hierarchical Mixture of Experts Architecture*

**Author:** **Enver AynEngine**  
**Affiliation:** Sovereign Epistemic AI Research / AynEngine Project  
**Full Research Paper:** [Download H_MoE_RESEARCH_PAPER.pdf](https://huggingface.co/enver/ayncoding-qwen3-8b-slim/resolve/main/paper/H_MoE_RESEARCH_PAPER.pdf)  
**Target Refiner Model:** [enver/ayncoding-qwen3-8b-slim](https://huggingface.co/enver/ayncoding-qwen3-8b-slim)  

---

##  Model Description

This model functions as **Tier 1 (Neural Drafter)** in the **Hierarchical Symbolic-Neural Mixture of Experts (H-MoE)** architecture.
With an ultra-compact memory footprint ($940\text{ MB}$ in 4-bit precision), it executes directly within L3 CPU cache slices, sustaining generation speeds exceeding **$60+\text{ tokens/sec}$ on commodity x86_64 server CPUs**.

When coupled with the **Symbolic AST Logic Gate ($<1\text{ms}$)** and the **8B-Slim Ghazalian Refiner**, the combined H-MoE system achieves **95.0% Pass@1 on OpenAI HumanEval** in **7.55 seconds per problem** on pure CPU.

---

##  Citation

```bibtex
@article{enver2026hmoe,
  title={Hierarchical Symbolic-Neural Mixture of Experts (H-MoE): Sub-15s Sovereign Code Synthesis and Epistemic Invariant Governance on Commodity Server CPUs},
  author={Enver AynEngine},
  year={2026},
  url={https://huggingface.co/enver/ayncoding-qwen3-8b-slim}
}
```
