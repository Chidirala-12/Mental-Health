import csv
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Function to preprocess and tokenize text
def preprocess_text(text, maxlen=None):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(text)
    sequences = tokenizer.texts_to_sequences(text)
    return pad_sequences(sequences, padding='post', maxlen=maxlen)

# Function to load questions and options from a CSV file
def load_questions_responses(csv_file):
    questions = []
    options = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            questions.append(row[0])  # Assuming the first column contains questions
            options.append(row[1:])  # Assuming the remaining columns contain options
    return questions, options

# Load questions and options from CSV
csv_file = "final.csv"  # Adjust the file name/path as necessary
questions, options = load_questions_responses(csv_file)

# Preprocess questions and options
questions_seq = preprocess_text(questions, maxlen=5)

# Define mental health categories and their associated keywords
categories = {
    "anxiety": {"keywords": {"anxious", "panic", "nervous", "worry", "fear"}},
    "depression": {"keywords": {"depressed", "sad", "hopeless", "suicidal", "miserable"}},
    "stress": {"keywords": {"stress", "overwhelmed", "pressure", "tension", "strain"}},
    # Add more categories and keywords as needed
}

# Define function to identify mental health category based on selected options
def identify_mental_health_category(selected_options, categories):
    for category, category_info in categories.items():
        keywords = category_info["keywords"]
        if any(keyword in selected_options for keyword in keywords):
            return category
    return None

# Greet the user
print("Hi! I'm Shubmann. I'll ask you some questions to assess your mental health. Please choose the option that best represents your feelings.")
print("Type 'end' at any time to end the assessment.\n")

# Store user responses
selected_options = []

# Loop through questions and options
for question, option_set in zip(questions, options):
    print(question)
    print("Options:", ", ".join(option_set))
    
    # Get user's choice
    user_choice = input("Your choice: ")
    
    # Check if user wants to end the assessment
    if user_choice.lower() == "end":
        print("Assessment ended.")
        break
    
    selected_options.append(user_choice)

# If the assessment ended prematurely, skip the rest
if "end" not in selected_options:
    # Print the user's selected options
    print("\nYour selected options:")
    for option in selected_options:
        print("- " + option)
    
    # Identify mental health category based on user's selected options
    predicted_category = identify_mental_health_category(selected_options, categories)
    
    # Print the identified mental health category
    if predicted_category:
        print(f"\nBased on your selected options, you may be experiencing: {predicted_category}")
    else:
        print("\nNo matching mental health category found based on your selected options.")