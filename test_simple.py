import requests
from config import CLIENT_ID, CLIENT_SECRET, TENANT_ID, AUTHORITY, SCOPES

def test_basic_access():
    """Test basic Microsoft Graph API access"""
    print("🧪 Testing Basic Microsoft Graph API Access")
    print("="*50)
    
    # Get access token
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPES[0],
        'grant_type': 'client_credentials'
    }
    response = requests.post(f"{AUTHORITY}/oauth2/v2.0/token", data=data)
    
    if response.status_code != 200:
        print(f"❌ Authentication failed: {response.status_code}")
        print(response.text)
        return
    
    token = response.json()['access_token']
    print("✅ Authentication successful!")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Get organization info (basic access)
    print("\n📋 Test 1: Organization Info")
    try:
        response = requests.get("https://graph.microsoft.com/v1.0/organization", headers=headers)
        if response.status_code == 200:
            org_data = response.json()
            print(f"✅ Success: {org_data.get('value', [{}])[0].get('displayName', 'Unknown')}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Get users (requires User.Read.All)
    print("\n👥 Test 2: Users Access")
    try:
        response = requests.get("https://graph.microsoft.com/v1.0/users?$top=1", headers=headers)
        if response.status_code == 200:
            users_data = response.json()
            print(f"✅ Success: Found {len(users_data.get('value', []))} users")
        elif response.status_code == 403:
            print("❌ Failed: Need User.Read.All permission")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Audit logs (requires AuditLog.Read.All)
    print("\n📊 Test 3: Audit Logs Access")
    try:
        response = requests.get("https://graph.microsoft.com/v1.0/auditLogs/directoryAudits?$top=1", headers=headers)
        if response.status_code == 200:
            audit_data = response.json()
            print(f"✅ Success: Found {len(audit_data.get('value', []))} audit records")
        elif response.status_code == 403:
            print("❌ Failed: Need AuditLog.Read.All permission")
            print("   Please grant admin consent for this permission")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_basic_access() 