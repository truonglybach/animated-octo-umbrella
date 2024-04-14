# this will utilize the SEC API to grab financial statements
import os

# *** should set the range to be between the last five years as the default
# TICKER and FORMAT OF DATES should be explicit in the HTML

def grabFinStmts(ticker, beg_date="2019-01-01", end_date="2024-04-13"):
    from sec_api import QueryApi, XbrlApi
    import json

    SEC_API_KEY=os.environ.get("SEC_API_KEY")

    query_stmt =  f"ticker:{ticker} AND filedAt:[{beg_date} TO {end_date}] AND formType:\"10-Q\""
    # Query
    queryApi = QueryApi(api_key=SEC_API_KEY)

    query = {
    "query": { "query_string": { 
        "query": query_stmt,
        "time_zone": "America/New_York"
    } },
    "from": "0",
    "size": "10",
    "sort": [{ "filedAt": { "order": "desc" } }]
    }

    response = queryApi.get_filings(query)

    url = json.dumps(response["filings"][0].get("documentFormatFiles")[0]["documentUrl"], indent=2)

    # Extract Data
    xbrlApi = XbrlApi(SEC_API_KEY)
    xbrl_json = xbrlApi.xbrl_to_json(htm_url=url)

    bal_sheet = xbrl_json.get("BalanceSheets")
    income_stmt = xbrl_json.get("StatementsOfIncome")
    cf_stmt = xbrl_json.get("StatementsOfCashFlows")
    stmt_sh_eqy = xbrl_json.get("StatementsOfShareholdersEquity")

    return [income_stmt, bal_sheet, cf_stmt, stmt_sh_eqy]
