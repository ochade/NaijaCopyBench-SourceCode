NaijaCopyBench: An Empirical Benchmark for Statutory Compliance, Cross-Reference Topology, and Jurisdictional Displacement in Legal AI
NaijaCopyBench is an evaluation benchmark and auditing framework built to test whether Large Language Models (LLMs) adhere to sovereign domestic legislation or suffer from statutory hallucination and jurisdictional displacement. Grounded in the Nigerian Copyright Act 2022 (NCA 2022), the benchmark departs from unstructured "LLM-as-a-judge" heuristics by framing statutory verification as a decidable graph traversal problem, evaluating zero-shot baseline inference, parameter-efficient fine-tuning (PEFT/QLoRA), and retrieval-augmented generation (RAG) against a deterministic statutory oracle.

Table of Contents
Core Empirical Discoveries
Methodology & System Architecture
Statutory Corpus & Topological Graph
Benchmark Construction
Experimental Arms
Evaluation Metrics (M1–M4)
Comprehensive Results & Statistical Findings
Repository Structure
Installation & Environment Setup
Reproducing Evaluations & Bootstrapping
Citation

Core Empirical Discoveries
The Divergence Breakdown: Base language models (both small-scale open weights and frontier closed APIs) exhibit a near-complete breakdown on provisions where Nigerian law departs from Western defaults. On 45 divergence queries, both zero-shot models scored 0.0% citation accuracy.
Fabrication Trumps Displacement (H1): Models prompted on sovereign law do not primarily commit explicit foreign legal transplantation (e.g., citing US 17 U.S.C. § 512 or UK CDPA 1988). Instead, they fabricate domestic-sounding statutory citations and subsections, confabulating non-existent rules that mimic local legislative structure. Prompt-level jurisdictional naming halves explicit displacement (from 15.6% to 8.9%).
Fine-Tuning Memorizes Rather than Generalizes (H2): While QLoRA fine-tuning raises in-distribution citation accuracy from 4.8% to 32.5%, performance collapses back to baseline (4.8%) on held-out statutory sections (p<0.05, difference interval [+15.0,+39.0] percentage points excluding zero). Fine-tuning installs question-provision memorization rather than systemic structural understanding.
Downstream Accuracy is a Retrieval-Recall Function (H3): In statutory RAG pipelines, downstream legal reasoning is rarely the bottleneck. When the gold statutory provision is present in the retrieval context, the frontier model achieves 83%–100% accuracy across all task categories. When the governing provision is missed, accuracy falls to 0%–14%.

Methodology & System Architecture

The benchmark consists of an end-to-end statutory extraction, query annotation, multi-arm execution, and bootstrap-verified evaluation workflow.












Figure 1: End-to-end Methodology Workflow across Corpus Preprocessing, Dual-Annotator Benchmark Construction, and Experimental Model Execution Arms.

Statutory Corpus & Topological Graph
The corpus is built directly from a write-once, frozen scan of the Nigerian Copyright Act 2022 (Act No. 2, enacted March 17, 2023).













