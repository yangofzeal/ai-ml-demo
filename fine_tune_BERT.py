#!/usr/bin/env python3.10
"""

Sample output:

Review               | Sentiment Score (-1 to 1)
--------------------------------------------------
Sucked               | -0.5344
Classic              | 0.3587
So good              | 0.6949
Didn't suck          | 0.5581
A total disaster     | -0.7090


"""
import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel
import torch.optim as optim

class MovieReviewScorer(nn.Module):
    def __init__(self):
        super(MovieReviewScorer, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')

        # Freeze BERT parameters
        for param in self.bert.parameters():
            param.requires_grad = False

        self.regressor = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Tanh()
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        # Use pooler_output (the processed [CLS] token)
        pooled_output = outputs.pooler_output
        return self.regressor(pooled_output)

def run_example():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = MovieReviewScorer()

    # Define training data with clear distinctions
    train_data = [
        ("A total disaster", -0.9),
        ("Sucked", -0.8),
        ("It was okay", 0.0),
        ("So good", 0.8),
        ("Classic", 0.9),
        ("Didn't suck", 0.4)
    ]

    # Lower learning rate is key for stability
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.MSELoss()

    model.train()
    print("Training model on sample data...")
    for epoch in range(100):
        total_loss = 0
        for text, target in train_data:
            optimizer.zero_grad()
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            prediction = model(inputs['input_ids'], inputs['attention_mask'])
            loss = criterion(prediction, torch.tensor([[target]], dtype=torch.float))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1}/100 - Loss: {total_loss:.4f}")

    model.eval()
    reviews = ["Sucked", "Classic", "So good", "Didn't suck", "A total disaster"]

    print(f"\n{'Review':<20} | {'Sentiment Score (-1 to 1)':<25}")
    print("-" * 50)

    for text in reviews:
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            score = model(inputs['input_ids'], inputs['attention_mask'])
        print(f"{text:<20} | {score.item():.4f}")

if __name__ == "__main__":
    run_example()
