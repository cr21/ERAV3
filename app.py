# app.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import torch
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
import random
import os
import nltk
# nltk.data.path.append('') 
from nltk.corpus import wordnet


app = FastAPI()

# Create a static directory for serving HTML and JS files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define a custom Dataset class
class TextDataset(Dataset):
    def __init__(self, file_path, max_length=10):
        # Load the file and split it into lines
        with open(file_path, 'r') as f:
            self.lines = f.readlines()
        
        # Maximum length of tokens (fixed length)
        self.max_length = max_length

    def __len__(self):
        # Returns the total number of lines in the file
        return len(self.lines)

    def __getitem__(self, idx):
        # Tokenize the line at the given index
        text = self.lines[idx].strip()  # Remove any trailing newlines or spaces
        tokens = text.split()  # Simple tokenization
        
        # Convert tokens to a tensor and pad/truncate them to max_length
        token_ids = torch.tensor([ord(token[0]) for token in tokens], dtype=torch.long)  # Simple token encoding for example
        
        # Pad or truncate the token_ids to the fixed max_length
        if len(token_ids) < self.max_length:
            token_ids = torch.cat([token_ids, torch.zeros(self.max_length - len(token_ids), dtype=torch.long)])
        else:
            token_ids = token_ids[:self.max_length]
        
        # Return tokenized text and a dummy label (e.g., 0)
        label = 0  # Assign dummy label (for example purposes)
        return token_ids, label

def collate_fn(batch):
    texts, labels = zip(*batch)
    texts = [torch.tensor(text) for text in texts]
    texts_padded = pad_sequence(texts, batch_first=True, padding_value=0)
    labels = torch.tensor(labels)
    return texts_padded, labels

def synonym_replacement(sentence, n):
    words = sentence.split()
    for _ in range(n):
        word_to_replace = random.choice(words)
        synonyms = wordnet.synsets(word_to_replace)
        if synonyms:
            synonym = synonyms[0].lemmas()[0].name()
            words = [synonym if word == word_to_replace else word for word in words]
    return ' '.join(words)

# HTML form for file upload
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Text Data Processing</title>
</head>
<body>
    <h1>Upload a Text File</h1>
    <form action="/uploadfile/" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".txt">
        <input type="submit" value="Upload">
    </form>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def main():
    return html_content

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    with open(file_location, "r") as f:
        file_content = f.read()
    
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Text Data Processing</title>
    </head>
    <body>
        <h1>Uploaded File Content</h1>
        <div>
            <pre>{file_content}</pre>
        </div>
        <button onclick="tokenize('{file_location}')">Show Tokenization</button>
        <button onclick="augment()">Show Augmentation</button>
        <button onclick="reset()">Reset</button>  <!-- Reset button -->
        <div id="tokenization-result"></div>
        <div id="augmentation-result"></div>
        
        <script>
            async function tokenize(fileLocation) {{
                const response = await fetch('/tokenize', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ file_location: fileLocation }})
                }});
                const result = await response.json();
                
                // Display token IDs for each line
                let tokenizationResult = '<strong>Tokenization Result:</strong><br>';
                result.token_ids.forEach((ids, index) => {{
                    tokenizationResult += 'Line ' + (index + 1) + ': Token IDs: ' + ids.join(', ') + '<br>';
                }});
                
                document.getElementById('tokenization-result').innerHTML = tokenizationResult;
            }}

            async function augment() {{
                const response = await fetch('/augment', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ content: `{file_content}` }})
                }});
                const result = await response.json();
                
                // Display augmented text for each line
                let augmentationResult = '<strong>Augmentation Result:</strong><br>';
                result.augmented.forEach((line, index) => {{
                    augmentationResult += 'Line ' + (index + 1) + ': ' + line + '<br>';  // Display each augmented line
                }});
                
                document.getElementById('augmentation-result').innerHTML = augmentationResult;
            }}

            function reset() {{
                window.location.href = '/';  // Navigate back to the upload page
            }}
        </script>
    </body>
    </html>
    """)

@app.post("/tokenize")
async def tokenize(content: dict):
    file_location = content['file_location']  # Get the file location from the request
    dataset = TextDataset(file_path=file_location)  # Use the file location to create the dataset

    # Use DataLoader to get all data
    data_loader = DataLoader(dataset, batch_size=1, collate_fn=collate_fn)
    
    token_ids_results = []  # List to store token IDs for each line
    for token_ids, _ in data_loader:
        token_ids_list = token_ids[0].tolist()  # Get the first batch of token IDs as a list
        token_ids_results.append(token_ids_list)  # Append the token IDs for this line

    return {
        "token_ids": token_ids_results,  # Return token IDs for all lines
        "tokens": [' '.join([str(id) for id in ids]) for ids in token_ids_results]  # Convert token IDs to string for display
    }

@app.post("/augment")
async def augment(content: dict):
    text = content['content']
    lines = text.splitlines()  # Split the content into lines
    augmented_lines = []

    for line in lines:
        augmented_line = synonym_replacement(line, n=5)  # Replace 1 synonym for each line
        augmented_lines.append(augmented_line)

    return {"augmented": augmented_lines}  # Return a list of augmented lines

# To run the app, use the command: uvicorn app:app --reload
