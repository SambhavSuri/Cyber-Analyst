import requests
from config import CLIENT_ID, CLIENT_SECRET, TENANT_ID, AUTHORITY, SCOPES

def get_access_token():
    """Get access token for Microsoft Graph API"""
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPES[0],
        'grant_type': 'client_credentials'
    }
    response = requests.post(f"{AUTHORITY}/oauth2/v2.0/token", data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"❌ Authentication failed: {response.status_code}")
        print(response.text)
        return None

def check_app_permissions():
    """Check what permissions are granted to the app"""
    token = get_access_token()
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get the service principal for our app
    url = f"https://graph.microsoft.com/v1.0/servicePrincipals"
    params = {
        "$filter": f"appId eq '{CLIENT_ID}'",
        "$select": "id,appId,appDisplayName,appRoles,oauth2PermissionScopes"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("value"):
                app = data["value"][0]
                print(f"📋 App: {app.get('appDisplayName', 'Unknown')}")
                print(f"🔑 App ID: {app.get('appId')}")
                print(f"🆔 Service Principal ID: {app.get('id')}")
                print("\n" + "="*60)
                
                # Check application permissions (app roles)
                print("🔐 APPLICATION PERMISSIONS (App Roles):")
                app_roles = app.get("appRoles", [])
                if app_roles:
                    for role in app_roles:
                        print(f"  ✅ {role.get('value')} - {role.get('displayName')}")
                else:
                    print("  ❌ No application permissions found")
                
                print("\n" + "="*60)
                
                # Check delegated permissions (OAuth scopes)
                print("🔐 DELEGATED PERMISSIONS (OAuth Scopes):")
                oauth_scopes = app.get("oauth2PermissionScopes", [])
                if oauth_scopes:
                    for scope in oauth_scopes:
                        print(f"  ✅ {scope.get('value')} - {scope.get('adminConsentDisplayName')}")
                else:
                    print("  ❌ No delegated permissions found")
                
                print("\n" + "="*60)
                
                # Check what permissions are actually granted
                print("🔍 CHECKING GRANTED PERMISSIONS:")
                check_granted_permissions(token, app.get('id'))
                
            else:
                print("❌ App not found in the tenant")
        else:
            print(f"❌ Failed to get app details: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error checking permissions: {str(e)}")

def check_granted_permissions(token, service_principal_id):
    """Check what permissions are actually granted to the app"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get app role assignments
    url = f"https://graph.microsoft.com/v1.0/servicePrincipals/{service_principal_id}/appRoleAssignments"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            assignments = data.get("value", [])
            
            if assignments:
                print("✅ GRANTED PERMISSIONS:")
                for assignment in assignments:
                    print(f"  - {assignment.get('appRole', {}).get('value')}")
            else:
                print("❌ NO PERMISSIONS GRANTED")
                print("   You need to grant admin consent for the permissions!")
                
        elif response.status_code == 403:
            print("❌ Cannot check granted permissions - insufficient privileges")
            print("   This is normal if you don't have admin rights")
        else:
            print(f"❌ Error checking granted permissions: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_audit_logs_access():
    """Test if we can access audit logs"""
    token = get_access_token()
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/auditLogs/directoryAudits?$top=1"
    
    try:
        response = requests.get(url, headers=headers)
        
        print("\n" + "="*60)
        print("🧪 TESTING AUDIT LOGS ACCESS:")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Can access audit logs")
            data = response.json()
            print(f"   Found {len(data.get('value', []))} records")
        elif response.status_code == 403:
            print("❌ FAILED: Cannot access audit logs (403 Forbidden)")
            print("   Error details:")
            error_data = response.json()
            print(f"   Code: {error_data.get('error', {}).get('code')}")
            print(f"   Message: {error_data.get('error', {}).get('message')}")
        else:
            print(f"❌ UNEXPECTED ERROR: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing access: {str(e)}")

if __name__ == "__main__":
    print("🔍 Microsoft Graph API Permission Checker")
    print("="*60)
    
    check_app_permissions()
    test_audit_logs_access()
    
    print("\n" + "="*60)
    print("📋 NEXT STEPS:")
    print("1. If permissions are not granted, grant admin consent")
    print("2. Wait 5-10 minutes for permissions to propagate")
    print("3. Run this script again to verify")
    print("4. If still failing, check if you have admin rights") 