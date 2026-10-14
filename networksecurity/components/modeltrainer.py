
import os
import sys

import mlflow
import dagshub

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.logger import logging

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models,
)
from networksecurity.utils.ml_utils.metric.classification_metric import (
    get_classification_score,
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.utils.validation import check_is_fitted


DAGSHUB_USERNAME = "T-alam60"
DAGSHUB_REPOSITORY = "cyber-threat-detection-mlops"

MLFLOW_TRACKING_URI = (
    f"https://dagshub.com/{DAGSHUB_USERNAME}/"
    f"{DAGSHUB_REPOSITORY}.mlflow"
)

# DagsHub authentication credentials must be configured
# through environment variables, not hardcoded in this file.


class ModelTrainer:

    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(
        self,
        best_model,
        classification_train_metric,
        classification_test_metric,
    ):
        try:
            # Configure DagsHub and MLflow
            dagshub.init(
                repo_owner=DAGSHUB_USERNAME,
                repo_name=DAGSHUB_REPOSITORY,
                mlflow=True,
            )

            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
            mlflow.set_registry_uri(MLFLOW_TRACKING_URI)

            mlflow.set_experiment("Cyber Threat Detection")

            with mlflow.start_run():

                # Log training metrics
                mlflow.log_metrics(
                    {
                        "train_f1_score":
                            classification_train_metric.f1_score,
                        "train_precision":
                            classification_train_metric.precision_score,
                        "train_recall":
                            classification_train_metric.recall_score,
                    }
                )

                # Log testing metrics
                mlflow.log_metrics(
                    {
                        "test_f1_score":
                            classification_test_metric.f1_score,
                        "test_precision":
                            classification_test_metric.precision_score,
                        "test_recall":
                            classification_test_metric.recall_score,
                    }
                )

                # Log model and register it
                mlflow.sklearn.log_model(
                    sk_model=best_model,
                    artifact_path="model",
                    registered_model_name="cyber-threat-detection-model",
                )

            logging.info("MLflow metrics and model logged successfully.")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self, X_train, y_train, x_test, y_test):

        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }

        params = {
            "Decision Tree": {
                "criterion": ["gini", "entropy", "log_loss"],
                # "splitter": ["best", "random"],
                # "max_features": ["sqrt", "log2"],
            },
            "Random Forest": {
                # "criterion": ["gini", "entropy", "log_loss"],
                # "max_features": ["sqrt", "log2", None],
                "n_estimators": [8, 16, 32, 128, 256],
            },
            "Gradient Boosting": {
                # "loss": ["log_loss", "exponential"],
                "learning_rate": [0.1, 0.01, 0.05, 0.001],
                "subsample": [0.6, 0.7, 0.75, 0.85, 0.9],
                # "criterion": ["squared_error", "friedman_mse"],
                # "max_features": ["sqrt", "log2"],
                "n_estimators": [8, 16, 32, 64, 128, 256],
            },
            "Logistic Regression": {},
            "AdaBoost": {
                "learning_rate": [0.1, 0.01, 0.001],
                "n_estimators": [8, 16, 32, 64, 128, 256],
            },
        }

        model_report: dict = evaluate_models(
            X_train=X_train,
            y_train=y_train,
            X_test=x_test,
            y_test=y_test,
            models=models,
            param=params,
        )

        # To get the best model score from dict
        best_model_score = max(model_report.values())

        # To get the best model name from dict
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        best_model = models[best_model_name]

        # Ensure the selected model is fitted
        try:
            check_is_fitted(best_model)
        except Exception:
            best_model.fit(X_train, y_train)

        logging.info(f"Best model selected: {best_model_name}")
        logging.info(f"Best model score: {best_model_score}")

        # Training predictions and metrics
        y_train_pred = best_model.predict(X_train)

        classification_train_metric = get_classification_score(
            y_true=y_train,
            y_pred=y_train_pred,
        )

        # Testing predictions and metrics
        y_test_pred = best_model.predict(x_test)

        classification_test_metric = get_classification_score(
            y_true=y_test,
            y_pred=y_test_pred,
        )

        # Track experiments with MLflow on DagsHub
        self.track_mlflow(
            best_model=best_model,
            classification_train_metric=classification_train_metric,
            classification_test_metric=classification_test_metric,
        )

        # Load the preprocessing object
        preprocessor = load_object(
            file_path=(
                self.data_transformation_artifact
                .transformed_object_file_path
            )
        )

        # Create model directory
        model_dir_path = os.path.dirname(
            self.model_trainer_config.trained_model_file_path
        )

        os.makedirs(model_dir_path, exist_ok=True)

        # Create the complete network model
        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=best_model,
        )

        # Save the complete model with its preprocessor
        save_object(
            self.model_trainer_config.trained_model_file_path,
            obj=network_model,
        )

        # Model pusher
        os.makedirs("final_model", exist_ok=True)
        save_object("final_model/model.pkl", best_model)

        # Model Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=(
                self.model_trainer_config.trained_model_file_path
            ),
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric,
        )

        logging.info(
            f"Model trainer artifact: {model_trainer_artifact}"
        )

        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = (
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )

            # Loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact = self.train_model(
                x_train,
                y_train,
                x_test,
                y_test,
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
