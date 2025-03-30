from django.utils import timezone  # Correct import for Django's timezone
from .models import TickerData
import os
import pandas as pd
import requests
from sklearn.preprocessing import MinMaxScaler

# Input: Dictionary with primary keys for earnigns, cash flow, income statement, and balance sheet data
# Output: Pandas DataFrame with 1D feature vector ready for prediction
def json_to_dataframe(combined_data):
    earnings_data = pd.DataFrame(combined_data['earnings_data']['quarterlyEarnings'])
    cash_flow_data = pd.DataFrame(combined_data['cash_flow_data']['quarterlyReports'])
    balance_sheet_data = pd.DataFrame(combined_data['balance_sheet_data']['quarterlyReports'])
    income_stmt_data = pd.DataFrame(combined_data['income_stmt_data']['quarterlyReports'])

    total_report = earnings_data.merge(cash_flow_data, on='fiscalDateEnding') \
                        .merge(income_stmt_data, on='fiscalDateEnding') \
                        .merge(balance_sheet_data, on='fiscalDateEnding')

    # Columns to drop (organized by category for better maintainability)
    columns_to_drop = [
        # Earnings columns
        'surprise', 'surprisePercentage', 'reportTime', 'reportedCurrency_x',
        # Cash flow columns
        'paymentsForOperatingActivities', 'proceedsFromOperatingActivities',
        'changeInOperatingLiabilities', 'changeInOperatingAssets',
        'changeInReceivables', 'changeInInventory',
        'paymentsForRepurchaseOfPreferredStock', 'dividendPayoutPreferredStock',
        'proceedsFromIssuanceOfCommonStock', 'proceedsFromIssuanceOfPreferredStock',
        'proceedsFromSaleOfTreasuryStock', 'changeInExchangeRate', 'reportedCurrency_y',
        # Income statement columns
        'investmentIncomeNet', 'reportedCurrency',
        # Balance sheet columns
        'otherNonCurrentAssets', 'commonStock',
        # Date columns
        'fiscalDateEnding', 'reportedDate'
    ]


    # Data cleaning pipeline
    total_report = (total_report
                .drop(columns=columns_to_drop)
                .replace(['None', 'NaN'], 0)
                .astype(float))  # Explicit conversion to float


    # Initialize the scaler
    scaler = MinMaxScaler()
    # Normalize each column independently
    scaled_total_report= pd.DataFrame(
                            scaler.fit_transform(total_report),
                            columns=total_report.columns,
                        ).iloc[1:].reset_index(drop=True)
  

    # No need to compute target var yet
    # compute_target = pd.DataFrame()
    # compute_target = scaled_total_report.diff()
    # compute_target = compute_target.iloc[1:].reset_index(drop=True)
    # compute_target['SumOfNorm'] = compute_target.sum(axis=1)
    # compute_target['FinRepScore'] = compute_target['SumOfNorm'] 

    # first and most recent row
    return scaled_total_report.iloc[[0]].values
    
def fetch_from_alpha(ticker, alpha_key, title):
    # Call API for earnings report data
    url = f'https://www.alphavantage.co/query?function={title}&symbol={ticker}&apikey={alpha_key}'
    r = requests.get(url)
    data = r.json()
    return data


def fetch_and_cache_ticker_data(ticker):
    try:
        ticker_data = TickerData.objects.get(ticker=ticker)
        if not ticker_data.is_stale():
            combined_data=ticker_data.dataset
            return json_to_dataframe(combined_data)
    except TickerData.DoesNotExist:
        pass

    # API KEY
    alpha_key = os.environ.get('ALPHA_KEY')
    earnings_data = fetch_from_alpha(ticker, alpha_key, 'EARNINGS')
    cash_flow_data = fetch_from_alpha(ticker, alpha_key, 'CASH_FLOW')
    balance_sheet_data = fetch_from_alpha(ticker, alpha_key, 'BALANCE_SHEET')
    income_stmt_data = fetch_from_alpha(ticker, alpha_key, 'INCOME_STATEMENT')

    # Combine data from all APIs into a single dictionary
    combined_data = {
        'ticker': ticker,
        'earnings_data': earnings_data,
        'cash_flow_data': cash_flow_data,
        'balance_sheet_data': balance_sheet_data,
        'income_stmt_data': income_stmt_data,
    }

    # Saves Dirty data on database 
    # TODO: Clean Data before saving
    TickerData.objects.update_or_create(
        ticker=ticker,
        defaults={
            'dataset': combined_data,
            'last_updated': timezone.now(),  # Use Django's timezone.now()
        }
    )


    return json_to_dataframe(combined_data)


   
