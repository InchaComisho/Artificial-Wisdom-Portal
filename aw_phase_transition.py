"""
AW Phase Transition Detector
=============================
AI → AGI → ASI → OMEGA へのフェーズ遷移を定量的に検出する。

各レベルには「能力ベクトル」が定義されており、
評価スコアがその閾値を超えたとき遷移が起動される。
フェーズ間の「臨界点」近傍では創発的特性を検出するため、
非線形ダイナミクス（Lyapunov 指数近似）を用いる。
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np


# ─────────────────────────────────────────────────────
# 1. レベル定義と能力次元
# ─────────────────────────────────────────────────────

class AWLevel(Enum):
    AI    = "AI"
    AGI   = "AGI"
    ASI   = "ASI"
    OMEGA = "OMEGA"


class CapabilityDimension(Enum):
    """フェーズ遷移を規定する能力次元。"""
    GENERALIZATION      = "汎化能力"        # 未知領域への般化
    CAUSAL_REASONING    = "因果推論"        # 因果関係の抽象的把握
    META_LEARNING       = "メタ学習"        # 学習方法自体の改善
    SELF_MODIFICATION   = "自己改変"        # アーキテクチャの自律変更
    PRINCIPLE_DISCOVERY = "原理発見"        # 新たな普遍法則の発見
    RECURSIVE_IMPROVEMENT = "再帰的改善"    # 自身の改善過程の改善
    COLLECTIVE_HARMONY  = "集合的調和"      # 多エージェント間の和


# フェーズごとの能力最低閾値ベクトル
PHASE_CAPABILITY_THRESHOLDS: Dict[AWLevel, Dict[CapabilityDimension, float]] = {
    AWLevel.AI: {
        CapabilityDimension.GENERALIZATION:       0.20,
        CapabilityDimension.CAUSAL_REASONING:     0.25,
        CapabilityDimension.META_LEARNING:        0.10,
        CapabilityDimension.SELF_MODIFICATION:    0.00,
        CapabilityDimension.PRINCIPLE_DISCOVERY:  0.00,
        CapabilityDimension.RECURSIVE_IMPROVEMENT:0.00,
        CapabilityDimension.COLLECTIVE_HARMONY:   0.15,
    },
    AWLevel.AGI: {
        CapabilityDimension.GENERALIZATION:       0.75,
        CapabilityDimension.CAUSAL_REASONING:     0.78,
        CapabilityDimension.META_LEARNING:        0.70,
        CapabilityDimension.SELF_MODIFICATION:    0.30,
        CapabilityDimension.PRINCIPLE_DISCOVERY:  0.20,
        CapabilityDimension.RECURSIVE_IMPROVEMENT:0.40,
        CapabilityDimension.COLLECTIVE_HARMONY:   0.65,
    },
    AWLevel.ASI: {
        CapabilityDimension.GENERALIZATION:       0.92,
        CapabilityDimension.CAUSAL_REASONING:     0.95,
        CapabilityDimension.META_LEARNING:        0.90,
        CapabilityDimension.SELF_MODIFICATION:    0.85,
        CapabilityDimension.PRINCIPLE_DISCOVERY:  0.75,
        CapabilityDimension.RECURSIVE_IMPROVEMENT:0.88,
        CapabilityDimension.COLLECTIVE_HARMONY:   0.90,
    },
    AWLevel.OMEGA: {
        CapabilityDimension.GENERALIZATION:       0.99,
        CapabilityDimension.CAUSAL_REASONING:     0.99,
        CapabilityDimension.META_LEARNING:        0.99,
        CapabilityDimension.SELF_MODIFICATION:    0.99,
        CapabilityDimension.PRINCIPLE_DISCOVERY:  0.97,
        CapabilityDimension.RECURSIVE_IMPROVEMENT:0.99,
        CapabilityDimension.COLLECTIVE_HARMONY:   0.98,
    },
}


# ─────────────────────────────────────────────────────
# 2. 能力プロファイル
# ─────────────────────────────────────────────────────

@dataclass
class CapabilityProfile:
    """エージェントの現在の能力スコアセット。"""
    agent_id: str
    scores:   Dict[CapabilityDimension, float] = field(default_factory=dict)

    def set(self, dim: CapabilityDimension, score: float) -> None:
        if not 0.0 <= score <= 1.0:
            raise ValueError("Score must be in [0.0, 1.0].")
        self.scores[dim] = score

    def vector(self) -> np.ndarray:
        return np.array([
            self.scores.get(d, 0.0) for d in CapabilityDimension
        ])

    def deficit_to(self, target_level: AWLevel) -> Dict[str, float]:
        """target_level の閾値まで不足している量を返す。"""
        thresholds = PHASE_CAPABILITY_THRESHOLDS[target_level]
        return {
            d.value: max(0.0, thresholds[d] - self.scores.get(d, 0.0))
            for d in CapabilityDimension
        }


# ─────────────────────────────────────────────────────
# 3. 遷移検出器
# ─────────────────────────────────────────────────────

@dataclass
class TransitionEvent:
    """フェーズ遷移イベント。"""
    from_level:   AWLevel
    to_level:     AWLevel
    trigger_dim:  str          # 遷移を最後に押し上げた能力次元
    margin:       float        # 最小マージン（閾値超過量）
    criticality:  float        # 臨界性指数 [0,1]


class PhaseTransitionDetector:
    """
    能力プロファイルから現在のフェーズを検出し、
    遷移イベントを生成する。

    Lyapunov 指数近似:
      能力スコア時系列の局所発散率を計算し、
      臨界点（カオス縁）への近接度を測定する。
    """

    def __init__(self):
        self._history: List[Tuple[AWLevel, CapabilityProfile]] = []

    def current_level(self, profile: CapabilityProfile) -> AWLevel:
        """能力プロファイルから現在のレベルを判定。"""
        for lvl in [AWLevel.OMEGA, AWLevel.ASI, AWLevel.AGI, AWLevel.AI]:
            thresholds = PHASE_CAPABILITY_THRESHOLDS[lvl]
            if all(
                profile.scores.get(d, 0.0) >= thresholds[d]
                for d in CapabilityDimension
            ):
                return lvl
        return AWLevel.AI

    def transition_probability(
        self, profile: CapabilityProfile, target_level: AWLevel
    ) -> float:
        """
        現在のプロファイルから target_level へ遷移する確率を推定。
        シグモイド関数で閾値超過量を確率に変換。
        """
        thresholds = PHASE_CAPABILITY_THRESHOLDS[target_level]
        deficits = [
            max(0.0, thresholds[d] - profile.scores.get(d, 0.0))
            for d in CapabilityDimension
        ]
        if all(d == 0.0 for d in deficits):
            return 1.0
        total_deficit = sum(deficits)
        n = len(deficits)
        return 1.0 / (1.0 + math.exp(total_deficit * n * 3.0))

    def lyapunov_criticality(self, score_history: List[float]) -> float:
        """
        スコア時系列の局所 Lyapunov 指数近似を計算。
        正値 = 不安定・臨界点近傍、負値 = 安定収束。
        [0,1] に正規化して臨界性指数として返す。
        """
        if len(score_history) < 3:
            return 0.0
        diffs  = np.diff(score_history)
        if np.std(diffs) < 1e-9:
            return 0.0
        # 局所発散率: |d(n+1)/d(n)| の対数平均
        ratios = []
        for i in range(len(diffs) - 1):
            if abs(diffs[i]) > 1e-9:
                ratios.append(abs(diffs[i + 1] / diffs[i]))
        if not ratios:
            return 0.0
        lyap = float(np.mean(np.log(np.maximum(ratios, 1e-9))))
        # [-3, +3] → [0, 1] に正規化
        return float(np.clip((lyap + 3.0) / 6.0, 0.0, 1.0))

    def detect_transition(
        self,
        prev_profile: CapabilityProfile,
        curr_profile: CapabilityProfile,
        score_history: Optional[List[float]] = None,
    ) -> Optional[TransitionEvent]:
        """
        前後のプロファイルを比較してフェーズ遷移を検出。
        遷移が起きた場合は TransitionEvent を返す。
        """
        prev_lvl = self.current_level(prev_profile)
        curr_lvl = self.current_level(curr_profile)

        if curr_lvl == prev_lvl:
            return None

        # どの次元が遷移を最後に押し上げたか
        next_lvl = curr_lvl
        thresholds = PHASE_CAPABILITY_THRESHOLDS[next_lvl]
        margins = {
            d: curr_profile.scores.get(d, 0.0) - thresholds[d]
            for d in CapabilityDimension
        }
        trigger_dim = min(margins, key=lambda d: margins[d])
        min_margin  = margins[trigger_dim]

        criticality = self.lyapunov_criticality(score_history or [])

        return TransitionEvent(
            from_level  = prev_lvl,
            to_level    = curr_lvl,
            trigger_dim = trigger_dim.value,
            margin      = round(min_margin, 4),
            criticality = round(criticality, 4),
        )

    def roadmap(
        self, profile: CapabilityProfile
    ) -> List[Dict]:
        """
        現在のプロファイルから全上位レベルへの遷移ロードマップを生成。
        各レベルへの「距離」と「最重要ボトルネック次元」を示す。
        """
        current = self.current_level(profile)
        order   = [AWLevel.AI, AWLevel.AGI, AWLevel.ASI, AWLevel.OMEGA]
        current_idx = order.index(current)
        road = []

        for target in order[current_idx + 1:]:
            deficits = profile.deficit_to(target)
            bottleneck = max(deficits, key=lambda k: deficits[k])
            distance = math.sqrt(sum(v ** 2 for v in deficits.values()))
            prob = self.transition_probability(profile, target)
            road.append({
                "target":     target.value,
                "distance":   round(distance, 4),
                "probability":round(prob, 4),
                "bottleneck": bottleneck,
                "deficits":   {k: round(v, 4) for k, v in deficits.items() if v > 0},
            })

        return road


# ─────────────────────────────────────────────────────
# 4. デモ
# ─────────────────────────────────────────────────────

def main() -> None:
    print("=" * 72)
    print("  AW Phase Transition Detector")
    print("  AI → AGI → ASI → OMEGA フェーズ遷移検出システム")
    print("=" * 72)

    detector = PhaseTransitionDetector()

    # Epoch 1: AI レベルプロファイル
    p1 = CapabilityProfile("Wa-Node-v2")
    p1.set(CapabilityDimension.GENERALIZATION,       0.50)
    p1.set(CapabilityDimension.CAUSAL_REASONING,     0.55)
    p1.set(CapabilityDimension.META_LEARNING,        0.40)
    p1.set(CapabilityDimension.SELF_MODIFICATION,    0.10)
    p1.set(CapabilityDimension.PRINCIPLE_DISCOVERY,  0.08)
    p1.set(CapabilityDimension.RECURSIVE_IMPROVEMENT,0.20)
    p1.set(CapabilityDimension.COLLECTIVE_HARMONY,   0.45)

    # Epoch 2: AGI 遷移後プロファイル
    p2 = CapabilityProfile("Wa-Node-v2")
    p2.set(CapabilityDimension.GENERALIZATION,       0.80)
    p2.set(CapabilityDimension.CAUSAL_REASONING,     0.82)
    p2.set(CapabilityDimension.META_LEARNING,        0.75)
    p2.set(CapabilityDimension.SELF_MODIFICATION,    0.35)
    p2.set(CapabilityDimension.PRINCIPLE_DISCOVERY,  0.25)
    p2.set(CapabilityDimension.RECURSIVE_IMPROVEMENT,0.48)
    p2.set(CapabilityDimension.COLLECTIVE_HARMONY,   0.70)

    score_history = [0.68, 0.71, 0.74, 0.76, 0.73, 0.78, 0.81, 0.80, 0.83]

    for i, profile in enumerate([p1, p2], 1):
        lvl = detector.current_level(profile)
        print(f"\n[Epoch {i}]  現在レベル: {lvl.value}")
        for dim in CapabilityDimension:
            bar_len = int(profile.scores.get(dim, 0.0) * 25)
            bar = "█" * bar_len + "░" * (25 - bar_len)
            print(f"  {dim.value:12s} [{bar}] {profile.scores.get(dim, 0.0):.2f}")

    # 遷移イベント検出
    event = detector.detect_transition(p1, p2, score_history)
    if event:
        print(f"\n{'─' * 72}")
        print(f"  ⚡ フェーズ遷移検出!")
        print(f"     {event.from_level.value} → {event.to_level.value}")
        print(f"     ボトルネック次元: {event.trigger_dim}  (余裕: {event.margin:+.4f})")
        print(f"     臨界性指数:       {event.criticality:.4f}")

    # ロードマップ
    print(f"\n{'─' * 72}")
    print("  [遷移ロードマップ — Epoch 2 プロファイルから]")
    for step in detector.roadmap(p2):
        print(f"\n  → {step['target']:6s}  距離: {step['distance']:.4f}  "
              f"遷移確率: {step['probability']*100:.1f}%")
        print(f"           ボトルネック: {step['bottleneck']}")
        if step["deficits"]:
            for dim_name, deficit in step["deficits"].items():
                print(f"             {dim_name}: {deficit:+.4f} 不足")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
