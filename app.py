from flask import Flask, render_template, request
import csv
from your_python_file import preprocess_text, load_questions_responses, identify_mental_health_category

app = Flask(__name__)

# Load questions and options from CSV
csv_file = "final.csv"  # Adjust the file name/path as necessary
questions, options = load_questions_responses(csv_file)

# Define mental health categories and their associated keywords
categories = {
    "anxiety": {"keywords": {"anxious", "panic", "nervous", "worry", "fear"}},
    "depression": {"keywords": {"depressed", "sad", "hopeless", "suicidal", "miserable"}},
    "stress": {"keywords": {"stress", "overwhelmed", "pressure", "tension", "strain"}},
    # Add more categories and keywords as needed
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_options = []
        for i in range(len(questions)):
            selected_option = request.form.get(f'question_{i+1}')  # Assuming question IDs start from 1
            if selected_option:
                selected_options.append(selected_option)

        # Identify mental health category based on user's selected options
        predicted_category = identify_mental_health_category(selected_options, categories)

        # Render template with result
        return render_template('result.html', predicted_category=predicted_category)

    # Render template with questions and options
    return render_template('index.html', questions=questions, options=options)

if __name__ == '__main__':
    app.run(debug=True)
