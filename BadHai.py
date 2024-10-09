import tkinter as tk
from tkinter import ttk
from ai21 import AI21Client
from ai21.models.chat import ChatMessage, ResponseFormat
from PIL import Image, ImageTk
import random

client = AI21Client(api_key="F0vMbwgybEVr0EmoKFXunpNjLHrqMXVT")

def is_therapy_query(user_input):
    therapy_terms = ["help", "sad", "anxiety", "stress", "feel", "talk", "advice", "therapy", "depressed"]
    return any(term in user_input.lower() for term in therapy_terms)

def get_bot_response():
    user_input = entry.get()
    
    if user_input.lower() in ["exit", "quit"]:
        conversation_box.insert(tk.END, "Bot: Goodbye\n", "bot")
        root.quit()
        return

    conversation_box.insert(tk.END, f"You: {user_input}\n", "user")
    
    if is_therapy_query(user_input):
        prompt = f"Please provide supportive and empathetic responses to the following user query:\nUser Query: {user_input}\n"
        
        messages = [
            ChatMessage(
                role="system",
                content="You are a mental therapist who provides empathetic and supportive responses."
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
        
        if not assistant_response.strip():
            assistant_response = "I'm sorry, I didn't understand that. Can you please rephrase?"

        conversation_box.insert(tk.END, f"Bot: {assistant_response}\n", "bot")
    else:
        conversation_box.insert(tk.END, "Bot: I'm here to talk and provide support. Please share what's on your mind.\n", "bot")

    entry.delete(0, tk.END)
    entry.insert(0, "Enter the text...") 

def get_affirmation():
    affirmations = [
        "You are enough just as you are.",
        "You have the power to create change.",
        "Believe in yourself and all that you are.",
        "Every day may not be good, but there's something good in every day.",
        "You are capable of amazing things."
    ]
    affirmation = random.choice(affirmations)
    conversation_box.insert(tk.END, f"Bot: {affirmation}\n", "bot")

def show_breathing_exercise():
    breathing_instruction = "Let's do a quick breathing exercise. Inhale deeply through your nose for 4 seconds...\nHold for 4 seconds...\nExhale slowly through your mouth for 4 seconds...\nRepeat."
    conversation_box.insert(tk.END, f"Bot: {breathing_instruction}\n", "bot")

root = tk.Tk()
root.title("Mental Therapist Bot")
root.geometry("600x500")
root.resizable(False, False)

icon_image = Image.open("icon.png")
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)

def set_gradient_background(canvas, width, height):
    gradient_color1 = "#2980b9"  
    gradient_color2 = "#8e44ad"  
    for i in range(height):
        color = f'#{int((i/height)*255):02x}{int((1 - i/height)*255):02x}ff'
        canvas.create_line(0, i, width, i, fill=color)

canvas = tk.Canvas(root, width=600, height=500)
canvas.pack()
set_gradient_background(canvas, 600, 500)

FONT = ("Arial", 12)
USER_FONT = ("Arial", 12, "bold")
BOT_FONT = ("Arial", 12)

conversation_frame = tk.Frame(root, bg="#34495e")
conversation_frame.place(relx=0.5, rely=0.4, anchor='center', width=580, height=300)

scrollbar = tk.Scrollbar(conversation_frame, width=15)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

conversation_box = tk.Text(conversation_frame, wrap='word', height=20, width=50, font=FONT, fg="#ecf0f1", bg="#2c3e50", yscrollcommand=scrollbar.set)
conversation_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
scrollbar.config(command=conversation_box.yview)

conversation_box.tag_configure("user", foreground="#1abc9c", font=USER_FONT)
conversation_box.tag_configure("bot", foreground="#f1c40f", font=BOT_FONT)

entry_frame = tk.Frame(root, bg="#2c3e50")
entry_frame.pack(pady=10, padx=10, fill=tk.X)

entry = tk.Entry(entry_frame, width=40, font=FONT, bg="#34495e", fg="#ecf0f1", insertbackground="white")
entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

entry.insert(0, "Enter the text...") 
entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END) if entry.get() == "Enter the text..." else None)
entry.bind("<FocusOut>", lambda e: entry.insert(0, "Enter the text...") if entry.get() == "" else None)

send_button = tk.Button(entry_frame, text="Send", command=get_bot_response, font=("Arial", 14), bg="#3498db", fg="white", bd=0, relief="flat", width=10)
send_button.pack(side=tk.RIGHT, padx=10)

def on_enter(event):
    send_button.config(bg="#5dade2")

def on_leave(event):
    send_button.config(bg="#3498db")

send_button.bind("<Enter>", on_enter)
send_button.bind("<Leave>", on_leave)

affirmation_button = tk.Button(entry_frame, text="Affirmation", command=get_affirmation, font=("Arial", 14), bg="#27ae60", fg="white", bd=0, relief="flat", width=10)
affirmation_button.pack(side=tk.RIGHT, padx=10)

breathing_button = tk.Button(entry_frame, text="Breath Exercise", command=show_breathing_exercise, font=("Arial", 14), bg="#e67e22", fg="white", bd=0, relief="flat", width=10)
breathing_button.pack(side=tk.RIGHT, padx=10)

# Add label for instruction
instruction_label = tk.Label(root, text="Enter your thoughts or feelings:", font=("Arial", 12), bg="#2980b9", fg="white")
instruction_label.pack(pady=(10, 0))

# Customize scrollbar style
scrollbar.config(bg="#34495e", troughcolor="#2c3e50", borderwidth=0)
conversation_box.tag_configure("bot", background="#2c3e50")

root.bind('<Return>', lambda event: get_bot_response())

root.mainloop()
