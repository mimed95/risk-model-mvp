import requests
from fredapi import Fred  # Use 'fredapi' instead of 'fred' for the official package
from bls import BLS

# Replace these with your actual API keys
FRED_API_KEY = 'your_fred_api_key'
BLS_API_KEY = 'your_bls_api_key'

# Initialize API clients
fred = Fred(api_key=FRED_API_KEY)
bls = BLS(api_key=BLS_API_KEY)

# Fetch latest Federal Funds Rate from FRED
def get_latest_interest_rate():
    series_id = 'FEDFUNDS'  # Federal Funds Rate series
    data = fred.get_series_latest_release(series_id)
    return float(data[-1])  # Return the most recent value

# Fetch latest CPI from BLS
def get_latest_cpi():
    series_id = 'CUUR0000SA0'  # CPI for All Urban Consumers (CPI-U), not seasonally adjusted
    data = bls.series(series_id, start_year=2023, end_year=2024)
    return float(data[-1]['value'])  # Return the most recent value

# Fetch latest unemployment rate from BLS
def get_latest_unemployment_rate():
    series_id = 'LNS14000000'  # Unemployment Rate, seasonally adjusted
    data = bls.series(series_id, start_year=2023, end_year=2024)
    return float(data[-1]['value'])  # Return the most recent value

# Calculate risk score using a weighted formula
def calculate_risk_score(interest_rate, cpi, unemployment_rate):
    # Example weights: 50% interest rate, 30% CPI, 20% unemployment rate
    score = (0.5 * interest_rate) + (0.3 * cpi) + (0.2 * unemployment_rate)
    return score

# Classify risk based on score
def classify_risk(score):
    if score < 5:
        return "Low Risk"
    elif score < 10:
        return "Medium Risk"
    else:
        return "High Risk"

# Main application logic
def main():
    print("Fetching latest data...")
    try:
        base_interest_rate = get_latest_interest_rate()
        base_cpi = get_latest_cpi()
        base_unemployment_rate = get_latest_unemployment_rate()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return
    
    # Display base values
    print(f"Base Interest Rate: {base_interest_rate}%")
    print(f"Base CPI: {base_cpi}")
    print(f"Base Unemployment Rate: {base_unemployment_rate}%")
    
    # Get user input for scenario changes
    print("\nEnter scenario changes:")
    try:
        interest_rate_change = float(input("Change in interest rate (in percentage points): "))
        cpi_change = float(input("Change in CPI (in percentage points): "))
        unemployment_rate_change = float(input("Change in unemployment rate (in percentage points): "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return
    
    # Calculate modified values
    modified_interest_rate = base_interest_rate + interest_rate_change
    modified_cpi = base_cpi + cpi_change
    modified_unemployment_rate = base_unemployment_rate + unemployment_rate_change
    
    # Compute risk score and classify
    risk_score = calculate_risk_score(modified_interest_rate, modified_cpi, modified_unemployment_rate)
    risk_category = classify_risk(risk_score)
    
    # Display results
    print("\nScenario Results:")
    print(f"Modified Interest Rate: {modified_interest_rate}%")
    print(f"Modified CPI: {modified_cpi}")
    print(f"Modified Unemployment Rate: {modified_unemployment_rate}%")
    print(f"Risk Score: {risk_score:.2f}")
    print(f"Risk Category: {risk_category}")

if __name__ == "__main__":
    main()