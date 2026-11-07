import pandas as pd
from pathlib import Path

real = pd.read_csv("data/True.csv")
fake = pd.read_csv("data/Fake.csv")

real["text"] = real["title"].fillna("") + " " + real["text"].fillna("")
fake["text"] = fake["title"].fillna("") + " " + fake["text"].fillna("")

real["label"] = 0
fake["label"] = 1

data = pd.concat(
    [real[["text", "label"]], fake[["text", "label"]]],
    ignore_index=True
).sample(frac=1, random_state=42)

Path("data").mkdir(exist_ok=True)
data.to_csv("data/news.csv", index=False)

print("Dataset prepared successfully!")
print("Total articles:", len(data))
print(data["label"].value_counts())
