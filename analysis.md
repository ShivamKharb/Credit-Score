# Wallet Credit Score Analysis – Aave V2 Protocol

## Executive Summary

This report presents an analytical overview of wallet behavior on the Aave V2 protocol using a custom credit scoring model. The model assigns scores between **0 and 1000** to wallets based solely on historical DeFi transaction behavior, rewarding responsible and sustained usage while penalizing exploitative, high-risk, or bot-like patterns.

The dataset consists of over 100,000 transaction-level records from the Aave V2 protocol, representing various actions including `deposit`, `borrow`, `repay`, `redeemunderlying`, and `liquidationcall`.



## Score Distribution

Wallet credit scores are binned into 100-point intervals ranging from 0 to 1000. The distribution helps identify risk segments and behavioral patterns.

![score_distribution](score_distribution.png)

### Score Ranges

| Score Range | Risk Label       
|-------------|---------------
| 0–99        | Very Risky     
| 100–199     | Very Risky     
| 200–299     | Very Risky    
| 300–399     | Poor       
| 400–499     | Poor           
| 500–599     | Fair           
| 600–699     | Good           
| 700–799     | Excellent      
| 800–1000    | Excellent     





##  Behavioral Patterns by Score Range

###  **Very Risky Wallets (0–299)**
- Often exhibit only 1–2 transactions
- Tend to borrow without repaying
- Have very low total transaction volume (possibly bots or inactive)
- Frequently liquidated due to poor collateral management
- Short active periods or single-day behavior
- Many may be **programmatic exploit attempts or dust wallets**

###  **Poor Wallets (300–499)**
- Have minimal activity beyond initial interaction
- Low repay-to-borrow ratios
- Low transaction diversity (one-time borrowers or depositors)
- May signal short-term farming or abandoned wallets

###  **Fair Wallets (500–599)**
- Have balanced deposits and some repayments
- Moderate transaction volume
- Limited liquidations but low consistency in behavior
- Possibly occasional DeFi users

###  **Good Wallets (600–699)**
- Responsible usage patterns
- Multiple deposits and repays
- Rarely liquidated
- Actively participate over longer periods

###  **Excellent Wallets (700–1000)**
- Highly engaged wallets with strong on-chain credit behavior
- High repay-to-borrow ratios
- Frequent deposits
- No liquidations or defaults
- Consistently active across many days/months
- Likely long-term lenders or whales using Aave as a credit facility


##  Insights & Recommendations

- Over **60% of wallets** fall below a score of 500 — a potential indicator of spam, bots, or unsafe lending behavior.
- Only **~10% of wallets** are truly high-quality credit participants — candidates for premium DeFi services or whitelisted borrowing tiers.
- This model could help:
  - **Build on-chain credit reputation**
  - **Adjust borrowing limits or collateral ratios**
  - **Detect exploit attempts early**


## Scoring Model Highlights

- Based solely on on-chain actions — no off-chain identity, no credit bureaus.
- Deterministic, interpretable, and transparent.
- Can be extended with:
  - Time-weighted activity
  - Social staking behavior
  - Multi-protocol reputation

---

## Files Used

| File                        | Description                              |
|-----------------------------|------------------------------------------|
| `user-wallet-transactions.json` | Raw Aave V2 transaction data             |
| `credit_score.py`          | Scoring logic & feature engineering      |
| `wallet_scores.csv`        | Final wallet score + risk label output   |
| `score_distribution.png`   | Histogram of score distribution          |
| `analysis.md`              | This report                              |
| `wallet_analysis_report.pdf` | Exported professional PDF version        |

---

**Generated with by the Wallet Credit Score system.**
