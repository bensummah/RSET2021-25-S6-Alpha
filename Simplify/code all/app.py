
from flask import Flask, render_template, request
from transformers import T5ForConditionalGeneration, T5Tokenizer
import os

app = Flask(__name__)

# Load the trained model and tokenizer (outside function for efficiency)
model_path = "C:\\Users\\adity\\OneDrive\\Desktop\\checkpoint 4500"  # Update path to your model
model = T5ForConditionalGeneration.from_pretrained(model_path)
tokenizer = T5Tokenizer.from_pretrained("t5-small")

def simplify_text(input_text):
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    output_ids = model.generate(input_ids, max_length=512)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output_text

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_text = request.form["inputText"]
        simplified_text = simplify_text(input_text)
        return simplified_text
    else:
        return render_template("soln.html", simplified_text="")

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(port=5500)
