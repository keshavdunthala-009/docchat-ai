import { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Chat } from './components/Chat';
import axios from 'axios';

const API_URL = 'https://docchat-rag-llm-production.up.railway.app';

function App() {
  const [activeDoc, setActiveDoc] = useState(null);
  const [docs, setDocs] = useState([]);
  const [questionCount, setQuestionCount] = useState(0);
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    const createSession = async () => {
      try {
        const res = await axios.get(`${API_URL}/session`);
        setSessionId(res.data.session_id);
        console.log("Session created:", res.data.session_id);
      } catch (err) {
        setSessionId(Math.random().toString(36).substring(7));
      }
    };
    createSession();
  }, []);

  return (
    <div style={{display:'grid', gridTemplateColumns:'260px 1fr', height:'100vh', fontFamily:'Segoe UI, sans-serif', background:'#0d0d0d'}}>
      <Sidebar
        docs={docs}
        activeDoc={activeDoc}
        questionCount={questionCount}
        sessionId={sessionId}
        onUpload={(doc) => { setDocs([...docs, doc]); setActiveDoc(doc); }}
        onSelect={setActiveDoc}
      />
      <Chat
        activeDoc={activeDoc}
        sessionId={sessionId}
        onQuestion={() => setQuestionCount(prev => prev + 1)}
      />
    </div>
  );
}

export default App;