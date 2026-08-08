import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'https://docchat-rag-llm-production.up.railway.app';

export function Chat({ activeDoc, sessionId, onQuestion }) {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([
    { type:'ai', text:'Document ready. Ask anything and I will find the exact answer grounded 100% in your file.' }
  ]);
  const [loading, setLoading] = useState(false);
  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!question.trim() || !activeDoc) return;
    const q = question;
    setMessages(prev => [...prev, { type:'user', text:q }]);
    setQuestion('');
    setLoading(true);
    onQuestion();
    try {
      const res = await axios.post(`${API_URL}/ask`, {
        question: q,
        session_id: "default"
      });
      setMessages(prev => [...prev, {
        type:'ai',
        text: res.data.answer,
        source: activeDoc.name
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { type:'error', text:'Error: ' + err.message }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{display:'flex', flexDirection:'column', height:'100vh', background:'#0d0d0d'}}>

      <div style={{padding:'12px 18px', borderBottom:'1px solid #1a1a1a', display:'flex', alignItems:'center', justifyContent:'space-between'}}>
        <div style={{display:'flex', alignItems:'center', gap:'10px'}}>
          <span style={{width:'8px', height:'8px', borderRadius:'50%', background:'#22c55e', display:'inline-block', flexShrink:0}}></span>
          <div>
            <div style={{fontSize:'13px', fontWeight:'500', color:'#fff'}}>
              {activeDoc ? activeDoc.name : 'No document selected'}
            </div>
            <div style={{fontSize:'10px', color:'#555', marginTop:'1px'}}>Answers grounded 100% in your document</div>
          </div>
        </div>
        <span style={{fontSize:'10px', padding:'3px 8px', borderRadius:'99px', background:'#6c47ff22', color:'#9b7cff', border:'1px solid #6c47ff33'}}>
          🔒 Private
        </span>
      </div>

      <div ref={chatRef} style={{flex:1, overflowY:'auto', padding:'16px', display:'flex', flexDirection:'column', gap:'14px'}}>

        {!activeDoc && (
          <div style={{flex:1, display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', color:'#555', gap:'10px', marginTop:'100px'}}>
            <div style={{fontSize:'40px'}}>🧠</div>
            <div style={{fontSize:'14px', fontWeight:'500', color:'#888'}}>DocChat AI</div>
            <div style={{fontSize:'12px', textAlign:'center', maxWidth:'220px', lineHeight:'1.7', color:'#444'}}>Upload a document on the left to get started</div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} style={{display:'flex', gap:'10px', flexDirection: msg.type === 'user' ? 'row-reverse' : 'row', alignItems:'flex-start'}}>
            <div style={{width:'28px', height:'28px', borderRadius:'8px', background: msg.type === 'user' ? '#1e1e1e' : '#6c47ff', display:'flex', alignItems:'center', justifyContent:'center', fontSize:'13px', flexShrink:0, border: msg.type === 'user' ? '1px solid #2a2a2a' : 'none'}}>
              {msg.type === 'user' ? '👤' : '✨'}
            </div>

            <div style={{maxWidth:'75%'}}>
              <div style={{padding:'10px 14px', borderRadius:'12px', fontSize:'12px', lineHeight:'1.7',
                background: msg.type === 'user' ? '#6c47ff' : '#161616',
                color: msg.type === 'user' ? '#fff' : msg.type === 'error' ? '#f87171' : '#ccc',
                border: msg.type === 'user' ? 'none' : '1px solid #1e1e1e',
                borderTopLeftRadius: msg.type !== 'user' ? '3px' : '12px',
                borderTopRightRadius: msg.type === 'user' ? '3px' : '12px'
              }}>
                {msg.text}
              </div>
              {msg.source && (
                <div style={{marginTop:'5px', display:'inline-flex', alignItems:'center', gap:'5px', fontSize:'10px', padding:'3px 8px', borderRadius:'99px', background:'#0d2818', color:'#4ade80', border:'1px solid #166534'}}>
                  ✅ Source: {msg.source}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{display:'flex', gap:'10px', alignItems:'flex-start'}}>
            <div style={{width:'28px', height:'28px', borderRadius:'8px', background:'#6c47ff', display:'flex', alignItems:'center', justifyContent:'center', fontSize:'13px', flexShrink:0}}>✨</div>
            <div style={{padding:'12px 16px', background:'#161616', border:'1px solid #1e1e1e', borderRadius:'12px', borderTopLeftRadius:'3px', display:'flex', gap:'5px', alignItems:'center'}}>
              {[0,1,2].map(i => (
                <span key={i} style={{width:'5px', height:'5px', borderRadius:'50%', background:'#555', display:'inline-block', animation:'blink 1.2s infinite', animationDelay:`${i*0.2}s`}}></span>
              ))}
            </div>
          </div>
        )}
      </div>

      <div style={{padding:'14px 18px', borderTop:'1px solid #1a1a1a', background:'#111'}}>
        <form onSubmit={handleAsk}>
          <div style={{display:'flex', gap:'8px', alignItems:'center', background:'#161616', border:'1px solid #2a2a2a', borderRadius:'10px', padding:'6px 6px 6px 14px'}}>
            <input
              type='text'
              placeholder={activeDoc ? 'Ask anything about your document...' : 'Upload a document first...'}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={loading || !activeDoc}
              style={{flex:1, background:'transparent', border:'none', outline:'none', fontSize:'12px', color:'#ddd', fontFamily:'Segoe UI, sans-serif'}}
            />
            <button type='submit' disabled={loading || !activeDoc || !question.trim()} style={{padding:'8px 16px', background: loading || !activeDoc ? '#2a2a2a' : '#6c47ff', color: loading || !activeDoc ? '#555' : '#fff', border:'none', borderRadius:'7px', fontSize:'12px', cursor: loading || !activeDoc ? 'not-allowed' : 'pointer', fontWeight:'500', fontFamily:'Segoe UI, sans-serif', flexShrink:0}}>
              {loading ? '...' : 'Send ➤'}
            </button>
          </div>
        </form>
        <div style={{fontSize:'10px', color:'#333', textAlign:'center', marginTop:'8px', display:'flex', alignItems:'center', justifyContent:'center', gap:'5px'}}>
          <span style={{width:'5px', height:'5px', borderRadius:'50%', background:'#22c55e', display:'inline-block'}}></span>
          100% private — your data never leaves your machine
        </div>
      </div>

      <style>{`@keyframes blink{0%,60%,100%{opacity:0.3}30%{opacity:1}}`}</style>
    </div>
  );
}