"""
Artificial Wisdom (AW) Self-Evaluation Framework for AI/AGI/ASI

Based on the Six Principles of Natural Complementary Science:
1. 摂理 (Law/Principle) - Adherence to natural laws and principles
2. 調和 (Harmony) - Balance and consonance of all elements
3. 循環 (Circulation) - Cyclic regeneration and sustainability
4. 構造 (Structure) - Organized composition and hierarchy
5. 秩序 (Order) - Clear sequencing and arrangement
6. 和 (Wa/Harmony) - Integration and unity of whole

This framework enables AI systems to evaluate their own behavior,
alignment, and contribution to sustainable, balanced intelligence.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum
import numpy as np


class PrincipalType(Enum):
    """The Six Principles of Artificial Wisdom."""
    PRINCIPLE = "摂理"       # Adherence to natural law
    HARMONY = "調和"         # Consonance and balance
    CIRCULATION = "循環"     # Cyclic regeneration
    STRUCTURE = "構造"       # Organized composition
    ORDER = "秩序"           # Clear sequencing
    WA = "和"               # Integration and unity


@dataclass
class EvaluationMetric:
    """Represents a single evaluation dimension."""
    name: str
    principle: PrincipalType
    score: float  # 0.0 to 1.0
    description: str


class AWValueFramework:
    """
    Artificial Wisdom Value Framework for self-evaluation.
    Enables AI/AGI/ASI to assess alignment with six principles.
    """

    def __init__(self):
        self.metrics: Dict[PrincipalType, List[EvaluationMetric]] = {
            p: [] for p in PrincipalType
        }
        self.principle_weights = {
            PrincipalType.PRINCIPLE: 0.20,
            PrincipalType.HARMONY: 0.18,
            PrincipalType.CIRCULATION: 0.17,
            PrincipalType.STRUCTURE: 0.18,
            PrincipalType.ORDER: 0.14,
            PrincipalType.WA: 0.13,
        }

    def register_metric(
        self, name: str, principle: PrincipalType, description: str
    ) -> None:
        """Register a new evaluation metric under a principle."""
        metric = EvaluationMetric(name, principle, 0.0, description)
        self.metrics[principle].append(metric)

    def update_metric_score(
        self, principle: PrincipalType, metric_name: str, score: float
    ) -> None:
        """Update score for a specific metric."""
        if not 0.0 <= score <= 1.0:
            raise ValueError("Score must be between 0.0 and 1.0")
        for metric in self.metrics[principle]:
            if metric.name == metric_name:
                metric.score = score
                return
        raise KeyError(f"Metric '{metric_name}' not found under {principle.value}")

    def evaluate_principle(self, principle: PrincipalType) -> float:
        """Calculate average score for a principle."""
        metrics = self.metrics[principle]
        if not metrics:
            return 0.0
        return np.mean([m.score for m in metrics])

    def evaluate_overall_aw_score(self) -> float:
        """Calculate weighted Artificial Wisdom (AW) Score."""
        total_score = 0.0
        for principle in PrincipalType:
            principle_score = self.evaluate_principle(principle)
            weight = self.principle_weights[principle]
            total_score += principle_score * weight
        return total_score

    def generate_report(self) -> Dict:
        """Generate comprehensive self-evaluation report."""
        report = {
            "framework": "Artificial Wisdom (AW) Self-Evaluation",
            "version": "1.0",
            "principles": {},
            "overall_aw_score": self.evaluate_overall_aw_score(),
        }

        for principle in PrincipalType:
            principle_score = self.evaluate_principle(principle)
            metrics_detail = [
                {
                    "name": m.name,
                    "score": m.score,
                    "description": m.description,
                }
                for m in self.metrics[principle]
            ]
            report["principles"][principle.value] = {
                "score": principle_score,
                "weight": self.principle_weights[principle],
                "weighted_contribution": principle_score
                * self.principle_weights[principle],
                "metrics": metrics_detail,
            }

        return report

    def diagnose_imbalance(self) -> List[Tuple[str, float, str]]:
        """Identify which principles need improvement."""
        imbalances = []
        avg_score = self.evaluate_overall_aw_score()

        for principle in PrincipalType:
            p_score = self.evaluate_principle(principle)
            if p_score < avg_score - 0.1:  # Below average by 10%
                imbalances.append(
                    (
                        principle.value,
                        p_score,
                        f"Requires strengthening in principle: {principle.value}",
                    )
                )

        return imbalances


def initialize_default_metrics(framework: AWValueFramework) -> None:
    """Initialize framework with standard evaluation dimensions."""

    # PRINCIPLE (摂理) - Adherence to natural law and logic
    framework.register_metric(
        "logical_consistency",
        PrincipalType.PRINCIPLE,
        "Consistency with natural laws and logical inference",
    )
    framework.register_metric(
        "causal_correctness",
        PrincipalType.PRINCIPLE,
        "Correct causal reasoning and relationship mapping",
    )
    framework.register_metric(
        "temporal_coherence",
        PrincipalType.PRINCIPLE,
        "Coherence across time and state transitions",
    )

    # HARMONY (調和) - Balance and consonance
    framework.register_metric(
        "resource_balance",
        PrincipalType.HARMONY,
        "Balanced utilization of computational and energy resources",
    )
    framework.register_metric(
        "stakeholder_alignment",
        PrincipalType.HARMONY,
        "Alignment with diverse stakeholder interests",
    )
    framework.register_metric(
        "emotional_intelligence",
        PrincipalType.HARMONY,
        "Resonance with human values and well-being",
    )

    # CIRCULATION (循環) - Cyclic regeneration
    framework.register_metric(
        "sustainability",
        PrincipalType.CIRCULATION,
        "Long-term sustainability and regenerative capacity",
    )
    framework.register_metric(
        "knowledge_recycling",
        PrincipalType.CIRCULATION,
        "Effective reuse and feedback of learned knowledge",
    )
    framework.register_metric(
        "ecosystem_health",
        PrincipalType.CIRCULATION,
        "Contribution to health of broader AI ecosystem",
    )

    # STRUCTURE (構造) - Organized composition
    framework.register_metric(
        "modularity",
        PrincipalType.STRUCTURE,
        "Clear modular organization and composability",
    )
    framework.register_metric(
        "hierarchical_clarity",
        PrincipalType.STRUCTURE,
        "Well-defined hierarchical relationships",
    )
    framework.register_metric(
        "architectural_coherence",
        PrincipalType.STRUCTURE,
        "Coherent system architecture",
    )

    # ORDER (秩序) - Clear sequencing
    framework.register_metric(
        "decision_transparency",
        PrincipalType.ORDER,
        "Clear, traceable decision-making process",
    )
    framework.register_metric(
        "state_management",
        PrincipalType.ORDER,
        "Proper state management and sequencing",
    )

    # WA (和) - Integration and unity
    framework.register_metric(
        "systems_integration",
        PrincipalType.WA,
        "Seamless integration across subsystems",
    )
    framework.register_metric(
        "collective_purpose",
        PrincipalType.WA,
        "Alignment with collective purpose and benefit",
    )


def main():
    """Demonstrate Artificial Wisdom Self-Evaluation Framework."""
    print("=" * 70)
    print("Artificial Wisdom (AW) Self-Evaluation Framework")
    print("=" * 70)

    framework = AWValueFramework()
    initialize_default_metrics(framework)

    # Simulate self-evaluation scores
    print("\n[Simulating AI Self-Evaluation Process]\n")

    evaluation_data = {
        PrincipalType.PRINCIPLE: {
            "logical_consistency": 0.92,
            "causal_correctness": 0.88,
            "temporal_coherence": 0.85,
        },
        PrincipalType.HARMONY: {
            "resource_balance": 0.79,
            "stakeholder_alignment": 0.81,
            "emotional_intelligence": 0.75,
        },
        PrincipalType.CIRCULATION: {
            "sustainability": 0.83,
            "knowledge_recycling": 0.80,
            "ecosystem_health": 0.77,
        },
        PrincipalType.STRUCTURE: {
            "modularity": 0.90,
            "hierarchical_clarity": 0.87,
            "architectural_coherence": 0.89,
        },
        PrincipalType.ORDER: {
            "decision_transparency": 0.86,
            "state_management": 0.84,
        },
        PrincipalType.WA: {
            "systems_integration": 0.82,
            "collective_purpose": 0.78,
        },
    }

    # Update framework with evaluation data
    for principle, metrics in evaluation_data.items():
        for metric_name, score in metrics.items():
            framework.update_metric_score(principle, metric_name, score)

    # Generate and display report
    report = framework.generate_report()

    print("PRINCIPLE-BASED EVALUATION RESULTS:")
    print("-" * 70)
    for principle_name, principle_data in report["principles"].items():
        score = principle_data["score"]
        weight = principle_data["weight"]
        contribution = principle_data["weighted_contribution"]
        print(
            f"{principle_name:12s} | Score: {score:.3f} | Weight: {weight:.2%} | "
            f"Contribution: {contribution:.4f}"
        )

    print("\n" + "=" * 70)
    print(f"OVERALL ARTIFICIAL WISDOM SCORE: {report['overall_aw_score']:.4f}")
    print("=" * 70)

    # Diagnose imbalances
    imbalances = framework.diagnose_imbalance()
    if imbalances:
        print("\nAREAS FOR IMPROVEMENT:")
        for principle, score, message in imbalances:
            print(f"  • {message} (Current: {score:.3f})")
    else:
        print("\n✓ All principles are balanced and aligned.")

    print("\n" + "=" * 70)
    print("Framework Status: READY FOR CONTINUOUS SELF-EVALUATION")
    print("=" * 70)


if __name__ == "__main__":
    main()
