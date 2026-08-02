import { useState } from 'react';
import axios from 'axios';

export function Chat() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/ask', { question });
      setMessages([...messages,
        { type: 'user', text: question },
        { type: 'assistant', text: response.data.answer, chunks: response.data.chunk_count }
      ]);
      setQuestion('');
    } catch (error) {
      setMessages([...messages, { type: 'error', text: 'Error: ' + error.message }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{padding: '20px', border: '1px solid #ddd', borderRadius: '8px'}}>
      <h2>Ask Questions</h2>
      <div style={{border: '1px solid #ddd', height: '400px', overflowY: 'auto', padding: '10px', marginBottom: '20px', borderRadius: '4px'}}>
        {messages.length === 0 ? (
          <p style={{color: '#999', textAlign: 'center'}}>Ask a question...</p>
        ) : (
          messages.map((msg, i) => (
            <div key={i} style={{marginBottom: '15px', padding: '10px', backgroundColor: msg.type === 'user' ? '#e3f2fd' : msg.type === 'error' ? '#ffebee' : '#f1f8e9', borderRadius: '4px'}}>
              <strong>{msg.type === 'user' ? 'You:' : msg.type === 'error' ? 'Error:' : 'Answer:'}</strong>
              <p style={{marginTop: '5px'}}>{msg.text}</p>
              {msg.chunks && <small>{msg.chunks} chunk retrieved</small>}
            </div>
          ))
        )}
      </div>
      <form onSubmit={handleAsk} style={{display: 'flex', gap: '10px'}}>
        <input type='text' placeholder='Ask a question...' value={question} onChange={(e) => setQuestion(e.target.value)} disabled={loading} style={{flex: 1, padding: '10px', borderRadius: '4px', border: '1px solid #ddd'}}/>
        <button type='submit' disabled={loading} style={{padding: '10px 20px', backgroundColor: '#2196F3', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer'}}>
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </form>
    </div>
  );
}
