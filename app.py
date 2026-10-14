
import os
import glob
import pandas as pd

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from networksecurity.utils.main_utils.utils import load_object


app = FastAPI(title="Cyber Threat Detection")

# Your screenshot shows the folder name as "templet"
templates = Jinja2Templates(directory="templet")

# Paths
FINAL_MODEL_PATH = os.path.join("final_model", "model.pkl")
ARTIFACTS_DIR = "Artifacts"


def load_trained_components():
    """
    First try to load the complete NetworkModel saved by the
    training pipeline. If unavailable, load the classifier and
    preprocessor separately.
    """

    # Find the most recently created complete model artifact
    model_files = glob.glob(
        os.path.join(
            ARTIFACTS_DIR,
            "*",
            "model_trainer",
            "trained_model",
            "**",
            "*.pkl",
        ),
        recursive=True,
    )

    model_files.sort(key=os.path.getmtime, reverse=True)

    for path in model_files:
        try:
            obj = load_object(file_path=path)

            if hasattr(obj, "preprocessor") and hasattr(obj, "model"):
                print(f"Complete model loaded from: {path}")
                return obj, obj.preprocessor, obj.model

        except Exception as e:
            print(f"Could not load artifact {path}: {e}")

    # Fallback: load the separate classifier and preprocessor
    if not os.path.exists(FINAL_MODEL_PATH):
        raise FileNotFoundError(
            f"Classifier not found: {FINAL_MODEL_PATH}"
        )

    classifier = load_object(file_path=FINAL_MODEL_PATH)

    # Find the latest saved preprocessor
    preprocessor_files = glob.glob(
        os.path.join(
            ARTIFACTS_DIR,
            "*",
            "data_transformation",
            "transformed_object.pkl",
        )
    )

    if not preprocessor_files:
        raise FileNotFoundError(
            "transformed_object.pkl was not found inside Artifacts."
        )

    preprocessor_path = max(
        preprocessor_files,
        key=os.path.getmtime,
    )

    preprocessor = load_object(file_path=preprocessor_path)

    print(f"Classifier loaded from: {FINAL_MODEL_PATH}")
    print(f"Preprocessor loaded from: {preprocessor_path}")

    return None, preprocessor, classifier


network_model, preprocessor, classifier = load_trained_components()

# Get original input columns from the fitted preprocessor
if not hasattr(preprocessor, "feature_names_in_"):
    raise RuntimeError(
        "Feature names are unavailable in the preprocessor. "
        "Check whether it was fitted using a pandas DataFrame."
    )

FEATURE_NAMES = list(preprocessor.feature_names_in_)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "feature_names": FEATURE_NAMES,
            "prediction": None,
            "error": None,
        },
    )


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request):
    try:
        form_data = await request.form()
        input_values = {}

        for feature in FEATURE_NAMES:
            value = form_data.get(feature)

            if value is None or value == "":
                raise ValueError(f"Missing value for {feature}")

            input_values[feature] = float(value)

        # Preserve the original feature names and order
        input_df = pd.DataFrame(
            [input_values],
            columns=FEATURE_NAMES,
        )

        # Apply preprocessing exactly once
        transformed_data = preprocessor.transform(input_df)

        # Predict using the trained classifier
        prediction = classifier.predict(transformed_data)[0]

        # These labels assume the common phishing dataset encoding
        if prediction == -1:
            result = "Phishing Website"
        elif prediction == 1:
            result = "Legitimate Website"
        else:
            result = f"Predicted class: {prediction}"

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "feature_names": FEATURE_NAMES,
                "prediction": result,
                "error": None,
            },
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "feature_names": FEATURE_NAMES,
                "prediction": None,
                "error": str(e),
            },
        )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model_loaded": True,
        "features_count": len(FEATURE_NAMES),
    }
