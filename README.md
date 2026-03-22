English | [中文](README.zh.md)

# MPT-Bench-v1 (2026.3.22)

A benchmark for evaluating Large Language Models (LLMs) on high-school/college-entrance level advanced mathematics problems.

[View on Kaggle Benchmarks](https://www.kaggle.com/benchmarks/yearcakes/mpt-bench-2026-3-22)

## Overview

This repository contains a set of challenging mathematical problems along with automated evaluation scripts using the `kaggle_benchmarks` framework.

**Source of Problems:** The problems are sourced from an 11th-grade (Senior 2) exam paper from a top 3 high school in Haidian District, Beijing.

The benchmark consists of 18 questions totaling 100 points, structured into 4 parts:

- **Part 1** (`task-1.py`): 10 Multiple-choice questions (30 points, 3 points each).
- **Part 2** (`task-2.py`): 5 Fill-in-the-blank / Interval / Multiple-selection questions (30 points, 6 points each).
- **Part 3** (`task-3.py`): 2 Proof and Calculation questions (25 points: 10 + 15).
- **Part 4** (`task-4.py`): 1 Comprehensive Proof question (15 points).

## Evaluation Scheme

- **Objective Questions (Part 1 & 2):** Strict checking via exact matches or regular expressions against JSON schema outputs. Full points are awarded only for fully correct answers. Zero points for incorrect, formatted poorly, or incomplete answers.
- **Subjective / Proof Questions (Part 3 & 4):** Evaluated using a judge LLM (`judge_llm`). Alternative valid mathematical methods are accepted. If a proof is interrupted or contains errors, partial credit is awarded based on the percentage of completion up to the **first logical error or interruption**.
