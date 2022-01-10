"""
ACCOUNT TYPE
"""
ACCOUNT_TESTING = "Testing"
ACCOUNT_STANDARD = "Standard"
ACCOUNT_PROFESSIONAL = "Professional"
ACCOUNT_BUSINESS = "Business"

"""
    PRICING
"""
# TESTING
ACCOUNT_TESTING_FORMS = 20
ACCOUNT_TESTING_WORKSPACES = 5
ACCOUNT_TESTING_SUBMISSIONS = 50
ACCOUNT_TESTING_STORAGE = 100  # MB
ACCOUNT_TESTING_CUSTOM_REDIRECT = False
ACCOUNT_TESTING_API = False
ACCOUNT_TESTING_CSV = False

# STANDARD
ACCOUNT_STANDARD_FORMS = 5
ACCOUNT_STANDARD_WORKSPACES = 3
ACCOUNT_STANDARD_SUBMISSIONS = 1000
ACCOUNT_STANDARD_STORAGE = 1000
ACCOUNT_STANDARD_CUSTOM_REDIRECT = True
ACCOUNT_STANDARD_API = True
ACCOUNT_STANDARD_CSV = True

# PROFESSIONAL
ACCOUNT_PROFESSIONAL_FORMS = 20
ACCOUNT_PROFESSIONAL_WORKSPACES = 10
ACCOUNT_PROFESSIONAL_SUBMISSIONS = 3000
ACCOUNT_PROFESSIONAL_STORAGE = 3000
ACCOUNT_PROFESSIONAL_CUSTOM_REDIRECT = True
ACCOUNT_PROFESSIONAL_API = True
ACCOUNT_PROFESSIONAL_CSV = True

# BUSINESS
ACCOUNT_BUSINESS_FORMS = float('inf')
ACCOUNT_BUSINESS_WORKSPACES = 100
ACCOUNT_BUSINESS_SUBMISSIONS = 100000
ACCOUNT_BUSINESS_STORAGE = 10000
ACCOUNT_BUSINESS_CUSTOM_REDIRECT = True
ACCOUNT_BUSINESS_API = True
ACCOUNT_BUSINESS_CSV = True


# LIMITATIONS
ACCOUNT_LIMITATIONS = {
    ACCOUNT_TESTING: {
        "total_forms": ACCOUNT_TESTING_FORMS,
        "total_workspaces": ACCOUNT_TESTING_WORKSPACES,
        "total_submissions": ACCOUNT_TESTING_SUBMISSIONS,
        "total_storage": ACCOUNT_TESTING_STORAGE,
        "api_access": ACCOUNT_TESTING_API,
        "custom_redirect": ACCOUNT_TESTING_CUSTOM_REDIRECT,
        "csv_export": ACCOUNT_TESTING_CSV,
    },
    ACCOUNT_STANDARD: {
        "total_forms": ACCOUNT_STANDARD_FORMS,
        "total_workspaces": ACCOUNT_STANDARD_WORKSPACES,
        "total_submissions": ACCOUNT_STANDARD_SUBMISSIONS,
        "total_storage": ACCOUNT_STANDARD_STORAGE,
        "api_access": ACCOUNT_STANDARD_API,
        "custom_redirect": ACCOUNT_STANDARD_CUSTOM_REDIRECT,
        "csv_export": ACCOUNT_STANDARD_CSV,
    },
    ACCOUNT_PROFESSIONAL: {
        "total_forms": ACCOUNT_PROFESSIONAL_FORMS,
        "total_workspaces": ACCOUNT_PROFESSIONAL_WORKSPACES,
        "total_submissions": ACCOUNT_PROFESSIONAL_SUBMISSIONS,
        "total_storage": ACCOUNT_PROFESSIONAL_STORAGE,
        "api_access": ACCOUNT_PROFESSIONAL_API,
        "custom_redirect": ACCOUNT_PROFESSIONAL_CUSTOM_REDIRECT,
        "csv_export": ACCOUNT_PROFESSIONAL_CSV,
    },
    ACCOUNT_BUSINESS: {
        "total_forms": ACCOUNT_BUSINESS_FORMS,
        "total_workspaces": ACCOUNT_BUSINESS_WORKSPACES,
        "total_submissions": ACCOUNT_BUSINESS_SUBMISSIONS,
        "total_storage": ACCOUNT_BUSINESS_STORAGE,
        "api_access": ACCOUNT_BUSINESS_API,
        "custom_redirect": ACCOUNT_BUSINESS_CUSTOM_REDIRECT,
        "csv_export": ACCOUNT_BUSINESS_CSV,
    },
}
