# app.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import torch
from torch.utils.data import Dataset, DataLoader
from torchtext.data.utils import get_tokenizer
import random
import os

app = FastAPI()

# Define a custom Dataset class
class TextDataset(Dataset):
    def __init__(self, file_path, max_length=10):
        # Load the file and split it into lines
        with open(file_path, 'r') as f:
            self.lines = f.readlines()
        
        # Tokenizer
        self.tokenizer = get_tokenizer('basic_english')
        
        # Maximum length of tokens (fixed length)
        self.max_length = max_length

    def __len__(self):
        # Returns the total number of lines in the file
        return len(self.lines)

    def __getitem__(self, idx):
        # Tokenize the line at the given index
        text = self.lines[idx].strip()  # Remove any trailing newlines or spaces
        tokens = self.tokenizer(text)
        
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
    # Create the temp directory if it doesn't exist
    os.makedirs("temp", exist_ok=True)  # Create 'temp' directory if it doesn't exist

    # Save the uploaded file temporarily
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # Read the content of the uploaded file
    with open(file_location, "r") as f:
        file_content = f.read()
    
    # Clean up the temporary file
    os.remove(file_location)

    # Return HTML response with file content
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Text Data Processing</title>
    </head>
    <body>
        <h1>Uploaded File Content</h1>
        <div>
            <pre>{file_content}</pre>  <!-- Display file content here -->
        </div>
        <a href="/">Upload another file</a>  <!-- Link to go back to the upload page -->
    </body>
    </html>
    """)

# To run the app, use the command: uvicorn app:app --reload
