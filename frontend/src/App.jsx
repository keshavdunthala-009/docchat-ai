import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Chat } from './components/Chat';

function App() {
  const [docs, setDocs] = useState([]);
  const [activeDoc, setActiveDoc] = useState(null);
  const [questionCount, setQuestionCount] = useState(0);

  const handleUpload = (doc) => {
    setDocs((prev) => [...prev, doc]);
    setActiveDoc(doc);
  };

  const handleSelect = (doc) => {
    setActiveDoc(doc);
  };

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'Arial' }}>
      <div style={{ width: '280px', flexShrink: 0 }}>
        <Sidebar
          docs={docs}
          activeDoc={activeDoc}
          questionCount={questionCount}
          onUpload={handleUpload}
          onSelect={handleSelect}
        />
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: '20px' }}>
        <h1>RAG Document Q and A System</h1>
        <p>Upload documents and ask questions with AI-powered retrieval</p>

        {activeDoc ? (
          <Chat
            activeDoc={activeDoc}
            onQuestionAsked={() => setQuestionCount((c) => c + 1)}
          />
        ) : (
          <div style={{ textAlign: 'center', padding: '40px', color: '#999', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
            <p>Upload a document to get started</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;