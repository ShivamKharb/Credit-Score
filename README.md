# Wallet Credit Scoring Model

##  Objective

To assign a **credit score between 0 and 1000** to wallets interacting with the Aave V2 DeFi protocol, based **solely on their historical transaction behavior**. The goal is to distinguish responsible, long-term DeFi participants from risky, bot-like, or exploitative wallets.



## Scoring Methodology

Each wallet’s score is computed based on:

| Feature                        | Behavior Impact       | Score Effect             |
|-------------------------------|------------------------|--------------------------|
| `num_deposits`                | Responsible usage      |  Adds to score         |
| `repay_borrow_ratio`          | Risk mitigation        |  Strongly boosts score |
| `active_days`                 | Long-term participation|  Boosts score          |
| `total_volume`                | Capital involved       |  Moderate boost        |
| `liquidation_rate`            | Exploit / misuse       |  Reduces score         |
| `borrow without repay`        | High risk              |  Heavily penalized     |
| `suspicious volume / bot-like`| Likely bots            |  Penalized             |

Scoring range: `0` (worst) to `1000` (best)

Each score is then labeled into **risk bands**:

 Score Range  Risk Label        
-------------------------------
 750–1000     Excellent      
 600–749      Good           
 500–599      Fair           
 350–499      Poor       
 0–349        Very Risky     

---

## Architecture

##  Dependencies

Install all project dependencies with:

```bash
pip install -r requirements.txt



---

## Processing Flow

1. **Load JSON file**: Flatten nested fields like `actionData.amount`
2. **Aggregate by wallet**: Group by `userWallet`, calculate key metrics
3. **Score assignment**: Apply scoring logic to generate scores (0–1000)
4. **Risk label**: Categorize into qualitative bands
5. **Save results**: Output saved to `wallet_scores.csv`

---

##  Output File

 userWallet                                credit_score  risk_label     
------------------------------------------------------------------------
 0x000...4b6                                312           Very Risky   
 0x000...1ee                                625           Good        
 ...                                        ...           ...            

---

##  How to Run


# Generate scores
python credit_score.py

# Optional: Plot distribution
python plot_scores.py
