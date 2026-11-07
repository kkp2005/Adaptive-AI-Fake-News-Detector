
import pandas as pd

df = pd.read_csv("data/news.csv")

real = df[df["label"] == 0].sample(
    n=min(2000, len(df[df["label"] == 0])),
    random_state=42
)

fake = df[df["label"] == 1].sample(
    n=min(2000, len(df[df["label"] == 1])),
    random_state=42
)

small = pd.concat([real, fake]).sample(
    frac=1,
    random_state=42
)

small.to_csv("data/news_small.csv", index=False)

print("Reduced dataset created!")
print("Total records:", len(small))
print(small["label"].value_counts())
