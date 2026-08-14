import re  # Import the regular expression module

def validate_password(password):
    # Check if the password contains at least one capital letter, a special character, and has a minimum length of 8 characters
    if re.search(r'[A-Z]', password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', password) and len(password) >= 8:
        return True
    else:
        return False

def signUp(table, node):
    try:
        if node and validate_password(node.key):
            flag = table.Insert(node)
            return flag
        else:
            return False
    except Exception as e:
        print(f"Error in signUp: {e}")
        return False
    
def signIn(table, node):
    try:
        flag = table.CheckValue(node)
        return flag
    except Exception as e:
        print(f"Error in signIn: {e}")
        return False

def forgotPassword(table, node, confirmationPass):
    try:
        if node.key == confirmationPass and validate_password(node.key):
            flag = table.Update(node)
            return flag
        else:
            return False
    except Exception as e:
        print(f"Error in forgotPassword: {e}")
        return False
