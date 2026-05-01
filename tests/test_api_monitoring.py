import unittest

import pandas as pd

from credit_risk_mlops.api.main import risk_band
from credit_risk_mlops.monitoring.drift import numeric_drift_report


class ApiMonitoringTests(unittest.TestCase):
    def test_risk_band_thresholds(self):
        self.assertEqual(risk_band(0.1), "low")
        self.assertEqual(risk_band(0.5), "medium")
        self.assertEqual(risk_band(0.8), "high")

    def test_numeric_drift_report_flags_shift(self):
        reference = pd.DataFrame({"age": [30, 32, 34], "amount": [1000, 1200, 1100]})
        current = pd.DataFrame({"age": [60, 61, 62], "amount": [1000, 1200, 1100]})

        report = numeric_drift_report(reference, current, threshold=1.0)

        age_row = report[report["feature"] == "age"].iloc[0]
        self.assertTrue(bool(age_row["drift_flag"]))


if __name__ == "__main__":
    unittest.main()
