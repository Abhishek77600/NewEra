
  #YhTh8w4gexlbValOY90lm0GyV1y2awNzpnGJHVkO
import cohere

# Replace with your actual Cohere API key
API_KEY = "YhTh8w4gexlbValOY90lm0GyV1y2awNzpnGJHVkO"

# Initialize Cohere Client
co = cohere.Client(API_KEY)

try:
    # Generate response from Cohere
    response = co.chat(
        message="Hello!",
        model="command-r"  # Use "command-r" or "command" based on availability
    )

    # Print the AI's response
    print(response.text)

except cohere.CohereAPIError as e:
    print(f"Cohere API Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
