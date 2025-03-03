import pandas as pd
from fredapi import Fred
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# Initialize FRED API (replace with your actual API key)
fred = Fred(api_key='e6ff54b98580bf99e260753f23f56682')

def fetch_and_prepare_data():
    try:
        # Fetch time series from FRED
        unemployment_rate = fred.get_series('UNRATE')
        gdp = fred.get_series('GDPC1')
        treasury_yield = fred.get_series('DGS10')
        sp500_index = fred.get_series('SP500')
        housing_price_index = fred.get_series('CSUSHPISA')
        inflation_rate = fred.get_series('CPIAUCSL')
        financial_stress_index = fred.get_series('STLFSI3')

        # Reindex quarterly GDP to monthly and interpolate
        monthly_index = pd.date_range(start=gdp.index.min(), end=gdp.index.max(), freq='MS')
        gdp = gdp.reindex(monthly_index).interpolate(method='linear')
        gdp_growth = gdp.pct_change().fillna(0)

        # Resample daily and weekly series to month-start (MS)
        treasury_yield = treasury_yield.resample('MS').mean()
        sp500_index = sp500_index.resample('MS').mean()
        financial_stress_index = financial_stress_index.resample('MS').mean()

        # Calculate inflation rate percentage change
        inflation_rate = inflation_rate.pct_change().fillna(0)

        # Combine into DataFrame and remove rows with NaN values
        df = pd.DataFrame({
            'unemployment_rate': unemployment_rate,
            'gdp_growth': gdp_growth,
            'treasury_yield': treasury_yield,
            'sp500_index': sp500_index,
            'housing_price_index': housing_price_index,
            'inflation_rate': inflation_rate,
            'financial_stress_index': financial_stress_index
        }).dropna()

        # Check if DataFrame is empty
        if df.empty:
            print("Error: DataFrame is empty after dropping NaNs. Check series date ranges or alignment.")
            return None

        # Define risk categories based on financial stress index quantiles
        q1 = df['financial_stress_index'].quantile(0.25)
        q3 = df['financial_stress_index'].quantile(0.75)

        def define_risk_category(fsi):
            if fsi < q1:
                return 0  # Low Risk
            elif fsi <= q3:
                return 1  # Medium Risk
            else:
                return 2  # High Risk

        df['risk_category'] = df['financial_stress_index'].apply(define_risk_category)
        return df

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def train_and_evaluate_model(data):
    # Extract features and target
    X = data[['unemployment_rate', 'gdp_growth', 'treasury_yield', 'sp500_index', 'housing_price_index', 'inflation_rate']]
    y = data['risk_category']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = GradientBoostingClassifier(n_estimators=1000, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, predictions))
    print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))

    return model

def classify_scenario(model, scenario):
    # Convert scenario to DataFrame with matching columns
    scenario_df = pd.DataFrame([scenario], columns=['unemployment_rate', 'gdp_growth', 'treasury_yield', 'sp500_index', 'housing_price_index', 'inflation_rate'])
    prediction = model.predict(scenario_df)
    risk_label = {0: "Low", 1: "Medium", 2: "High"}[prediction[0]]
    return risk_label

# Execute the workflow
data = fetch_and_prepare_data()
if data is not None:
    trained_model = train_and_evaluate_model(data)

    # Example scenario
    example_scenario = {
        'unemployment_rate': 4.5,
        'gdp_growth': 0.02,
        'treasury_yield': 2.5,
        'sp500_index': 3600,
        'housing_price_index': 220,
        'inflation_rate': 0.03
    }

    # Classify the scenario
    risk = classify_scenario(trained_model, example_scenario)
    print("Risk Category for the example scenario:", risk)
else:
    print("Failed to prepare data. Cannot proceed with model training.")
