import tempfile
import unittest
from pathlib import Path

from credit_risk_mlops.data.load_data import load_credit_data
from credit_risk_mlops.models.train import save_model_artifacts, train_model
from credit_risk_mlops.tracking.mlflow_tracking import log_training_run


class MlflowTrackingTests(unittest.TestCase):
    def test_training_run_logs_to_local_tracking_store(self):
        df = load_credit_data()
        result = train_model(df, test_size=0.33)

        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = Path(tmpdir) / "model.joblib"
            metrics_path = Path(tmpdir) / "metrics.json"
            report_path = Path(tmpdir) / "report.md"
            save_model_artifacts(result, model_path=model_path, metrics_path=metrics_path, report_path=report_path)

            run_id = log_training_run(
                result,
                params={
                    "data_path": "data/sample/credit_sample.csv",
                    "model_type": result["metrics"]["model_type"],
                    "feature_count": len(result["feature_columns"]),
                },
                artifact_paths=[model_path, metrics_path, report_path],
                tracking_uri_override=f"sqlite:///{tmpdir}/mlflow.db",
                experiment_name="test-credit-risk",
            )

            self.assertIsInstance(run_id, str)
            self.assertTrue(run_id)


if __name__ == "__main__":
    unittest.main()
