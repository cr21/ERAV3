import React, { useState } from 'react';
import './App.css';

function App() {
    const [selectedOption, setSelectedOption] = useState('');
    const [fileContent, setFileContent] = useState('');
    const [imageSrc, setImageSrc] = useState(''); // New state for image source
    const [error, setError] = useState('');
    const [isFileUploaded, setIsFileUploaded] = useState(false); // State to track file upload

    const handleOptionChange = (event) => {
        setSelectedOption(event.target.value);
        setFileContent(''); // Reset file content when changing options
        setImageSrc(''); // Reset image source
        setError(''); // Reset error message
        setIsFileUploaded(false); // Reset file upload state
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            if (selectedOption === 'text') {
                uploadFile(file); // Call the upload function for text files
            } else if (selectedOption === 'image') {
                displayImage(file); // Call the function to display the image
            }
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

    const displayImage = (file) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            setImageSrc(reader.result); // Set the image source to display
            setIsFileUploaded(true); // Set file upload state to true
        };
        reader.readAsDataURL(file); // Read the file as a data URL
    };

    const resetForm = () => {
        setFileContent(''); // Clear the file content
        setImageSrc(''); // Clear the image source
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
                    {isFileUploaded && (
                        <div>
                            <h3>File Content:</h3>
                            <pre>{fileContent}</pre>
                            {error && <p style={{ color: 'red' }}>{error}</p>}
                            <button onClick={resetForm}>Reset</button>
                        </div>
                    )}
                </div>
            )}

            {selectedOption === 'image' && (
                <div>
                    <h2>Image Form</h2>
                    <input type="file" accept="image/*" onChange={handleFileChange} />
                    {isFileUploaded && imageSrc && ( // Show image if uploaded
                        <div>
                            <h3>Uploaded Image:</h3>
                            <img src={imageSrc} alt="Uploaded" style={{ maxWidth: '300px', maxHeight: '300px' }} />
                            <button onClick={resetForm}>Reset</button>
                        </div>
                    )}
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
