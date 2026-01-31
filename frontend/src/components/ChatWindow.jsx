import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, BrainCircuit } from 'lucide-react';
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
        <div className="flex-1 flex flex-col h-full bg-gray-900 overflow-hidden">
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-gray-700 opacity-20">
                        <BrainCircuit size={80} />
                        <p className="text-sm font-bold uppercase tracking-widest mt-4">System Idle</p>
                    </div>
                )}
                {messages.map((msg, idx) => <Message key={idx} message={msg} />)}
                {isLoading && (
                    <div className="flex items-center gap-3 text-blue-400 p-4 bg-blue-500/5 rounded-2xl w-fit border border-blue-500/10 animate-pulse">
                        <Loader2 className="animate-spin" size={16} />
                        <span className="text-xs font-bold uppercase">Processing...</span>
                    </div>
                )}
                <div ref={scrollRef} />
            </div>

            <div className="p-6 bg-gray-900/80 backdrop-blur-md">
                <form onSubmit={handleSubmit} className="max-w-4xl mx-auto flex items-center bg-gray-800 rounded-2xl border border-gray-700 focus-within:border-blue-500/50 transition-all p-1">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about your docs, YouTube videos, or search the web..."
                        className="flex-1 bg-transparent border-none focus:ring-0 px-4 py-3 text-sm placeholder:text-gray-600"
                    />
                    <button type="submit" disabled={!input.trim() || isLoading} className="p-3 bg-blue-600 hover:bg-blue-500 disabled:opacity-20 text-white rounded-xl transition shadow-lg shadow-blue-500/20">
                        <Send size={18} />
                    </button>
                </form>
            </div>
        </div>
    );
}

export default ChatWindow;