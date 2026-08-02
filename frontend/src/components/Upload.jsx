import { useState } from 'react';
import axios from 'axios';

export function Upload({ onSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post('http://localhost:8000/upload', formData);
      setMessage('Uploaded: ' + response.data.filename);
      setFile(null);
      onSuccess();
    } catch (error) {
      setMessage('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{padding: '20px', border: '1px solid #ddd', borderRadius: '8px', marginBottom: '20px'}}>
      <h2>Upload Document</h2>
      <form onSubmit={handleUpload} style={{display: 'flex', gap: '10px'}}>
        <input type='file' accept='.pdf,.txt' onChange={(e) => setFile(e.target.files[0])} disabled={loading} style={{flex: 1, padding: '8px'}}/>
        <button type='submit' disabled={loading || !file} style={{padding: '8px 16px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer'}}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}
