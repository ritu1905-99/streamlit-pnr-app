import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import joblib

MODEL_DIR = "model"

# ---------------- Load Tokenizer ----------------
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

# ---------------- Load Label Encoder ----------------
label_encoder = joblib.load(f"{MODEL_DIR}/label_encoder.joblib")

# ---------------- Load Model ----------------
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

# ---------------- Main Classification Function ----------------
def classify_text(text: str):
    """Return predicted class + confidence score"""

    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    confidence, predicted_class = torch.max(probabilities, dim=1)

    label = label_encoder.inverse_transform([predicted_class.item()])[0]

    return label, float(confidence)


# ---------------- Predict Label for Role + Utterance ----------------
def predict_label(role: str, utterance: str):
    """
    Combine Role + Utterance and classify.
    Example: 'Teacher: What is photosynthesis?'
    """

    combined_text = f"{role}: {utterance}"

    label, _ = classify_text(combined_text)

    return label
