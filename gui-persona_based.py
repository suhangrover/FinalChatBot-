import tkinter as tk
from tkinter import ttk
from ai21 import AI21Client
from ai21.models.chat import ChatMessage, ResponseFormat

client = AI21Client(api_key="F0vMbwgybEVr0EmoKFXunpNjLHrqMXVT")

def handle_general_conversation(user_input):
    general_responses = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! How can I help?",
        "how are you": "I'm just a chatbot, but I'm here to assist you!",
        "who are you": "I'm your research assistant chatbot, ready to help with your case evaluations.",
        "what is your purpose": "I assist with evaluating text extracts based on specific case information.",
        "what are you here for": "I assist with evaluating text extracts based on specific case information.",
        "define your existence": "I assist with evaluating text extracts based on specific case information.",
        "what's up": "Not much, just here to help! What’s on your mind?",
        "tell me something interesting": "Did you know that honey never spoils? It can last for thousands of years!",
        "what can you do": "I can help evaluate text relevance, assist with research, and provide information on various topics.",
        "are you a human": "Nope, I'm just a bot! But I'm here to help with your questions.",
        "bye": "Goodbye! Have a great day!",
        "see you later": "See you later! Feel free to return anytime.",
        "take care": "You too! Take care!"
    }
    
    normalized_input = user_input.lower().strip()
    if normalized_input in general_responses:
        return general_responses[normalized_input]
    return None

def get_bot_response():
    user_input = entry.get()
    
    if user_input.lower() in ["exit", "quit"]:
        conversation_box.insert(tk.END, "Bot: Goodbye\n", "bot")
        root.quit()
        return
    
    general_response = handle_general_conversation(user_input)
    
    if general_response:
        conversation_box.insert(tk.END, f"You: {user_input}\n", "user")
        conversation_box.insert(tk.END, f"Bot: {general_response}\n", "bot")
    else:
        conversation_box.insert(tk.END, f"You: {user_input}\n", "user")
        
        prompt = f"""Evaluate if the following text extract is relevant to the case at hand.
Extract:
{user_input}
Case:
[Please describe the case context here]  
        """
        
        messages = [
            ChatMessage(
                role="system",
                content="You are a retarded mental therapist"
            ),
            ChatMessage(
                role="user",
                content=prompt
            )
        ]
        
        response = client.chat.completions.create(
            model="jamba-instruct",
            messages=messages,
            n=1,
            max_tokens=1024,
            temperature=0.7,
            response_format=ResponseFormat(type="text"),
        )
        
        assistant_response = response.choices[0].message.content
        
        conversation_box.insert(tk.END, f"Bot: {assistant_response}\n", "bot")
    
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("AI21 Chatbot - Research Assistant")

root.geometry("600x500")
root.resizable(False, False)
root.configure(bg="#1e1e2f")

FONT = ("Helvetica", 12)
USER_FONT = ("Helvetica", 12, "bold")
BOT_FONT = ("Helvetica", 12)

conversation_frame = tk.Frame(root, bg="#1e1e2f")
conversation_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(conversation_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

conversation_box = tk.Text(conversation_frame, wrap='word', height=20, width=50, font=FONT, fg="#F0F0F0", bg="#2c2c34", yscrollcommand=scrollbar.set)
conversation_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
scrollbar.config(command=conversation_box.yview)

conversation_box.tag_configure("user", foreground="#56dbab", font=USER_FONT)
conversation_box.tag_configure("bot", foreground="#f1c40f", font=BOT_FONT)

entry_frame = tk.Frame(root, bg="#1e1e2f")
entry_frame.pack(pady=10, padx=10, fill=tk.X)

entry = tk.Entry(entry_frame, width=40, font=FONT, bg="#2c2c34", fg="#F0F0F0", insertbackground="white")
entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

send_button = ttk.Button(entry_frame, text="Send", command=get_bot_response, style="TButton")
send_button.pack(side=tk.RIGHT, padx=10)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=10, background="#3e3e52", foreground="white")
style.map("TButton", background=[('active', '#565675')])

root.bind('<Return>', lambda event: get_bot_response())

root.mainloop()
