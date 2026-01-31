import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import { getHistory, chatWithAgent } from './services/api';

function App() {
    const [messages, setMessages] = useState([]);
    const [model, setModel] = useState('Google Gemini');
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        getHistory().then(res => setMessages(res.data)).catch(err => console.error("History Load Error:", err));
    }, []);

    const handleSendMessage = async (text) => {
        const userMsg = { role: 'user', content: text };
        setMessages(prev => [...prev, userMsg]);
        setIsLoading(true);

        try {
            const res = await chatWithAgent(text, model);
            const aiMsg = { 
                role: 'assistant', 
                content: res.data.response,
                image_url: res.data.image_path // Support for visualizations
            };
            setMessages(prev => [...prev, aiMsg]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: "Error: Could not reach the brain. Is the backend running?" }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex h-screen w-full bg-gray-900 text-white overflow-hidden">
            {/* Sidebar remains fixed on the left */}
            <Sidebar 
                model={model} 
                setModel={setModel} 
                setMessages={setMessages} 
            />
            
            {/* Main Content Area */}
            <main className="flex-1 flex flex-col min-w-0 bg-gray-900 border-l border-gray-800">
                <header className="p-4 border-b border-gray-800 flex justify-between items-center bg-gray-900/50 backdrop-blur-md">
                    <h1 className="text-xl font-bold flex items-center gap-2">
                        <span className="text-2xl">🧠</span> AI Knowledge Agent
                    </h1>
                    <div className="flex items-center gap-3">
                        <span className="text-[10px] bg-blue-600/20 text-blue-400 border border-blue-600/50 px-3 py-1 rounded-full uppercase tracking-widest font-bold">
                            {model} Active
                        </span>
                    </div>
                </header>

                <ChatWindow 
                    messages={messages} 
                    onSend={handleSendMessage} 
                    isLoading={isLoading} 
                />
            </main>
        </div>
    );
}

export default App;