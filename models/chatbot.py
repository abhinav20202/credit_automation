import pandas as pd
from transformers import pipeline
import os
print("Starting Chatbot Service...")


class ChatbotService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Initializing Chatbot Model...")
            cls._instance = super(ChatbotService, cls).__new__(cls)
            # Initialize the text-generation pipeline
            cls._instance.chatbot = pipeline("text-generation", model="microsoft/DialoGPT-small")
            # Load user data from CSV
            CSV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csp.csv')
            cls._instance.user_data = pd.read_csv(CSV_FILE)
            print("Chatbot Model and User Data Initialized.")
        return cls._instance

    def get_user_context(self, username: str) -> str:
        """Creates a context string from user data."""
        user_info = self.user_data[self.user_data["username"] == username]
        if user_info.empty:
            return "No data found for this user."

        # Get the most recent record for the user
        user_info = user_info.iloc[-1]

        # Create a summary of the user's financial health
        context = (
            f"You are a helpful financial assistant. Here is the user's current financial summary:\n"
            f"- Gross Monthly Income: ${user_info['gross_monthly_income']}\n"
            f"- Total Monthly Debt Payments: ${user_info['total_monthly_debt_payments']}\n"
            f"- Total Credit Limit: ${user_info['total_credit_limit']}\n"
            f"- Credit History Length: {user_info['credit_history_length_months']} months\n"
            f"- Recent Credit Inquiries (last 6m): {user_info['new_credit_inquiries_last_6m']}\n"
            f"- Late Payments: {user_info['late_payment_count']}\n"
            f"- Most Recent Credit Score: {user_info['score_of_last_month']}\n\n"
            f"Based on this, provide helpful and personalized advice. The user has just asked:"
        )
        return context

    def get_response(self, user_input: str, username: str, history_str: str = "") -> tuple[str, str]:
        """
        Generates a response from the chatbot, maintaining conversation history as a string.
        """
        context = self.get_user_context(username)
        
        # Format the input with context and history for the model
        full_input = f"{context}\n{history_str}You: {user_input}\nBot:"
        
        # Generate the response.
        # The pad_token_id is set to the eos_token_id for open-ended generation.
        # We set max_new_tokens to control the output size and truncate to avoid warnings.
        generated_outputs = self.chatbot(
            full_input,
            max_new_tokens=100,  # Allow for a response of up to 100 tokens
            truncation=True,
            pad_token_id=self.chatbot.tokenizer.eos_token_id
        )
        
        # The generated text includes the input prompt, so we need to remove it.
        generated_text = generated_outputs[0]['generated_text']
        bot_reply = generated_text.replace(full_input, "").strip()

        # The model might continue the conversation, so we cut it off at the next turn.
        if "You:" in bot_reply:
            bot_reply = bot_reply.split("You:")[0].strip()
        if "Bot:" in bot_reply:
            bot_reply = bot_reply.split("Bot:")[0].strip()

        new_history = f"{history_str}You: {user_input}\nBot: {bot_reply}\n"
        return bot_reply, new_history

# Create a single instance to be used by the API
chatbot_instance = ChatbotService()

if __name__ == "__main__":
    print("enter name:- ")
    username = input("Please enter your username: ")

    # Check if the username exists
    if username not in chatbot_instance.user_data['username'].unique():
        print(f"Error: Username '{username}' not found in the database.")
    else:
        print(f"Welcome, {username}! You can start chatting with the financial assistant.")
        print("Type 'exit' or 'quit' to end the conversation.")
        print("-" * 30)

        history = ""
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Bot: Goodbye!")
                break
            
            # Get the personalized response
            bot_reply, history = chatbot_instance.get_response(user_input, username, history)
            print(f"Bot: {bot_reply}")