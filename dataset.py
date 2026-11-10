import pandas as pd
import numpy as np

A=pd.read_csv('Jan2017Trans.csv')
print(A['amount'].sum())

TOP5=A.groupby('customer_id')['amount'].sum().sort_values(ascending=False).head(5)

cols = ['amount', 'per_capita_income', 'yearly_income', 'credit_limit','total_debt']

for col in cols:
    A[col] = pd.to_numeric(
        A[col].astype(str).str.replace('$', '', regex=False).str.replace('-', '', regex=False),
        errors='coerce'
    )

A['agegroups'] = pd.cut(
    A['current_age'],
    bins=[0, 25, 40, 55, 75, 100],
    labels=["18-25", "26-40", "40-55", "55-75", "75-100"]
)


sample=A.groupby('agegroups',observed=True).agg(
        total_spending=("amount", "sum"),
        avg_spending=("amount", "mean"),
        median_spending=("amount", "median"),
        customers=("amount", "count"),
        Yearly_income=("yearly_income", "sum"),
        Yearly_avg_income=("yearly_income", "mean"),
        Avg_no_cards=("num_credit_cards", "mean"),
        total_credit_limt=('credit_limit','sum'),
        Avg_credit_limt=('credit_limit','mean'),
        median_credit_score=("credit_score", "mean")
).reset_index()