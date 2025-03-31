import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [pixelToMm, setPixelToMm] = useState(0.1193);
  const [image, setImage] = useState(null);
  const [originalUrl, setOriginalUrl] = useState('');
  const [labeledUrl, setLabeledUrl] = useState('');

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!image) return;

    console.log("Submitting image with ratio:", pixelToMm);
    const formData = new FormData();
    formData.append('image', image);
    formData.append('pixel_to_mm_ratio', pixelToMm);

    try {
      const response = await axios.post('http://localhost:8000/api/measure/', formData);
      console.log("API Response:", response.data);

      setOriginalUrl(response.data.original_image);
      setLabeledUrl(response.data.labeled_image);
    } catch (error) {
      alert('Measurement failed. Check the server or image input.');
    }
  };

  return (
    <div className="container">
      <h1>📏 PixiTape</h1>
      <div className="form-card">
        <label htmlFor="ratio" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          Pixel-to-mm Ratio:
          <input
            type="number"
            step="0.0001"
            value={pixelToMm}
            onChange={(e) => setPixelToMm(e.target.value)}
            style={{ marginLeft: '10px', padding: '4px', borderRadius: '4px', border: '1px solid #ccc' }}
          />
          <span
            title="To calculate this, place a known object (like a ruler) in the image and divide its real-world length (in mm) by its pixel length in the image. Example: 100mm object / 850 pixels = 0.1176"
            style={{
              cursor: 'help',
              fontWeight: 'bold',
              border: '1px solid #999',
              borderRadius: '50%',
              width: '18px',
              height: '18px',
              display: 'inline-flex',
              justifyContent: 'center',
              alignItems: 'center',
              backgroundColor: '#eee',
              fontSize: '12px'
            }}
          >
            i
          </span>
        </label>

        <label htmlFor="file">Upload Image:</label>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
        />

        <button onClick={handleSubmit}>Measure Length</button>
      </div>

      {originalUrl && labeledUrl && (
        <div className="result-section"
          style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '40px',
            marginTop: '40px',
            flexWrap: 'wrap'
          }}
        >
          <div style={{ textAlign: 'center', maxWidth: '45%' }}>
            <h3>Original:</h3>
            <img
              src={originalUrl}
              alt="Original"
              style={{
                maxWidth: '100%',
                height: 'auto',
                borderRadius: '8px',
                boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
              }}
            />
          </div>
          <div style={{ textAlign: 'center', maxWidth: '45%' }}>
            <h3>Labeled:</h3>
            <img
              src={labeledUrl}
              alt="Labeled"
              style={{
                maxWidth: '100%',
                height: 'auto',
                borderRadius: '8px',
                boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
