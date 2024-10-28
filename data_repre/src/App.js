import React, { useState } from 'react';
import './App.css';

function App() {
    const [selectedOption, setSelectedOption] = useState('');
    const [fileContent, setFileContent] = useState('');
    const [error, setError] = useState('');
    const [isFileUploaded, setIsFileUploaded] = useState(false); // New state to track file upload

    const handleOptionChange = (event) => {
        setSelectedOption(event.target.value);
        setFileContent(''); // Reset file content when changing options
        setError(''); // Reset error message
        setIsFileUploaded(false); // Reset file upload state
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            uploadFile(file); // Call the upload function
        }
    };

    const uploadFile = async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://127.0.0.1:8000/uploadfile/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setFileContent(data.content); // Set the file content from the response
            setIsFileUploaded(true); // Set file upload state to true
        } catch (error) {
            setError('Error uploading file: ' + error.message);
        }
    };

    const resetForm = () => {
        setFileContent(''); // Clear the file content
        setError(''); // Clear any error messages
        setSelectedOption(''); // Reset the selected option
        setIsFileUploaded(false); // Reset file upload state
    };

    return (
        <div className="App">
            <h1>Select an Option</h1>
            <form>
                <label>
                    <input type="radio" value="text" checked={selectedOption === 'text'} onChange={handleOptionChange} />
                    Text
                </label>
                <br />
                <label>
                    <input type="radio" value="image" checked={selectedOption === 'image'} onChange={handleOptionChange} />
                    Image
                </label>
                <br />
                <label>
                    <input type="radio" value="audio" checked={selectedOption === 'audio'} onChange={handleOptionChange} />
                    Audio
                </label>
                <br />
                <label>
                    <input type="radio" value="3d" checked={selectedOption === '3d'} onChange={handleOptionChange} />
                    3D
                </label>
            </form>

            {selectedOption === 'text' && (
                <div>
                    <h2>Text Form</h2>
                    <input type="file" accept=".txt" onChange={handleFileChange} />
                    {isFileUploaded && ( // Show content and reset button only if file is uploaded
                        <div>
                            <h3>File Content:</h3>
                            <pre>{fileContent}</pre> {/* Display the file content */}
                            {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error message */}
                            <button onClick={resetForm}>Reset</button> {/* Reset button */}
                        </div>
                    )}
                </div>
            )}

            {selectedOption === 'image' && (
                <div>
                    <h2>Image Form</h2>
                    <form>
                        <input type="file" accept="image/*" />
                        <button type="submit">Upload</button>
                    </form>
                </div>
            )}

            {selectedOption === 'audio' && (
                <div>
                    <h2>Audio Form</h2>
                    <form>
                        <input type="file" accept="audio/*" />
                        <button type="submit">Upload</button>
                    </form>
                </div>
            )}

            {selectedOption === '3d' && (
                <div>
                    <h2>3D Form</h2>
                    <form>
                        <input type="file" accept=".glb,.gltf" />
                        <button type="submit">Upload</button>
                    </form>
                </div>
            )}
        </div>
    );
}

export default App;
