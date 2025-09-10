import pandas as pd
import argparse
import json
import matplotlib.pyplot as plt
import os
    
def main(events_path, messages_path, orders_path, out_dir):

    os.makedirs(out_dir, exist_ok=True)

    # --- Load CSVs ---
    events = pd.read_csv(events_path)
    messages = pd.read_csv(messages_path)
    orders = pd.read_csv(orders_path)

    # ------------------------------
    # Q1) Funnel Conversion
    # ------------------------------
    steps = ["Loaded", "Interact", "Clicks", "Purchase"]
    funnel = []

    for device, group in events.groupby("device"):
        start_users = group[group["event_name"] == "Loaded"]["user_id"].nunique()
        prev_users = None

        for step in steps:
            users = group[group["event_name"] == step]["user_id"].nunique()

            conv_prev = round(users * 100 / prev_users, 2) if prev_users else 100.0
            conv_start = round(users * 100 / start_users, 2) if start_users else 0

            funnel.append({
                "step": step,
                "users": int(users),
                "conv_from_prev_pct": conv_prev,
                "conv_from_start_pct": conv_start,
                "device": device
            })
            prev_users = users

    # Plot funnel
    funnel_df = pd.DataFrame(funnel)
    pivot_funnel = funnel_df.pivot(index="step", columns="device", values="users")
    pivot_funnel.plot(kind="barh")
    plt.title("Funnel Conversion by Device")
    plt.ylabel("Users")
    plt.savefig(f"{out_dir}/funnel.png")
    plt.close()

    # ------------------------------
    # Q2) Intent Distribution
    # ------------------------------
    messages["detected_intent"] = messages["detected_intent"].fillna("unknown")
    messages.loc[messages["detected_intent"].str.strip() == "", "detected_intent"] = "unknown"

    intent_counts = messages["detected_intent"].value_counts().reset_index()
    intent_counts.columns = ["intent", "count"]
    intent_counts["pct_of_total"] = round(intent_counts["count"] * 100 / intent_counts["count"].sum(), 2)

    intents = intent_counts.to_dict(orient="records")

    # Plot intents (top 10)
    intent_counts.head(10).plot(kind="bar", x="intent", y="count")
    plt.title("Top 10 Intents")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/intents.png")
    plt.close()

    # ------------------------------
    # Q3) Cancellation SLA
    # ------------------------------
    orders["created_at"] = pd.to_datetime(orders["created_at"])
    orders["canceled_at"] = pd.to_datetime(orders["canceled_at"], errors="coerce")

    total_orders = len(orders)
    canceled = orders["canceled_at"].notna().sum()

    violations = ((orders["canceled_at"] - orders["created_at"]).dt.total_seconds() / 60 > 60).sum()
    violation_rate = round(violations * 100 / total_orders, 2) if total_orders else 0

    cancellation_sla = {
        "total_orders": int(total_orders),
        "canceled": int(canceled),
        "violations": int(violations),
        "violation_rate_pct": violation_rate
    }

    # ------------------------------
    # Save JSON
    # ------------------------------
    output = {
        "funnel": funnel,
        "intents": intents,
        "cancellation_sla": cancellation_sla
    }

    with open(f"{out_dir}/report.json", "w") as f:
        json.dump(output, f, indent=2)

    print("✅ Report generated!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", required=True)
    parser.add_argument("--messages", required=True)
    parser.add_argument("--orders", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    main(args.events, args.messages, args.orders, args.out)
