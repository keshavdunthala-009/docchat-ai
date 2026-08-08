import { useState } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'https://docchat-rag-llm-production.up.railway.app';

export function Sidebar({ docs, activeDoc, questionCount, sessionId, onUpload, onSelect }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState('');

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file || !sessionId) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      // Use unique session_id per user!
      const res = await axios.post(
        `${API_URL}/upload?session_id=${sessionId}`,
        formData
      );
      onUpload({ name: res.data.filename });
      setMsg('✅ Uploaded!');
      setFile(null);
    } catch (err) {
      setMsg('❌ Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{background:'#111', borderRight:'1px solid #1e1e1e', display:'flex', flexDirection:'column', padding:'16px', gap:'14px', height:'100vh', overflow:'hidden'}}>

      {/* Logo */}
      <div style={{display:'flex', alignItems:'center', gap:'10px', paddingBottom:'14px', borderBottom:'1px solid #1e1e1e'}}>
        <div style={{width:'34px', height:'34px', borderRadius:'8px', background:'#6c47ff', display:'flex', alignItems:'center', justifyContent:'center', flexShrink:0}}>
          <span style={{fontSize:'16px'}}>🧠</span>
        </div>
        <div>
          <div style={{fontSize:'14px', fontWeight:'600', color:'#fff'}}>DocChat AI</div>
          <div style={{fontSize:'10px', color:'#555', marginTop:'1px'}}>RAG-powered document Q&A</div>
        </div>
      </div>

      {/* Upload Zone */}
      <div style={{border:'1px dashed #2a2a2a', borderRadius:'10px', padding:'16px', textAlign:'center', background:'#161616'}}>
        <div style={{fontSize:'22px', color:'#444', marginBottom:'6px'}}>📤</div>
        <div style={{fontSize:'11px', color:'#555', marginBottom:'10px', lineHeight:'1.5'}}>Drop your PDF here or click to browse</div>
        <form onSubmit={handleUpload}>
          <input
            type='file'
            accept='.pdf,.txt'
            onChange={(e) => setFile(e.target.files[0])}
            style={{fontSize:'11px', marginBottom:'8px', width:'100%', color:'#888'}}
          />
          <button
            type='submit'
            disabled={loading || !file || !sessionId}
            style={{
              width:'100%',
              padding:'7px',
              background: loading || !file ? '#1a1a1a' : '#6c47ff',
              color: loading || !file ? '#555' : '#fff',
              border:'1px solid #2a2a2a',
              borderRadius:'6px',
              cursor: loading || !file ? 'not-allowed' : 'pointer',
              fontSize:'11px',
              fontFamily:'Segoe UI, sans-serif'
            }}
          >
            {loading ? 'Uploading...' : '⬆ Upload'}
          </button>
        </form>
        {msg && <p style={{fontSize:'11px', color:'#4ade80', marginTop:'6px'}}>{msg}</p>}
      </div>

      {/* Documents */}
      {docs.length > 0 && (
        <>
          <div style={{fontSize:'10px', fontWeight:'600', color:'#444', letterSpacing:'0.8px', textTransform:'uppercase'}}>
            Documents
          </div>
          <div style={{display:'flex', flexDirection:'column', gap:'6px', overflowY:'auto'}}>
            {docs.map((doc, i) => (
              <div
                key={i}
                onClick={() => onSelect(doc)}
                style={{
                  display:'flex',
                  alignItems:'center',
                  gap:'8px',
                  padding:'9px 10px',
                  borderRadius:'8px',
                  background: activeDoc?.name === doc.name ? '#1a1535' : '#161616',
                  border:'1px solid',
                  borderColor: activeDoc?.name === doc.name ? '#6c47ff33' : '#1e1e1e',
                  cursor:'pointer'
                }}
              >
                <span style={{fontSize:'14px', flexShrink:0}}>📄</span>
                <span style={{fontSize:'11px', color:'#ddd', flex:1, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap'}}>
                  {doc.name}
                </span>
                {activeDoc?.name === doc.name && (
                  <span style={{fontSize:'9px', padding:'2px 7px', borderRadius:'99px', background:'#6c47ff22', color:'#9b7cff', border:'1px solid #6c47ff44', flexShrink:0}}>
                    Active
                  </span>
                )}
              </div>
            ))}
          </div>
        </>
      )}

      {/* Stats */}
      <div style={{marginTop:'auto', display:'grid', gridTemplateColumns:'1fr 1fr', gap:'8px'}}>
        <div style={{background:'#161616', border:'1px solid #1e1e1e', borderRadius:'8px', padding:'10px'}}>
          <div style={{fontSize:'18px', fontWeight:'600', color:'#fff', marginBottom:'2px'}}>{questionCount}</div>
          <div style={{fontSize:'10px', color:'#555'}}>Questions asked</div>
        </div>
        <div style={{background:'#161616', border:'1px solid #1e1e1e', borderRadius:'8px', padding:'10px'}}>
          <div style={{fontSize:'18px', fontWeight:'600', color:'#fff', marginBottom:'2px'}}>{docs.length}</div>
          <div style={{fontSize:'10px', color:'#555'}}>Docs uploaded</div>
        </div>
      </div>
    </div>
  );
}