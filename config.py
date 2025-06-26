# Microsoft Graph API Configuration
TENANT_ID = ""
CLIENT_ID = ""
CLIENT_SECRET = ""

# Authentication
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# Microsoft Graph API Endpoints for different services
ENDPOINTS = {
    # Entra ID (Azure AD) Logs
    "entra_signins": "https://graph.microsoft.com/v1.0/auditLogs/signIns",
    "entra_audit": "https://graph.microsoft.com/v1.0/auditLogs/directoryAudits",
    "entra_users": "https://graph.microsoft.com/v1.0/users",
    
    # Microsoft Defender for Endpoint
    "defender_alerts": "https://graph.microsoft.com/v1.0/security/alerts",
    "defender_incidents": "https://graph.microsoft.com/v1.0/security/incidents",
    "defender_secureScores": "https://graph.microsoft.com/v1.0/security/secureScores",
    
    # Microsoft Intune
    "intune_devices": "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices",
    "intune_apps": "https://graph.microsoft.com/v1.0/deviceManagement/mobileApps",
    "intune_policies": "https://graph.microsoft.com/v1.0/deviceManagement/deviceCompliancePolicies",
    
    # Microsoft Purview
    "purview_retention": "https://graph.microsoft.com/v1.0/security/retentionEvents",
    "purview_labels": "https://graph.microsoft.com/v1.0/informationProtection/threatAssessmentRequests",
    
    # Microsoft 365 Compliance
    "compliance_audit": "https://graph.microsoft.com/v1.0/auditLogs/directoryAudits",
    "compliance_reports": "https://graph.microsoft.com/v1.0/reports",
    
    # Exchange Online
    "exchange_messages": "https://graph.microsoft.com/v1.0/me/messages",
    "exchange_mailbox": "https://graph.microsoft.com/v1.0/me/mailboxSettings",
    
    # SharePoint Online
    "sharepoint_sites": "https://graph.microsoft.com/v1.0/sites",
    "sharepoint_drives": "https://graph.microsoft.com/v1.0/me/drives",
    
    # Teams
    "teams_chats": "https://graph.microsoft.com/v1.0/me/chats",
    "teams_meetings": "https://graph.microsoft.com/v1.0/me/onlineMeetings"
}

# Required API Permissions for each service
REQUIRED_PERMISSIONS = {
    "entra_id": [
        "AuditLog.Read.All",
        "User.Read.All",
        "Directory.Read.All"
    ],
    "defender": [
        "SecurityEvents.Read.All",
        "SecurityIncident.Read.All"
    ],
    "intune": [
        "DeviceManagementServiceConfig.Read.All",
        "DeviceManagementManagedDevices.Read.All"
    ],
    "purview": [
        "InformationProtectionPolicy.Read.All",
        "ThreatAssessment.Read.All"
    ],
    "compliance": [
        "AuditLog.Read.All",
        "Reports.Read.All"
    ],
    "exchange": [
        "Mail.Read",
        "MailboxSettings.Read"
    ],
    "sharepoint": [
        "Sites.Read.All",
        "Files.Read.All"
    ],
    "teams": [
        "Chat.Read",
        "OnlineMeetings.Read"
    ]
} 