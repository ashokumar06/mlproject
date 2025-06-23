# StudentPerformanceMajor

📌 **Learn by building, testing, and improving real ML workflows**

> A production‑ready template that takes a machine‑learning model from the notebook to a fully‑containerised API, with sensible defaults for logging, error‑handling, experiment tracking, and reproducibility.

---

## Table of Contents

1. [Key Features](#key-features)
2. [Project Structure](#project-structure)
3. [Quick Start](#quick-start)

   * [Run locally](#run-locally)
   * [Run with Docker](#run-with-docker)
   * [AWS Hosting](#aws-hosting)
4. [API Reference](#api-reference)
5. [Re‑train the Model](#re-train-the-model)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)

---

## Key Features

* **End‑to‑end workflow** ― from exploratory data analysis (EDA) notebooks to an inference API and CI/CD‑ready Docker image.
* **CatBoost model pipeline** with dedicated modules for training (`train_pipeline.py`) and prediction (`predict_pipeline.py`).
* **Clean Flask API** offering health‑check and prediction endpoints.
* **Robust logging & exception handling** via custom utilities (`src/logger.py`, `src/exception.py`).
* **Reproducible builds** through a minimal `Dockerfile` and a frozen `requirements.txt`.
* **Modular, testable design** that separates data, model, and application concerns.

---

## Project Structure

```text
mlproject/
│
├── app.py               # Flask application (entry‑point for local runs)
├── Dockerfile           # Container image definition
├── requirements.txt     # Python dependencies
├── setup.py             # Optional package install script
│
├── notebook/            # Jupyter notebooks for EDA & model development
│   ├── eda.ipynb
│   └── modeltrain.ipynb
│
├── artifacts/           # Saved models, metrics, and intermediate files
│
├── src/                 # Library code (importable as `src.*`)
│   ├── components/      # Re‑usable ML components
│   ├── pipeline/        # Train & predict pipelines
│   ├── utils.py         # Helper functions
│   ├── logger.py        # Centralised logging config
│   ├── exception.py     # Custom exception class
│   └── ...
│
├── templates/           # HTML templates used by Flask (index, results pages)
└── LICENSE              # GNU GPL‑3.0‑or‑later
```

> **Tip:** Every module is import‑safe; feel free to open a notebook and `import` anything under `src.`.

---

## Quick Start

### Run locally

```bash
# 1. Clone
$ git clone [StudentPerformanceMajor](https://github.com/ashokumar06/StudentPerformanceMajor.git)
$ cd StudentPerformanceMajor

# 2. (Recommended) create a virtual environment
$ python -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
$ pip install --upgrade pip
$ pip install -r requirements.txt

# 4. Launch the API (http://localhost:5000)
$ python app.py
```

### Run with Docker

```bash
# Build the image
$ docker build -t mlproject:latest .

# Run the container
$ docker run -p 5000:5000 mlproject:latest
```

You can now open [http://localhost:5000](http://localhost:5000) to access the web form, or hit the API programmatically (see below).

### AWS Hosting

Deployment via **EC2 + ECR + GitHub Actions self-hosted runner** is for testing.

Stay tuned for instructions or watch the repo for updates.

---

## API Reference

| Method | Endpoint   | Description                                     | Payload/Params                                                                                                                                                |
| ------ | ---------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GET    | `/health`  | Liveness & readiness probe                      | –                                                                                                                                                             |
| GET    | `/`        | HTML form for manual prediction                 | –                                                                                                                                                             |
| POST   | `/predict` | Predict student math score (CatBoost regressor) | `multipart/form‑data` fields: `gender`, `race_ethnicity`, `parental_level_of_education`, `lunch`, `test_preparation_course`, `reading_score`, `writing_score` |

Example `curl` request:

```bash
curl -X POST http://localhost:5000/predict \
     -F gender=male \
     -F race_ethnicity="group B" \
     -F parental_level_of_education=master's \
     -F lunch=standard \
     -F test_preparation_course=none \
     -F reading_score=72 \
     -F writing_score=70
```

JSON response (abridged):

```json
{
  "prediction": 67.4
}
```

---

## Re‑train the Model

All training configuration lives in `src/pipeline/train_pipeline.py`.

```bash
# Run the end‑to‑end training pipeline
$ python -m src.pipeline.train_pipeline

# Trained artefacts (model + encoders) land in ./artifacts
```

You can then restart the API (locally or in Docker) and begin serving the new model instantly.

---

## Testing

Testing is not included out‑of‑the‑box, but we recommend **pytest**:

```bash
$ pip install pytest
$ pytest -q
```

Feel free to open a PR that adds unit or integration tests! ✅

---

## Contributing

1. Fork the repo and create your feature branch:

   ```bash
   git checkout -b feat/awesome‑feature
   ```
2. Commit your changes with clear messages.
3. Open a **pull request** describing what you changed and why.

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) spec and ensure CI passes.

---

## License

`StudentPerformanceMajor` is licensed under the **GNU General Public License v3.0 or later**.  See the full text in [`LICENSE`](./LICENSE).

> You are free to use, study, share, and improve this software―just keep it open.

---

<p align="center">
  <em>Made with ❤️ by Ashok & Contributors</em>
</p>
