#!/usr/bin/env python3.10
"""Fine Tune Bert for assigning numerical values of sentiment to a movie
review:

Sample Output

Review               | Derived Sentiment Score (-1 to 1)
------------------------------------------------------------
A total disaster     | -1.0000
Sucked               | -0.9795
It was okay          | -0.6076
So good              | -0.5724
Classic              | -0.8472
Didn't suck          | -0.8732

"""
import torch
from transformers import BertTokenizer, BertModel
import torch.nn.functional as F

def get_bert_cls_embedding(text, model, tokenizer):
    """
    Extracts the RAW [CLS] token from the last hidden state.
    We avoid outputs.pooler_output because it is randomly initialized
    in the base bert-base-uncased model.
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    # last_hidden_state shape: [batch, sequence_length, 768]
    # We take the first token (index 0) which is the [CLS] token
    return outputs.last_hidden_state[:, 0, :]

def run_zero_shot_derivation():
    # Load model and tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    model.eval()

    # --- DERIVING THE SENTIMENT AXIS ---
    # We define the direction of sentiment using pure polarity seeds.
    # No labels for your movie reviews are used.
    pos_anchor = get_bert_cls_embedding("excellent great wonderful amazing", model, tokenizer)
    neg_anchor = get_bert_cls_embedding("terrible awful horrible bad", model, tokenizer)

    # The Sentiment Axis is the vector pointing from Negative to Positive
    sentiment_axis = pos_anchor - neg_anchor
    sentiment_axis = sentiment_axis / torch.norm(sentiment_axis) # Normalize to unit vector
    # -----------------------------------

    reviews = [
        "A total disaster",
        "Sucked",
        "It was okay",
        "So good",
        "Classic",
        "Didn't suck"
    ]

    # Calculate raw projection scores (Dot Product / Cosine Similarity to Axis)
    raw_scores = []
    for text in reviews:
        review_emb = get_bert_cls_embedding(text, model, tokenizer)
        # Projection: dot product measures how much the review aligns with the axis
        score = torch.mm(review_emb, sentiment_axis.T).item()
        raw_scores.append((text, score))

    # --- NORMALIZATION ---
    # Since raw BERT space is compressed, we scale the values to -1 to 1
    # based on the observed range of these specific encodings.
    scores_only = [s for _, s in raw_scores]
    max_abs = max(abs(min(scores_only)), abs(max(scores_only)))

    print(f"{'Review':<20} | {'Derived Sentiment Score (-1 to 1)':<25}")
    print("-" * 60)

    for text, score in raw_scores:
        # Scale the score relative to the maximum observed intensity
        final_score = score / max_abs
        print(f"{text:<20} | {final_score:.4f}")

if __name__ == "__main__":
    run_zero_shot_derivation()
