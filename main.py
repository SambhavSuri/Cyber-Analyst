import requests
import pandas as pd
from datetime import datetime, timedelta
from config import CLIENT_ID, CLIENT_SECRET, TENANT_ID, AUTHORITY, SCOPES

# ========== STEP 1: AUTHENTICATE ==========
def get_access_token():
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPES[0],
        'grant_type': 'client_credentials'
    }
    response = requests.post(f"{AUTHORITY}/oauth2/v2.0/token", data=data)
    
    if response.status_code != 200:
        print(f"❌ Authentication failed with status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None
        
    token_data = response.json()
    if 'access_token' not in token_data:
        print("❌ No access token received")
        print(f"Token response: {token_data}")
        return None
        
    print("✅ Authentication successful!")
    return token_data['access_token']

# ========== STEP 2: FETCH AUDIT LOGS ==========
def fetch_audit_logs(token, start_time, end_time):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/auditLogs/directoryAudits?$filter=activityDateTime ge {start_time} and activityDateTime le {end_time}"
    all_logs = []

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 403:
            print("❌ Permission denied (403 Forbidden)")
            print("You need to add the following permissions to your Azure AD app:")
            print("  - AuditLog.Read.All")
            print("\nTo fix this:")
            print("1. Go to Azure Portal → Azure Active Directory → App registrations")
            print("2. Select your app → API permissions")
            print("3. Add permission: Microsoft Graph → Application permissions → AuditLog.Read.All")
            print("4. Grant admin consent")
            return None
        elif response.status_code != 200:
            print(f"❌ Error fetching audit logs: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
        result = response.json()
        all_logs.extend(result.get("value", []))
        
        # Handle pagination
        while "@odata.nextLink" in result:
            response = requests.get(result["@odata.nextLink"], headers=headers)
            if response.status_code == 200:
                result = response.json()
                all_logs.extend(result.get("value", []))
            else:
                break

        print(f"✅ Successfully fetched {len(all_logs)} audit log entries")
        return all_logs
        
    except Exception as e:
        print(f"❌ Error during data fetch: {str(e)}")
        return None

# ========== STEP 3: SAVE TO EXCEL ==========
def save_to_excel(data, filename):
    if not data:
        print("❌ No data to save")
        return
        
    try:
        df = pd.json_normalize(data)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"✅ Saved {filename} with {len(df)} entries.")
    except Exception as e:
        print(f"❌ Error saving to Excel: {str(e)}")

# ========== MAIN ==========
def main():
    print("🚀 Microsoft 365 Audit Logs Fetcher")
    print("="*50)
    
    # Get access token
    token = get_access_token()
    if not token:
        print("❌ Failed to get access token. Exiting.")
        return
    
    # Set time range (last 30 days)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=30)
    start_str = start_time.isoformat() + 'Z'
    end_str = end_time.isoformat() + 'Z'
    
    print(f"📅 Fetching audit logs from {start_str} to {end_str}")

    # Fetch audit logs
    audit_logs = fetch_audit_logs(token, start_str, end_str)
    
    if audit_logs:
        save_to_excel(audit_logs, "AuditLogs_Last30Days.xlsx")
    else:
        print("❌ Failed to fetch audit logs")

if __name__ == "__main__":
    main()
