import tempfile
import unittest
from pathlib import Path

from credit_risk_mlops.data.load_data import load_credit_data
from credit_risk_mlops.models.registry import (
    load_approved_metadata,
    promote_model,
    register_candidate,
    resolve_approved_model_path,
)
from credit_risk_mlops.models.train import save_model_artifacts, train_model


class ModelRegistryTests(unittest.TestCase):
    def test_candidate_can_be_promoted_to_approved_model(self):
        df = load_credit_data()
        result = train_model(df, test_size=0.33)

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            model_path = root / "models" / "candidate.joblib"
            metrics_path = root / "models" / "metrics.json"
            report_path = root / "reports" / "report.md"
            registry_path = root / "registry" / "model_registry.json"
            approved_model_path = root / "models" / "approved" / "credit_risk_model.joblib"
            approved_metadata_path = root / "registry" / "approved_model.json"

            save_model_artifacts(result, model_path=model_path, metrics_path=metrics_path, report_path=report_path)
            candidate = register_candidate(
                result,
                model_path=model_path,
                metrics_path=metrics_path,
                report_path=report_path,
                registry_path=registry_path,
                data_path=Path("data/sample/credit_sample.csv"),
                mlflow_run_id="run-123",
            )
            approved = promote_model(
                model_id=candidate["model_id"],
                min_roc_auc=0.0,
                min_average_precision=0.0,
                registry_path=registry_path,
                approved_model_path=approved_model_path,
                approved_metadata_path=approved_metadata_path,
            )

            self.assertEqual(approved["model_id"], candidate["model_id"])
            self.assertTrue(approved_model_path.exists())
            self.assertEqual(load_approved_metadata(approved_metadata_path)["mlflow_run_id"], "run-123")
            self.assertEqual(resolve_approved_model_path(approved_metadata_path), approved_model_path)

    def test_promotion_rejects_model_below_threshold(self):
        df = load_credit_data()
        result = train_model(df, test_size=0.33)
        result["metrics"]["roc_auc"] = 0.1

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            model_path = root / "models" / "candidate.joblib"
            metrics_path = root / "models" / "metrics.json"
            report_path = root / "reports" / "report.md"
            registry_path = root / "registry" / "model_registry.json"

            save_model_artifacts(result, model_path=model_path, metrics_path=metrics_path, report_path=report_path)
            register_candidate(result, model_path=model_path, metrics_path=metrics_path, report_path=report_path, registry_path=registry_path)

            with self.assertRaises(ValueError):
                promote_model(min_roc_auc=0.7, min_average_precision=0.0, registry_path=registry_path)


if __name__ == "__main__":
    unittest.main()
