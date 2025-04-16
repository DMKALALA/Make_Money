
# 📊 YNAB Mobile Dashboard

A mobile-optimized interactive budget dashboard powered by the YNAB (You Need A Budget) API, built using Python, Streamlit, and Plotly. This dashboard helps visualize your financial health through real-time budget insights, category breakdowns, and savings vs spending trends.

---

## 🚀 Features

* 📆  **Month Selector** : Choose from available budget months
* 💰  **Summary Metrics** :
  * To Be Budgeted
  * Inflow & Outflow
* 📊  **Visualizations** :
  * Cash Flow Bar Chart
  * Top Spending Categories Pie Chart
  * Savings vs Spending Line Chart
  * Net Savings Over Time
  * Category Breakdown Over Time
  * Interactive Granularity View (Daily, Weekly, Monthly)
* 🔍 **Category Filters** for detailed analysis
* 📤 **Export to CSV** functionality for offline reporting

---

## 🧰 Tech Stack

* [Streamlit](https://streamlit.io/)
* [Plotly Express](https://plotly.com/python/plotly-express/)
* [YNAB API](https://api.youneedabudget.com/)
* [Python 3.12+](https://www.python.org/)

---

## 🔒 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/ynab-dashboard.git
cd ynab-dashboard
```

### 2. Create Virtual Environment

```bash
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file with:

```
YNAB_TOKEN=your_ynab_personal_access_token_here
```

> 🔐 If deploying to Streamlit Cloud, use the "Secrets" tab instead.

### 5. Run Locally

```bash
streamlit run dashboard.py
```

---

## 📸 Screenshots & Visuals

### 📋 Dashboard Overview

![Dashboard](https://chatgpt.com/c/images/dashboard_overview.png)

### 🏷️ Category Pie Chart

![Categories](https://chatgpt.com/c/images/top_categories.png)

### 💸 Savings vs Spending Trend

![SavingsVsSpending](https://chatgpt.com/c/images/savings_vs_spending.png)

---

## 🌐 Deployment

Deployed on [Streamlit Cloud](https://denismoneyapp.streamlit.app/). Set the main file to `dashboard.py` and configure `YNAB_TOKEN` in Secrets.

---

## 📬 Feedback & Contributions

Pull requests, suggestions, and feedback are welcome! Let's build smarter financial tools together.

---

## 🧠 Credits

Created with ❤️ by Denis Kalala, powered by real-time insights from YNAB.

---

## 📄 License

[MIT](https://chatgpt.com/c/LICENSE)
