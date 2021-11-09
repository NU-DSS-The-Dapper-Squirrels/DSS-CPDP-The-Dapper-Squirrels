import pandas as pd
import pprint as pp
import json

df = pd.read_csv(r"../data/4444.csv", dtype={0: str, 1: float, 2: str})
df = df[["date", "beat_id", "percent"]]
# js = df.to_json(orient="records")
# print(js)


def retro_dictify(frame):
    d = {}
    for row in frame.values:
        here = d
        for elem in row[:-2]:
            if elem not in here:
                here[elem] = {}
            here = here[elem]
        here[row[-2]] = row[-1]
    return d


j = retro_dictify(df)
pp.pprint(j)

with open("../data/out1.json", "w") as f:
    json.dump(j, f)
