from flask import Flask, render_template, request, jsonify
import spacy
import PyPDF2
import docx2txt

app = Flask(__name__)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading en_core_web_sm model...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# Function to extract text from different file types
def extract_text_from_file(file):
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension == 'pdf':
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    elif file_extension == 'docx':
        try:
            text = docx2txt.process(file)
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return None
    elif file_extension == 'txt':
        try:
            text = file.read().decode('utf-8')
            return text
        except Exception as e:
            print(f"Error reading TXT: {e}")
            return None
    else:
        return None

# Translation speed estimates (words per hour for now)
TRANSLATION_SPEEDS = {
    'chinese': 300,
    'spanish': 600,
    'arabic': 250,
    'portuguese': 550,
    'russian': 400,
    'german': 500,
    'french': 650,
    'japanese': 200
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    text = request.form.get('text')  # Get text from textarea

    if 'fileInput' in request.files:
        file = request.files['fileInput']
        if file.filename != '':
            text = extract_text_from_file(file)
            if text is None:
                return jsonify({'error': 'Error extracting text from file'})

    if not text:
        return jsonify({'error': 'No text to analyze'})

    doc = nlp(text)
    num_words = len(doc)
    num_sentences = len(list(doc.sents))
    complexity = num_words / num_sentences if num_sentences else 0
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    translation_times = {}
    for language, speed in TRANSLATION_SPEEDS.items():
        translation_time_hours = num_words / speed
        translation_times[language] = round(translation_time_hours, 2)  # Round to 2 decimal places

    return jsonify({
        'word_count': num_words,
        'sentence_count': num_sentences,
        'complexity': complexity,
        'translation_times': translation_times
    })

if __name__ == '__main__':
    app.run(debug=True)