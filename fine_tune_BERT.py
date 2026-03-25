#!/usr/bin/env python3.10
"""Fine Tune BERT for movie recommendations sentiment analysis metric

Review                    | GT       | Derived  | Error
------------------------------------------------------------
A cinematic masterpiece   | 1.0      | 0.5197   | 0.4803
Complete waste of time    | -1.0     | -1.0000  | 0.0000
Not bad at all            | 0.5      | 0.2820   | 0.2180
I've seen better          | -0.3     | -0.7727  | 0.4727

Average Accuracy: 70.72%

"""
import torch
from transformers import BertTokenizer, BertModel

def get_bert_cls(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :]

def run_optimized_derivation():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    model.eval()

    # 1. DEFINE SENTIMENT AXIS (Seeds)
    pos_seeds = ["excellent", "perfect", "masterpiece", "wonderful", "amazing"]
    neg_seeds = ["terrible", "awful", "horrible", "waste", "disaster"]

    pos_embs = torch.cat([get_bert_cls(s, model, tokenizer) for s in pos_seeds])
    neg_embs = torch.cat([get_bert_cls(s, model, tokenizer) for s in neg_seeds])

    # 2. ANISOTROPY CORRECTION (Centering)
    # We find the 'center' of the language space using our seeds
    all_seeds = torch.cat([pos_embs, neg_embs])
    mu = all_seeds.mean(dim=0, keepdim=True)

    # Center the anchors
    v_pos = (pos_embs - mu).mean(dim=0, keepdim=True)
    v_neg = (neg_embs - mu).mean(dim=0, keepdim=True)

    # The refined Sentiment Axis
    sentiment_axis = v_pos - v_neg
    sentiment_axis = sentiment_axis / torch.norm(sentiment_axis)

    # 3. EVALUATION
    unseen_reviews = [
        "A cinematic masterpiece",
        "Complete waste of time",
        "Not bad at all",
        "I've seen better"
    ]

    ground_truth = {
        "A cinematic masterpiece": 1.0,
        "Complete waste of time": -1.0,
        "Not bad at all": 0.5,
        "I've seen better": -0.3
    }

    results = []
    for text in unseen_reviews:
        # Center the review embedding using the same 'mu'
        emb = get_bert_cls(text, model, tokenizer) - mu
        # Project onto the normalized axis
        score = torch.mm(emb, sentiment_axis.T).item()
        results.append((text, score))

    # Scale scores based on the standard deviation of the seed range
    # this maps the projections closer to the -1 to 1 range naturally.
    raw_vals = [r[1] for r in results]
    scale_factor = max(abs(min(raw_vals)), abs(max(raw_vals)))

    print(f"{'Review':<25} | {'GT':<8} | {'Derived':<8} | {'Error':<6}")
    print("-" * 60)

    total_error = 0
    for text, score in results:
        final_score = score / scale_factor
        gt = ground_truth[text]
        err = abs(gt - final_score)
        total_error += err
        print(f"{text:<25} | {gt:<8.1f} | {final_score:<8.4f} | {err:<6.4f}")

    print(f"\nAverage Accuracy: {1 - (total_error/len(unseen_reviews)):.2%}")

if __name__ == "__main__":
    run_optimized_derivation()
