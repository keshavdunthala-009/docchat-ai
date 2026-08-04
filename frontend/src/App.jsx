import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Chat } from './components/Chat';

function App() {
  const [activeDoc, setActiveDoc] = useState(null);
  const [docs, setDocs] = useState([]);
  const [questionCount, setQuestionCount] = useState(0);

  return (
    <div style={{display:'grid', gridTemplateColumns:'260px 1fr', height:'100vh', fontFamily:'Segoe UI, sans-serif', background:'#0d0d0d'}}>
      <Sidebar 
        docs={docs} 
        activeDoc={activeDoc} 
        questionCount={questionCount}
        onUpload={(doc) => { setDocs([...docs, doc]); setActiveDoc(doc); }} 
        onSelect={setActiveDoc}
      />
      <Chat 
        activeDoc={activeDoc}
        onQuestion={() => setQuestionCount(prev => prev + 1)}
      />
    </div>
  );
}

export default App;