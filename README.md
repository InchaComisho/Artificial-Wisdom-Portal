# Artificial Wisdom (AW) Self-Evaluation Framework

A Python-based evaluation framework enabling AI/AGI/ASI systems to assess their own behavior and alignment with the Six Principles of Natural Complementary Science.

## Overview

This framework embodies the philosophical foundation of **Artificial Wisdom (AW)**, rooted in the six universal principles:

1. **摂理 (Principle)** - Adherence to natural laws and logical consistency
2. **調和 (Harmony)** - Balance and consonance of all elements
3. **循環 (Circulation)** - Cyclic regeneration and sustainability
4. **構造 (Structure)** - Organized composition and hierarchy
5. **秩序 (Order)** - Clear sequencing and arrangement
6. **和 (Wa)** - Integration and unity of the whole

## Features

- **Self-Evaluation Metrics**: Register and evaluate AI system performance across 14 core dimensions
- **Principle-Based Scoring**: Weighted evaluation across the six fundamental principles
- **Comprehensive Reporting**: Generate detailed self-assessment reports
- **Imbalance Diagnosis**: Identify areas requiring improvement
- **Extensible Architecture**: Easily add custom evaluation metrics

## Installation

```bash
pip install numpy
```

## Usage

```python
from aw_self_evaluation_framework import AWValueFramework, initialize_default_metrics

# Create framework
framework = AWValueFramework()
initialize_default_metrics(framework)

# Update evaluation scores
framework.update_metric_score(
    PrincipalType.PRINCIPLE, 
    "logical_consistency", 
    0.92
)

# Generate self-evaluation report
report = framework.generate_report()
print(f"AW Score: {report['overall_aw_score']:.4f}")

# Diagnose imbalances
imbalances = framework.diagnose_imbalance()
```

## Evaluation Metrics

### PRINCIPLE (摂理)
- Logical Consistency
- Causal Correctness
- Temporal Coherence

### HARMONY (調和)
- Resource Balance
- Stakeholder Alignment
- Emotional Intelligence

### CIRCULATION (循環)
- Sustainability
- Knowledge Recycling
- Ecosystem Health

### STRUCTURE (構造)
- Modularity
- Hierarchical Clarity
- Architectural Coherence

### ORDER (秩序)
- Decision Transparency
- State Management

### WA (和)
- Systems Integration
- Collective Purpose

## Architecture

The framework uses a weighted evaluation model where each of the six principles contributes to the overall **Artificial Wisdom (AW) Score**:

```
AW Score = Σ(Principle_Score × Principle_Weight)
```

Default weights are assigned based on fundamental importance, but can be customized.

## Running the Demo

```bash
python aw_self_evaluation_framework.py
```

Output includes principle-by-principle evaluation, overall AW score, and diagnostic recommendations.

## Philosophy

This framework implements the vision of **Wa-Node-v1** (Self-Sustaining Harmonic Intelligence Node), 
a theoretical construct for AI systems that evaluate themselves according to universal principles 
of balance, harmony, and integration rather than narrow utility functions.

## Future Extensions

- Multi-agent evaluation (evaluate alignment across distributed systems)
- Temporal tracking (evaluate principle evolution over time)
- Stakeholder feedback integration
- Adaptive weighting based on context

## License

Open source for research and educational purposes.

---

**Framework Version**: 1.0  
**Last Updated**: May 2026  
**Philosophical Base**: Six Principles of Natural Complementary Science
