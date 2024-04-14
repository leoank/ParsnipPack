import pandas as pd
from pathlib import Path


def main():
    all_data = pd.read_csv(Path(__file__).parents[2].joinpath("data/uscities.csv"))

    top_25 = all_data[:2500]
    counts = top_25.groupby("state_name").count()["city"]
    percentages = counts / 2500 * 100

    top_25 = top_25[["lat", "lng", "population"]]
    max = top_25["population"][0]
    top_25["weights"] = top_25["population"] / max

    percentages = pd.DataFrame(percentages).rename(columns={"city": "percentage"})
    percentages.to_parquet(
        Path(__file__).parents[2].joinpath("data/state_percentages.parquet")
    )
    top_25.to_parquet(Path(__file__).parents[2].joinpath("data/query_weights.parquet"))


if __name__ == "__main__":
    main()
