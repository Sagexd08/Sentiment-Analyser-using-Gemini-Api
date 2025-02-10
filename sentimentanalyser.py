import google.generativeai as genai
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext
from threading import Thread
import json
import time
import re

class SentimentChatbot:
    def __init__(self, api_key):
        """
        Initialize the sentiment analyzer chatbot with enhanced UI and confidence scoring
        """
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.history = []
        self.setup_gui()
        
    def setup_gui(self):
        """
        Create the enhanced chatbot GUI with modern styling
        """
        self.root = tk.Tk()
        self.root.title("Sentiment Analysis Assistant")
        self.root.geometry("800x900")
        
      
        self.setup_styles()
        
       
        container = ttk.Frame(self.root, style="Main.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        header = ttk.Frame(container, style="Header.TFrame")
        header.pack(fill=tk.X, pady=(0, 20))
        
        title = ttk.Label(
            header,
            text="Sentiment Analysis Assistant",
            style="Header.TLabel"
        )
        title.pack(side=tk.LEFT)
   
        self.confidence_frame = ttk.LabelFrame(
            container,
            text="Confidence Score",
            style="Confidence.TLabelframe"
        )
        self.confidence_frame.pack(fill=tk.X, pady=(0, 20))
        

        self.confidence_meter = ttk.Progressbar(
            self.confidence_frame,
            length=200,
            mode='determinate',
            style="Confidence.Horizontal.TProgressbar"
        )
        self.confidence_meter.pack(pady=10, padx=10)
        
        self.confidence_label = ttk.Label(
            self.confidence_frame,
            text="Awaiting analysis...",
            style="Confidence.TLabel"
        )
        self.confidence_label.pack(pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(
            container,
            wrap=tk.WORD,
            width=60,
            height=25,
            font=("Segoe UI", 11),
            bg="#ffffff",
            relief=tk.FLAT
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    
        self.chat_display.tag_configure("user", foreground="#0066cc", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_configure("bot", foreground="#006633", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_configure("timestamp", foreground="#666666", font=("Segoe UI", 9))
        self.chat_display.tag_configure("message", font=("Segoe UI", 11))
        input_frame = ttk.Frame(container, style="Input.TFrame")
        input_frame.pack(fill=tk.X)
        
        self.text_input = ttk.Entry(
            input_frame,
            font=("Segoe UI", 11),
            style="Chat.TEntry"
        )
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        send_button = ttk.Button(
            input_frame,
            text="Analyze",
            command=self.handle_input,
            style="Send.TButton"
        )
        send_button.pack(side=tk.RIGHT)
        self.text_input.bind("<Return>", lambda e: self.handle_input())
        self.display_message("Assistant", "Welcome! I can help you analyze the sentiment of any text. Type your message and press Enter or click Analyze. I'll provide detailed sentiment analysis with confidence scoring.")
        
    def setup_styles(self):
        """
        Configure custom styles for the UI
        """
        style = ttk.Style()
        style.configure("Main.TFrame", background="#f8f9fa")
        style.configure("Header.TFrame", background="#f8f9fa")
        style.configure("Header.TLabel",
                       font=("Segoe UI", 16, "bold"),
                       background="#f8f9fa",
                       foreground="#2c3e50")
        style.configure("Confidence.TLabelframe",
                       background="#f8f9fa",
                       font=("Segoe UI", 10))
        style.configure("Confidence.TLabel",
                       background="#f8f9fa",
                       font=("Segoe UI", 10))
        style.configure("Confidence.Horizontal.TProgressbar",
                       troughcolor="#e9ecef",
                       background="#28a745")
        style.configure("Input.TFrame", background="#f8f9fa")
        style.configure("Chat.TEntry", font=("Segoe UI", 11))
        style.configure("Send.TButton",
                       font=("Segoe UI", 10),
                       padding=5)
    
    def _create_prompt(self, text):
        """
        Create a structured prompt for sentiment analysis with confidence scoring
        """
        return f"""
        Analyze the sentiment of the following text and provide a detailed response in this exact format:
        CONFIDENCE_SCORE: [number between 0-100]
        SENTIMENT: [positive/negative/neutral]
        ANALYSIS: [Your detailed analysis including key emotional indicators and explanation]
        
        Text to analyze: "{text}"
        
        Note: Ensure the confidence score is a single number between 0 and 100, based on how clear and strong the sentiment signals are.
        """
    
    def parse_response(self, response_text):
        """
        Parse the structured response to extract confidence score and analysis
        """
        confidence_match = re.search(r"CONFIDENCE_SCORE:\s*(\d+)", response_text)
        confidence = int(confidence_match.group(1)) if confidence_match else 50
        cleaned_response = re.sub(r"CONFIDENCE_SCORE:\s*\d+\s*\n", "", response_text)
        cleaned_response = re.sub(r"SENTIMENT:\s*", "Sentiment: ", cleaned_response, count=1)
        cleaned_response = re.sub(r"ANALYSIS:\s*", "\nAnalysis: ", cleaned_response, count=1)
        
        return confidence, cleaned_response.strip()
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment and return confidence score with formatted response
        """
        try:
            response = self.model.generate_content(self._create_prompt(text))
            confidence, analysis = self.parse_response(response.text)
            return confidence, analysis
        except Exception as e:
            return 0, f"Sorry, I encountered an error: {str(e)}"
    
    def update_confidence_meter(self, confidence):
        """
        Update the confidence meter and label
        """
        self.confidence_meter["value"] = confidence
        self.confidence_label["text"] = f"Confidence Score: {confidence}%"
        style = ttk.Style()
        if confidence >= 80:
            style.configure("Confidence.Horizontal.TProgressbar", background="#28a745")
        elif confidence >= 50:
            style.configure("Confidence.Horizontal.TProgressbar", background="#ffc107")
        else:
            style.configure("Confidence.Horizontal.TProgressbar", background="#dc3545")
    
    def handle_input(self):
        """
        Handle user input and display response
        """
        text = self.text_input.get().strip()
        if not text:
            return
            
        self.display_message("You", text)
        self.text_input.delete(0, tk.END)
        Thread(target=self.process_and_respond, args=(text,), daemon=True).start()
    
    def process_and_respond(self, text):
        """
        Process the input and display response in a separate thread
        """
        self.display_message("Assistant", "Analyzing...", temporary=True)
        
        confidence, response = self.analyze_sentiment(text)
        
        self.chat_display.delete("end-2c linestart", "end-1c lineend")
        self.display_message("Assistant", response)
        self.update_confidence_meter(confidence)
        
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "input": text,
            "response": response,
            "confidence": confidence
        })
    
    def display_message(self, sender, message, temporary=False):
        """
        Display a message in the chat window with enhanced formatting
        """
        self.chat_display.configure(state='normal')
        
        if self.chat_display.get("1.0", tk.END).strip():
            self.chat_display.insert(tk.END, "\n\n")
        
        timestamp = datetime.now().strftime("%H:%M")
        tag = "user" if sender == "You" else "bot"
        self.chat_display.insert(tk.END, f"{sender}", tag)
        self.chat_display.insert(tk.END, f" ({timestamp})", "timestamp")
        self.chat_display.insert(tk.END, "\n")
        
        self.chat_display.insert(tk.END, message, "message")
        
        self.chat_display.see(tk.END)
        self.chat_display.configure(state='disabled')
    
    def save_history(self, filename="chat_history.json"):
        """
        Save chat history to file
        """
        with open(filename, 'w') as f:
            json.dump(self.history, f, indent=4)
    
    def run(self):
        """
        Start the chatbot
        """
        self.root.mainloop()

def main():
    
    API_KEY = "AIzaSyDpOCz5YzFKAxcjh4CkSqqVLCQkj5F1XXs"
    chatbot = SentimentChatbot(API_KEY)
    chatbot.run()

if __name__ == "__main__":
    main()