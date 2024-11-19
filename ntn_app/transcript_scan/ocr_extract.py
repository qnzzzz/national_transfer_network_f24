import numpy as np
import PyPDF2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from ntn_app.models import CollegeProfile

# Pre-defined training data
texts = [
    "PS50029 Introduction to issues in health and health beliefs 6 165 Pass",
    "EXTRA Units Unit Code Name Credits Awarded Attempt Mark (%) Outcome PS00000 EXTRA UNIT Academic integrity training & test 0 1 Pass",
    "Student-Generated Transcript Student Name",
    "PS50033 Advanced research design in health 6 172 Pass",
    "Note: modules marked as AUDIT or EXTRA do not count towards the Final Award.",
    "PS50148 Multivariate statistics for use in health contexts 6 1 65 Pass",
    "PS50112 Advanced statistics for use in health contexts 6 1 64 Pass",
    "PS50160 21st century public health psychology 6 1 64 Pass",
    # "PS50031 Communication in health 6 164 Pass",
    # "PS50161 Advanced qualitative analysis 6 168 Pass",
    # "PS50162 Informing interventions with health psychology 6 169"
]
labels = [1, 0, 0, 1, 0, 1, 1, 1]

# Initialize tokenizer
tokenizer = Tokenizer(num_words=1000)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
train_data = pad_sequences(sequences, maxlen=100)
train_labels = np.array(labels, dtype='int32')

# Initialize and train the model
model = Sequential([
    Embedding(1000, 16),
    LSTM(32),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(train_data, train_labels, epochs=30, verbose=1)

def process_pdf(file_stream):
    # Fetch all college names from CollegeProfile model
    college_names = CollegeProfile.objects.values_list('college_name', flat=True)

    # Read and process the PDF file directly from a file stream
    reader = PyPDF2.PdfReader(file_stream)
    pdf_text = ""
    detected_college = None
    
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pdf_text += page_text
            
    # Identify if any college name appears in the concatenated text
    for college_name in college_names:
        if college_name in pdf_text:
            detected_college = college_name
            break  # Stop after finding the first match
        
    # Segmenting the PDF text
    pdf_segments = [seg for seg in pdf_text.splitlines() if seg.strip()]
    
    # Tokenizing and padding sequences
    test_sequences = tokenizer.texts_to_sequences(pdf_segments)
    test_data = pad_sequences(test_sequences, maxlen=100)
    
    # Making predictions
    predictions = model.predict(test_data)
    
    results = []
    for i, pred in enumerate(predictions):
        # results.append((pdf_segments[i]))
        if pred[0] > 0.7:
            # results.append((pdf_segments[i]) + " " + str(pred[0].item()))
            results.append((pdf_segments[i]))
    # print(results)
    return results, detected_college
