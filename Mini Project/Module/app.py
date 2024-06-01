from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize an empty set to store unique entered strings
entered_strings = set()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Check if the user input is not empty and starts with "en" or "EN"
        if user_input.strip() and user_input.upper().startswith(('EN', 'EN')):
            # Check if the entered string is not a duplicate
            if user_input not in entered_strings:
                # Add the entered string to the set
                entered_strings.add(user_input)
        # Render the template passing the set of entered strings
        return render_template('index.html', entered_strings=entered_strings)
    # Render the template with an empty set if no strings have been entered yet
    return render_template('index.html', entered_strings=set())

if __name__ == '__main__':
    app.run(debug=True)
