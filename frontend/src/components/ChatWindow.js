import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Sparkles } from 'lucide-react';
import Message from './Message';

function ChatWindow({ messages, onSend, isLoading }) {
    const [input, setInput] = useState('');
    const scrollRef = useRef(null);

    useEffect(() => {
        scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isLoading]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim() && !isLoading) {
            onSend(input);
            setInput('');
        }
    };

    return (
        <div className="flex-1 flex flex-col h-full overflow-hidden bg-gray-900">
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-gray-600 space-y-4">
                        <Sparkles size={48} className="text-gray-700" />
                        <p className="text-sm uppercase tracking-widest font-bold">Brain Standby</p>
                    </div>
                )}
                {messages.map((msg, idx) => (
                    <Message key={idx} message={msg} />
                ))}
                {isLoading && (
                    <div className="flex items-center space-x-3 text-blue-400 text-sm p-4 bg-blue-600/5 rounded-2xl w-fit border border-blue-500/20">
                        <Loader2 className="animate-spin" size={16} />
                        <span className="font-medium">Synthesizing response...</span>
                    </div>
                )}
                <div ref={scrollRef} />
            </div>

            <div className="p-6 border-t border-gray-800 bg-gray-900">
                <form onSubmit={handleSubmit} className="max-w-4xl mx-auto flex items-center bg-gray-800 rounded-2xl border border-gray-700 focus-within:border-blue-500/50 focus-within:ring-4 focus-within:ring-blue-500/10 transition-all p-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask anything (YouTube URL, CSV question, or Document query)..."
                        className="flex-1 bg-transparent border-none focus:ring-0 px-4 py-2 text-sm"
                    />
                    <button 
                        type="submit" 
                        disabled={!input.trim() || isLoading}
                        className="p-3 bg-blue-600 hover:bg-blue-500 disabled:opacity-30 disabled:grayscale text-white rounded-xl transition shadow-lg shadow-blue-500/20"
                    >
                        <Send size={18} />
                    </button>
                </form>
            </div>
        </div>
    );
}

export default ChatWindow;