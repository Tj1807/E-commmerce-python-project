# E-commmerce-python-project

# Project Overview
## This project is an interactive E‑commerce Returns Analytics dashboard built with Streamlit and Plotly on top of a synthetic returns dataset.
## It enables exploratory analysis of order returns, customer behavior, and revenue patterns for different product categories and customer segments.

# Key capabilities include:

1. Overall and category‑level return rates
2. Return reasons distribution
3. Revenue insights by category and order value
4. Relationship between product price and days to return
5. Rich interactive filtering on customer and order attributes

# Repository Structure
.
├─ app.py                          # Streamlit application (main dashboard)
├─ ecommerce_returns_synthetic_data.csv   # Synthetic e‑commerce returns dataset
└─ Python_Project_ecommerce.ipynb  # Exploratory data analysis & prototyping notebook

# Dataset Description
## ecommerce_returns_synthetic_data.csv contains one row per order.

## Main columns:

1. OrderID: Unique identifier for each order
2. ProductID: Unique identifier for each product
3. UserID: Unique identifier for each user
4. OrderDate: Order placement date
5. ReturnDate: Date the order was returned (if returned)
6. ProductCategory: Product category (Books, Clothing, Electronics, Home, Toys)
7. ProductPrice: Unit price of the product
8. OrderQuantity: Quantity ordered
9. ReturnReason: Reason for return (Changed mind, Wrong item, Defective, Not as described, etc.)
10. ReturnStatus: Return outcome (Returned / Not Returned)
11. DaystoReturn: Number of days between order and return (can be negative in raw data and is cleaned in code)
12. UserAge: Age of the customer
13. UserGender: Gender of the customer
14. UserLocation: City‑level location label
15. PaymentMethod: Payment channel (Credit Card, Debit Card, PayPal, Gift Card, etc.)
16. ShippingMethod: Shipping type (Standard, Express, Next‑Day)
17. DiscountApplied: Discount applied on the order (monetary amount)

## Additional feature created in code:

-- Revenue: ProductPrice * OrderQuantity

## During preprocessing, OrderDate and ReturnDate are converted to datetime, DaystoReturn is coerced to numeric and transformed to its absolute value to handle negative anomalies, and Revenue is computed.

# Dashboard Features
1. Data Loading & Preprocessing
## The app uses a cached loader to read and preprocess the CSV file:

​1. Reads ecommerce_returns_synthetic_data.csv with pandas.
2. Converts OrderDate and ReturnDate to datetime.
3. Converts DaystoReturn to numeric and applies absolute value.
4. Creates a Revenue column as ProductPrice * OrderQuantity.

2. Dynamic Filters
## A Dynamic Filters section allows users to slice the dataset before computing KPIs and charts:
​
1. Product Category filter:
## st.selectbox with All + sorted unique ProductCategory.

2. User Gender filter:
## st.selectbox with All + sorted unique UserGender.

3. User Age range:
## st.slider for min and max age (18–70).

4. Revenue range:
## st.slider for minimum and maximum revenue (0–3000).

5. Days to Return range:
## st.select_slider on sorted unique non‑null DaystoReturn values.

6. Return Reason filter:
## st.multiselect on unique ReturnReason values.

## Filters are applied sequentially to a working copy of the dataframe, and the rest of the dashboard uses this filtered subset.
​

3. KPIs
## Once filters are applied, the app displays four key metrics:
​
### Total Orders: Count of filtered records.
### Returned Orders: Count where ReturnStatus == "Returned".
### Return Rate (%): Returned Orders / Total Orders * 100 (formatted to one decimal place).
### Avg Days to Return: Mean of DaystoReturn for filtered data (NA if not applicable).

4. Visualizations (Tabs)
## The main visual content is organized into three tabs: Overview, Returns Analysis, and Revenue Analysis.
​
## Overview Tab
### Overall Return Rate (bar chart):

### Uses plotreturnrate(df) to compute ReturnStatus distribution and display a bar chart of Returned vs Not Returned as percentages.

### Return by Product Category (bar chart):

### Uses plotcategoryreturnpercentage(df) to compute return percentage per ProductCategory and plot a bar chart of Returned percentages.

## Returns Analysis Tab
### Return Reasons Distribution (donut pie chart):

### plotreturnreasonpie(df) uses only Returned orders, calculates ReturnReason counts, and plots them as a pie chart with a hole (donut style).

### Price vs Days to Return (scatter):

### plotpricevsdaysscatter(df) filters to Returned orders with non‑null DaystoReturn and plots:

X: ProductPrice

Y: DaystoReturn

Color: ProductCategory

Size: OrderQuantity

Hover data: ReturnReason

## Revenue Analysis Tab
### Total Revenue by Product Category (pie chart):

### plotcategoryrevenuepie(df) groups by ProductCategory, sums Revenue, rounds to 0 decimals, and shows a pie chart of revenue share by category.

### Revenue Distribution (histogram):

### plotrevenuehistogram(df) builds a histogram of Revenue with 30 bins, small bar gap, and labels.

5. Data Preview & Filter Summary
## Data Preview: A st.expander labeled with the number of filtered rows shows a st.dataframe preview of the filtered dataset.
​

## Active Filters Summary: A st.info call prints a textual summary of the current filter selections (category, gender, age range, revenue range, days to return, and number of selected reasons).
​
# Setup & Installation
## Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

## Create and activate a virtual environment (optional but recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

## Install dependencies
### The core dependencies used in app.py and the notebook are:
### streamlit
### pandas
### numpy
### plotly
### seaborn and matplotlib (used in the notebook)

## Install with:
pip install streamlit pandas numpy plotly seaborn matplotlib

## You can also create a requirements.txt like:
### streamlit
### pandas
### numpy
### plotly
### seaborn
### matplotlib

## Running the Dashboard
### Ensure you are in the project directory and that ecommerce_returns_synthetic_data.csv is in the same folder as app.py.

streamlit run app.py
### Then open the local URL shown in the terminal (typically http://localhost:8501) in your browser.

## How the Code Works (High Level)
### Data Loading:
@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_returns_synthetic_data.csv")
    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
    df["ReturnDate"] = pd.to_datetime(df["ReturnDate"], errors="coerce")
    df["DaystoReturn"] = pd.to_numeric(df["DaystoReturn"], errors="coerce").abs()
    df["Revenue"] = df["ProductPrice"] * df["OrderQuantity"]
    return df
### This reflects the logic in loaddata from app.py (with formatting clarified).

## Filter Application
### The app builds filtered_df from the original dataframe using a series of conditional filters, for example:
​
1. Filter by category and gender when not "All".
2. Filter by age range and revenue range using numeric comparisons.
3. Filter by DaystoReturn range when available.
4. Filter by a set of ReturnReason values when selected.

## Plot Functions
### Each chart is encapsulated in a helper function to keep main() tidy:

1. plotreturnrate(df) – bar chart of return status percentages.
2. plotcategoryreturnpercentage(df) – bar chart of return percentage by product category.
3. plotreturnreasonpie(df) – donut pie chart of return reasons for returned orders.
4. plotrevenuehistogram(df) – histogram of order revenue.
5. plotpricevsdaysscatter(df) – scatter of ProductPrice vs DaystoReturn (returns only).
6. plotcategoryrevenuepie(df) – revenue share pie by product category.

## Notebook (Python_Project_ecommerce.ipynb)
### The notebook explores the same dataset with additional descriptive analysis and context:
​
1. Initial schema inspection, missing values check, and describe() statistics.
2. Conversion of date columns and creation of Revenue.
3. Calculation of overall and category‑level return rates (similar to logic reused in the app).
4. Commentary on patterns such as slightly higher return rates in some categories and typical ranges for DaystoReturn and UserAge.

### This notebook is useful for understanding the reasoning behind the dashboard design and validating that chart calculations match the exploratory analysis.

## License
### This project uses a fully synthetic dataset for demonstration and learning purposes.
### You can adapt the code and data structure for your own e‑commerce analytics or training projects; adjust the license section as needed for your GitHub repository.

