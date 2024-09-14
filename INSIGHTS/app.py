from flask import Flask, request, jsonify, render_template
import openai
import PyPDF2

app = Flask(__name__)

# Configurações da API OpenAI
openai.api_key = 'SUA API OPENAI AQUI'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        pdf_text = extract_text_from_pdf(file)
        return jsonify({'text': pdf_text})

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    document_text = data.get('document_text')

    if not question or not document_text:
        return jsonify({'error': 'Missing question or document text'}), 400

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{document_text}\n\nQuestion: {question}"}
        ]
    )

    answer = response.choices[0].message['content'].strip()
    return jsonify({'answer': answer})

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)
