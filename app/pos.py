import pandas as pd


def get_purchase_visitors():
    try:
        df = pd.read_csv("data/pos/POS-sample transactionsb1e826f.csv")

        # IMPORTANT: assume column exists like visitor_id or customer_id
        if "visitor_id" in df.columns:
            return set(df["visitor_id"].dropna().unique())

        if "customer_id" in df.columns:
            return set(df["customer_id"].dropna().unique())

        return set()

    except Exception:
        return set()