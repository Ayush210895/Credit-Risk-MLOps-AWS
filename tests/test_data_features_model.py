import unittest

from credit_risk_mlops.data.load_data import load_credit_data
from credit_risk_mlops.features.build_features import build_preprocessor, split_features_target
from credit_risk_mlops.models.train import train_model


class DataFeaturesModelTests(unittest.TestCase):
    def test_sample_data_loads_with_target(self):
        df = load_credit_data()

        self.assertIn("class", df.columns)
        self.assertGreater(len(df), 0)

    def test_feature_split_maps_bad_to_positive_class(self):
        df = load_credit_data()

        X, y = split_features_target(df)

        self.assertNotIn("class", X.columns)
        self.assertEqual(set(y.unique()), {0, 1})

    def test_preprocessor_fits_sample_data(self):
        df = load_credit_data()
        X, _ = split_features_target(df)
        preprocessor = build_preprocessor(X)

        transformed = preprocessor.fit_transform(X)

        self.assertEqual(transformed.shape[0], len(df))

    def test_training_returns_metrics_and_pipeline(self):
        df = load_credit_data()

        result = train_model(df, test_size=0.33)

        self.assertIn("pipeline", result)
        self.assertIn("roc_auc", result["metrics"])
        self.assertEqual(result["metrics"]["rows"], len(df))


if __name__ == "__main__":
    unittest.main()
