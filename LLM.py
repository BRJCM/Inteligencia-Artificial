# Import necessary libraries
import openai
from PyPDF2 import PdfReader

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Load the text from the PDF
pdf_path = "/mnt/data/IA_pdf.pdf"
pdf_text = extract_text_from_pdf(pdf_path)

# Initialize the LLM (for this example, we use OpenAI's GPT-3, but you can replace it with any open source LLM)
openai.api_key = "your_openai_api_key"  # Replace with your API key

# Function to find relevant text in the PDF
def find_relevant_text(pdf_text, question):
    # For simplicity, we use basic keyword search. This can be enhanced with more sophisticated NLP techniques.
    relevant_lines = []
    lines = pdf_text.split('\n')
    for line in lines:
        if any(word in line.lower() for word in question.lower().split()):
            relevant_lines.append(line)
    return '\n'.join(relevant_lines)

# Function to ask questions to the LLM
def ask_question_to_llm(question, context):
    prompt = f"Based on the following context, please answer the question:\n\n{context}\n\nQuestion: {question}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Define the questions based on the PDF content
questions = [
    "What are some common applications of generative AI in content creation?",
    "How can generative AI assist in personal and professional support?",
    "What are the benefits of using generative AI for learning and education?"
]

# Function to get answers to the questions along with the relevant text from the PDF
def get_answers_with_context(questions, pdf_text):
    qa_pairs = []
    for question in questions:
        context = find_relevant_text(pdf_text, question)
        answer = ask_question_to_llm(question, context)
        qa_pairs.append((question, context, answer))
    return qa_pairs

# Get answers to the defined questions
qa_pairs = get_answers_with_context(questions, pdf_text)

# Print questions, relevant text, and answers
for question, context, answer in qa_pairs:
    print(f"Question: {question}\nRelevant Text: {context}\nAnswer: {answer}\n")

# Save the questions, relevant text, and answers to a notebook file
with open("IA_Generative_Use_Cases_QA.ipynb", "w") as notebook_file:
    notebook_file.write("# Questions, Relevant Text, and Answers based on '100 cases of Generative AI'\n")
    for question, context, answer in qa_pairs:
        notebook_file.write(f"## Question: {question}\n")
        notebook_file.write(f"**Relevant Text:** {context}\n")
        notebook_file.write(f"**Answer:** {answer}\n\n")
