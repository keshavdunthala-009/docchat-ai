import { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Chat } from './components/Chat';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'https://docchat-rag-llm-production.up.railway.app';

function App() {
  const [activeDoc, setActiveDoc] = useState(null);
  const [docs, setDocs] = useState([]);
  const [questionCount, setQuestionCount] = useState(0);
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    const initSession = async () => {
      // Check if session exists in sessionStorage
      let existingSession = sessionStorage.getItem('docchat_session');
      
      if (existingSession) {
        // Reuse existing session
        console.log("Reusing session:", existingSession);
        setSessionId(existingSession);
      } else {
        // Create new session
        try {
          const res = await axios.get(`${API_URL}/session`);
          const newSessionId = res.data.session_id;
          sessionStorage.setItem('docchat_session', newSessionId);
          setSessionId(newSessionId);
          console.log("New session created:", newSessionId);
        } catch (err) {
          // Fallback
          const fallbackId = Math.random().toString(36).substring(7);
          sessionStorage.setItem('docchat_session', fallbackId);
          setSessionId(fallbackId);
        }
      }
    };
    
    initSession();
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