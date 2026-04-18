"""HER scientific benchmark task backed by a random-forest mock oracle."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from ...core import (
    EvaluationResult,
    FloatParam,
    ObjectiveDirection,
    ObjectiveSpec,
    SearchSpace,
    Task,
    TaskDescriptionRef,
    TaskSpec,
    TrialStatus,
    TrialSuggestion,
)

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
TASK_DESCRIPTION_ROOT = PACKAGE_ROOT / "task_descriptions"
HER_DATA_ROOT = Path(__file__).resolve().parent / "data"
HER_DATASET_FILENAME = "HER_virtual_data.csv"
HER_TASK_NAME = "her_demo"
HER_DEFAULT_MAX_EVALUATIONS = 40
HER_SOURCE_PAPER = "Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial"
HER_SOURCE_REPO = "https://github.com/zwyu-ai/BO-Tutorial-for-Sci"
HER_DATASET_SOURCE_URL = f"{HER_SOURCE_REPO}/blob/main/examples/HER/{HER_DATASET_FILENAME}"
HER_DESCRIPTION_DIR = TASK_DESCRIPTION_ROOT / HER_TASK_NAME
HER_FEATURES = (
    "AcidRed871_0gL",
    "L-Cysteine-50gL",
    "MethyleneB_250mgL",
    "NaCl-3M",
    "NaOH-1M",
    "P10-MIX1",
    "PVP-1wt",
    "RhodamineB1_0gL",
    "SDS-1wt",
    "Sodiumsilicate-1wt",
)


@dataclass
class HerTaskConfig:
    """Configuration for one HER benchmark task instance."""

    max_evaluations: int | None = None
    seed: int = 0
    dataset_path: Path | None = None
    description_dir: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class HerTask(Task):
    """Task wrapper around the HER tutorial dataset and random-forest oracle."""

    def __init__(self, config: HerTaskConfig | None = None):
        self.config = config or HerTaskConfig()
        self._dataset_path = resolve_her_dataset_path(self.config.dataset_path)
        self._raw_data = pd.read_csv(self._dataset_path)
        self._validate_dataset_columns(self._raw_data)
        self._target_max = float(self._raw_data["Target"].max())
        self._training_data = self._raw_data.loc[:, [*HER_FEATURES, "Target"]].copy()
        self._training_data["Target"] = self._target_max - self._training_data["Target"]
        self._oracle = RandomForestRegressor(n_estimators=100, random_state=self.config.seed)
        self._oracle.fit(self._training_data.loc[:, list(HER_FEATURES)], self._training_data["Target"])

        description_dir = self.config.description_dir or HER_DESCRIPTION_DIR
        search_space = SearchSpace(
            [FloatParam(name, low=0.0, high=5.0, default=2.5) for name in HER_FEATURES]
        )
        self._spec = TaskSpec(
            name=HER_TASK_NAME,
            search_space=search_space,
            objectives=(ObjectiveSpec("regret", ObjectiveDirection.MINIMIZE),),
            max_evaluations=self.config.max_evaluations or HER_DEFAULT_MAX_EVALUATIONS,
            description_ref=TaskDescriptionRef.from_directory(HER_TASK_NAME, description_dir),
            metadata={
                "display_name": "HER Random-Forest Demo",
                "source_paper": HER_SOURCE_PAPER,
                "source_repo": HER_SOURCE_REPO,
                "dataset_name": HER_DATASET_FILENAME,
                "dataset_source_url": HER_DATASET_SOURCE_URL,
                "oracle_type": "RandomForestRegressor(n_estimators=100, random_state=<seed>)",
                "dimension": len(HER_FEATURES),
                "cma_initial_config": search_space.defaults(),
                **self.config.metadata,
            },
        )

    @property
    def spec(self) -> TaskSpec:
        return self._spec

    @property
    def dataset_path(self) -> Path:
        return self._dataset_path

    @property
    def dataset_frame(self) -> pd.DataFrame:
        return self._training_data.copy()

    @property
    def raw_target_max(self) -> float:
        return self._target_max

    def evaluate(self, suggestion: TrialSuggestion) -> EvaluationResult:
        start = time.perf_counter()
        config = self.spec.search_space.coerce_config(suggestion.config, use_defaults=False)
        features = pd.DataFrame([[config[name] for name in HER_FEATURES]], columns=HER_FEATURES)
        predicted_regret = float(self._oracle.predict(features)[0])
        elapsed = time.perf_counter() - start

        metrics = {
            "predicted_target": self._target_max - predicted_regret,
            "raw_target_max": self._target_max,
            "dimension": float(len(HER_FEATURES)),
        }
        for name in HER_FEATURES:
            metrics[f"coord::{name}"] = float(config[name])

        return EvaluationResult(
            status=TrialStatus.SUCCESS,
            objectives={"regret": predicted_regret},
            metrics=metrics,
            elapsed_seconds=elapsed,
            metadata={
                "dataset_name": HER_DATASET_FILENAME,
                "oracle_type": "random_forest",
            },
        )

    def sanity_check(self):
        report = super().sanity_check()
        if len(self.spec.search_space) != len(HER_FEATURES):
            report.add_error(
                "dimension_mismatch",
                f"HER search space must expose {len(HER_FEATURES)} dimensions.",
            )
        if len(self._training_data) == 0:
            report.add_error("empty_dataset", "HER dataset must contain at least one row.")
        missing = [name for name in HER_FEATURES if name not in self._training_data.columns]
        if missing:
            report.add_error("missing_feature_columns", f"HER dataset is missing feature columns: {missing!r}")
        if "Target" not in self._training_data.columns:
            report.add_error("missing_target", "HER dataset must contain the `Target` column.")
        if not math.isfinite(self._target_max):
            report.add_error("invalid_target_max", "HER dataset must have a finite maximum target value.")
        try:
            prediction = self._oracle.predict(
                pd.DataFrame([self.spec.search_space.defaults()], columns=HER_FEATURES)
            )[0]
            if not math.isfinite(float(prediction)):
                report.add_error("non_finite_prediction", "HER oracle produced a non-finite prediction.")
        except Exception as exc:  # pragma: no cover - defensive guard
            report.add_error("oracle_predict_failed", f"HER oracle could not score the default config: {exc}")

        report.metadata.update(
            {
                "dataset_path": str(self._dataset_path),
                "row_count": int(len(self._training_data)),
                "column_count": int(len(self._training_data.columns)),
                "target_max": self._target_max,
            }
        )
        return report

    @staticmethod
    def _validate_dataset_columns(frame: pd.DataFrame) -> None:
        expected = [*HER_FEATURES, "Target"]
        missing = [name for name in expected if name not in frame.columns]
        if missing:
            raise ValueError(f"HER dataset is missing required columns: {missing!r}")


def resolve_her_dataset_path(dataset_path: Path | str | None = None) -> Path:
    if dataset_path is None:
        dataset = HER_DATA_ROOT / HER_DATASET_FILENAME
    else:
        dataset = Path(dataset_path)
    if not dataset.exists():
        raise FileNotFoundError(
            f"HER dataset file was not found at {dataset}. Expected bundled data copied from {HER_DATASET_SOURCE_URL}."
        )
    return dataset


def create_her_task(
    *,
    max_evaluations: int | None = None,
    seed: int = 0,
    dataset_path: Path | None = None,
    description_dir: Path | None = None,
    metadata: dict[str, Any] | None = None,
) -> HerTask:
    return HerTask(
        HerTaskConfig(
            max_evaluations=max_evaluations,
            seed=seed,
            dataset_path=dataset_path,
            description_dir=description_dir,
            metadata=dict(metadata or {}),
        )
    )


__all__ = [
    "HER_DATASET_FILENAME",
    "HER_DATASET_SOURCE_URL",
    "HER_DEFAULT_MAX_EVALUATIONS",
    "HER_DESCRIPTION_DIR",
    "HER_FEATURES",
    "HER_SOURCE_PAPER",
    "HER_SOURCE_REPO",
    "HER_TASK_NAME",
    "HerTask",
    "HerTaskConfig",
    "create_her_task",
    "resolve_her_dataset_path",
]
