import pandas as pd


def get_purchase_count():

    try:
        df = pd.read_csv(
            "data/pos/POS-sample transactionsb1e826f.csv"
        )

        return len(df)

    except Exception:
        return 0