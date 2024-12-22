import pandas as pd
import json
import numpy as np

# Global error log to store specific errors
error_log = []

# Load tokens from the json file
def load_tokens(filename="tokens.json"):
    try:
        with open(filename, "r") as file:
            tokens = json.load(file)
        return tokens
    except Exception as e:
        error_log.append({"error": "Error loading tokens", "message": str(e)})
        return {}

# Calculate dot product between two vectors
def calculate_dot_product(vec1, vec2):
    return np.dot(vec1, vec2)

# Normalize the dot product score to percentage
def normalize_score(dot_product, modulus1, modulus2):
    lower_bound = -modulus1 * modulus2  # Opposite vectors
    upper_bound = modulus1 * modulus2   # Identical vectors
    
    # If the vector for which we are comparing is the zero vector, return 50
    if modulus1 == 0 or modulus2 == 0:
        return 50
    
    percentage = ((dot_product - lower_bound) / (upper_bound - lower_bound)) * 100
    percentage = round(percentage, 3)  # Round to 3 decimal places
    return percentage

# Step 1: Load Responses
def load_responses(file_path="responses.xlsx"):
    try:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        error_log.append({"error": "Error loading responses", "message": str(e)})
        return pd.DataFrame()

# Step 2: Generate Matches based on Compatibility (Dot product and normalization)
def generate_matches(df, tokens):
    matches = {}

    for _, row1 in df.iterrows():
        name1 = row1["Name"]
        id1 = row1["ID"]
        token1 = row1["Token"]
        
        # Check if the token matches the ID
        if tokens.get(id1) != token1:
            error_log.append({"error": "Token mismatch", "person": name1, "id": id1, "expected_token": tokens.get(id1), "actual_token": token1})
            continue

        # Extract response vector for this person (now handling 50 questions)
        responses1 = row1.iloc[2:52].values  # Assuming the responses start from column index 2 and go up to column 51
        modulus1 = np.linalg.norm(responses1)  # Magnitude of the first vector

        best_match = None
        best_match_score = -float('inf')  # Start with a very low value

        # Compare with every other person
        for _, row2 in df.iterrows():
            if row1["ID"] == row2["ID"]:  # Skip checking with oneself
                continue

            name2 = row2["Name"]
            id2 = row2["ID"]
            token2 = row2["Token"]

            # Check token match
            if tokens.get(id2) != token2:
                error_log.append({"error": "Token mismatch", "person": name2, "id": id2, "expected_token": tokens.get(id2), "actual_token": token2})
                continue

            # Extract response vector for the other person (now handling 50 questions)
            responses2 = row2.iloc[2:52].values  # Assuming the responses start from column index 2 and go up to column 51
            modulus2 = np.linalg.norm(responses2)  # Magnitude of the second vector

            # Calculate dot product between the two response vectors
            dot_product = calculate_dot_product(responses1, responses2)

            # Normalize the score to percentage
            compatibility_score = normalize_score(dot_product, modulus1, modulus2)

            # Update best match if needed
            if compatibility_score > best_match_score:
                best_match_score = compatibility_score
                best_match = name2

        # Store the best match for this person
        matches[name1] = (best_match, best_match_score)

    return matches

# Step 3: Save the matches to a JSON file
def save_matches_to_json(matches, filename="matches.json"):
    try:
        with open(filename, "w") as file:
            json.dump(matches, file, indent=4)
    except Exception as e:
        error_log.append({"error": "Error saving matches", "message": str(e)})

# Save errors to an error.json file
def save_errors_to_json():
    try:
        # If there are no errors, write an empty list
        if error_log:
            with open("error.json", "w") as file:
                json.dump(error_log, file, indent=4)
        else:
            with open("error.json", "w") as file:
                json.dump([], file, indent=4)  # Empty error file
    except Exception as e:
        print(f"Error saving error log: {e}")

# Main Function
def main():
    tokens = load_tokens()  # Load tokens from the json file
    if not tokens:
        save_errors_to_json()
        return

    df = load_responses()  # Load responses from the Excel file
    if df.empty:
        save_errors_to_json()
        return

    matches = generate_matches(df, tokens)  # Generate the matches
    save_matches_to_json(matches)  # Save the results to a JSON file

    # Save any errors encountered during execution
    save_errors_to_json()
    for name, (match_name, score) in matches.items():
        print(f"{name} matches with {match_name} with score {score}")

if __name__ == "__main__":
    main()
