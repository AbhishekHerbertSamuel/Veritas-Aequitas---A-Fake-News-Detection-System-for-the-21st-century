from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the serialized model from disk
with open('text_classifier.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_text = ''
    user_input_text = ''  # Variable to hold the user input
    if request.method == 'POST':
        user_input_text = request.form['news_text']
        if user_input_text:  # Ensure that some text was actually typed in by the user
            prediction = model.predict([user_input_text])[0]
            prediction_text = 'Real' if prediction == 1 else 'Fake'
        else:
            prediction_text = 'Please enter some text to classify.'
    return render_template('index.html', prediction_text=prediction_text, user_input_text=user_input_text)
@app.route('/about')
def about():
    return render_template('about.html')  # You will create this about.html template

if __name__ == '__main__':
    app.run(debug=True)

