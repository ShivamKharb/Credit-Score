import json
import pandas as pd
import os

#  Auto-detect wallet column 
def detect_wallet_column(columns):
    wallet_keys = ['wallet_id', 'wallet_address', 'user', 'account', 'address', 'userWallet']
    for key in wallet_keys:
        if key in columns:
            return key
    raise KeyError(f"[ERROR] None of the expected wallet ID fields found in: {columns}")

#  Load data from JSON or CSV 
def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[ERROR] File not found: {file_path}")
    
    print(f"[INFO] Loading file: {file_path}")
    
    if file_path.endswith('.json'):
        with open(file_path, "r") as f:
            data = json.load(f)
        
        # Handle case where data is a dict with a key containing the records
        if isinstance(data, dict):
            # Try guessing the key
            for key in ['data', 'result', 'transactions', 'records']:
                if key in data and isinstance(data[key], list):
                    print(f"[INFO] Found transaction list under key: '{key}'")
                    data = data[key]
                    break
            else:
                raise ValueError("[ERROR] Could not locate transaction list in JSON file.")

        if not isinstance(data, list):
            raise ValueError("[ERROR] JSON root is not a list of records.")

        df = pd.json_normalize(data)
    
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("[ERROR] Unsupported file format. Only .json and .csv are supported.")
    
    print("[INFO] Loaded columns:", df.columns.tolist())
    return df

#  Feature engineering for credit behavior 
def generate_features(df, wallet_col):
    if 'timestamp' not in df.columns:
        raise ValueError("[ERROR] 'timestamp' column is missing in data.")

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')

    if 'actionData.amount' not in df.columns:
        if 'amount' in df.columns:
            df['actionData.amount'] = df['amount']
        else:
            df['actionData.amount'] = 0  # fallback if no amount found
    
    df['actionData.amount'] = pd.to_numeric(df['actionData.amount'], errors='coerce').fillna(0)

    if 'action' not in df.columns:
        raise ValueError("[ERROR] 'action' column not found in data.")

    grouped = df.groupby(wallet_col)

    features = grouped.agg(
        total_actions=('action', 'count'),
        num_deposits=('action', lambda x: (x == 'deposit').sum()),
        num_borrows=('action', lambda x: (x == 'borrow').sum()),
        num_repays=('action', lambda x: (x == 'repay').sum()),
        num_liquidations=('action', lambda x: (x == 'liquidationcall').sum()),
        total_volume=('actionData.amount', 'sum'),
        avg_txn_amount=('actionData.amount', 'mean'),
        active_days=('timestamp', lambda x: x.dt.date.nunique())
    ).reset_index()

    features['deposit_borrow_ratio'] = features['num_deposits'] / (features['num_borrows'] + 1)
    features['repay_borrow_ratio'] = features['num_repays'] / (features['num_borrows'] + 1)
    features['liquidation_rate'] = features['num_liquidations'] / (features['total_actions'] + 1)

    return features

#  Credit scoring logic based on behavior 
def calculate_credit_score(row):
    score = 300
    score += min(150, row['num_deposits'] * 8)
    score += min(250, row['repay_borrow_ratio'] * 120)
    score += min(100, row['active_days'] * 2)
    score += min(100, row['total_volume'] / 1000)

    score -= min(200, row['liquidation_rate'] * 400)
    if row['num_borrows'] > 0 and row['num_repays'] == 0:
        score -= 100
    if row['total_volume'] < 10:
        score -= 50
    if row['total_actions'] > 1000:
        score -= 100

    return max(0, min(1000, int(score)))

#  Risk label logic 
def label_risk(score):
    if score >= 750:
        return "Excellent"
    elif score >= 600:
        return "Good"
    elif score >= 500:
        return "Fair"
    elif score >= 350:
        return "Poor"
    else:
        return "Very Risky"

#  Full pipeline 
def generate_credit_scores(file_path, output_csv="wallet_scores.csv"):
    print(">> Running credit scoring script...")
    df = load_data(file_path)
    wallet_col = detect_wallet_column(df.columns)
    print(f"[INFO] Using '{wallet_col}' as wallet identifier")

    features = generate_features(df, wallet_col)
    print("[INFO] Features generated successfully")

    features['credit_score'] = features.apply(calculate_credit_score, axis=1)
    features['risk_label'] = features['credit_score'].apply(label_risk)

    features[[wallet_col, 'credit_score', 'risk_label']].to_csv(output_csv, index=False)
    print(f"[SUCCESS] Wallet credit scores saved to: {output_csv}")

#  Run the script 
if __name__ == "__main__":
    generate_credit_scores("Your File Path here")

   
    

   
