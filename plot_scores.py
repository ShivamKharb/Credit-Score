import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the credit score CSV
df = pd.read_csv("wallet_scores.csv")

# Set style
sns.set(style="whitegrid")

# Plot histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['credit_score'], bins=20, kde=True, color='skyblue', edgecolor='black')

# Add titles and labels
plt.title("Aave Wallet Credit Score Distribution", fontsize=16)
plt.xlabel("Credit Score", fontsize=14)
plt.ylabel("Number of Wallets", fontsize=14)
plt.axvline(df['credit_score'].mean(), color='red', linestyle='dashed', linewidth=2, label=f'Mean Score: {df["credit_score"].mean():.1f}')
plt.legend()

# Show plot
plt.tight_layout()
plt.show()
plt.savefig("score_distribution.png")
