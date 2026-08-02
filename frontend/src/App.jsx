import { useState } from 'react';
import { Upload } from './components/Upload';
import { Chat } from './components/Chat';

function App() {
  const [documentUploaded, setDocumentUploaded] = useState(false);

  return (
    <div style={{maxWidth: '900px', margin: '0 auto', padding: '20px', fontFamily: 'Arial'}}>
      <h1>RAG Document Q and A System</h1>
      <p>Upload documents and ask questions with AI-powered retrieval</p>
      <Upload onSuccess={() => setDocumentUploaded(true)} />
      {documentUploaded && <Chat />}
      {!documentUploaded && (
        <div style={{textAlign: 'center', padding: '40px', color: '#999', backgroundColor: '#f5f5f5', borderRadius: '8px'}}>
          <p>Upload a document to get started</p>
        </div>
      )}
    </div>
  );
}

export default App;
