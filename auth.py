import random
import pandas as pd
import yagmail
import json

# Step 1: Generate Unique Tokens
def generate_unique_token(existing_tokens):
    while True:
        token = f"{random.randint(0, 65535):04x}"  # Generates a 4-digit hexadecimal token
        if token not in existing_tokens:
            existing_tokens.add(token)
            return token

# Step 2: Send Emails
def send_email(to_email, token):
    try:
        # Replace with your email and app-specific password
        yag = yagmail.SMTP("arora.harashish@gmail.com", "wrap iykx nvpi rjjl")
        
        subject = "Your Digital Token for Somebody"
        body = f"Hello,\n\nYour digital token is: {token}\n\nBest Regards,\nSomebody"
        
        yag.send(to_email, subject, body)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# Step 3: Save the token dictionary to a JSON file
def save_tokens_to_json(token_dict, filename="tokens.json"):
    try:
        with open(filename, "w") as file:
            json.dump(token_dict, file, indent=4)
        print(f"Tokens saved to {filename}")
    except Exception as e:
        print(f"Failed to save tokens to JSON: {e}")

# Step 4: Main Function
def main():
    try:
        # Load data from Excel file
        file_path = "input.xlsx"  # Replace with your Excel file path
        df = pd.read_excel(file_path)

        tokens = set()  # Set to store unique tokens
        token_dict = {}  # Dictionary to store ID -> Token mapping

        for _, row in df.iterrows():
            name = row["Name"]
            id = row["ID"]
            email = f"{id}@iitd.ac.in"
            
            if id not in token_dict:  # If token not already generated
                token = generate_unique_token(tokens)
                token_dict[id] = token
                send_email(email, token)
                print(f"Token for {name} ({email}): {token}")
        
        # Save the generated tokens to a JSON file
        save_tokens_to_json(token_dict)

        print("All tokens generated and emails sent!")
    
    except Exception as e:
        print(f"Error in processing: {e}")

if __name__ == "__main__":
    main()
