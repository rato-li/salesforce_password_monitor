def check_password_policy_via_metadata():
    """Query Salesforce password policies via Metadata API"""
    from simple_salesforce import Salesforce
    try:
        sf = Salesforce(
            username=config['username'],
            password=config['password'] + config['security_token'],
            security_token=config['security_token'],
            domain=config['domain']
        )
        result = sf.mdapi.executeAnonymous(
            "PasswordPolicy pp = [SELECT MaxAge FROM PasswordPolicy WHERE Type = 'User' LIMIT 1];\n"
            "System.debug('MaxAge: ' + pp.MaxAge);"
        )
        # Parse result to get password age and calculate expiry
    except Exception as e:
        # Handle authentication failures
        pass