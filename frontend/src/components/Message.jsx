import React from 'react';
import { User, ShieldCheck } from 'lucide-react';

function Message({ message }) {
    const isUser = message.role === 'user';

    return (
        <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`flex-shrink-0 h-8 w-8 rounded-lg flex items-center justify-center ${isUser ? 'bg-blue-600 ml-3' : 'bg-purple-600 mr-3'}`}>
                    {isUser ? <User size={16} /> : <ShieldCheck size={16} />}
                </div>
                <div className={`p-4 rounded-2xl shadow-2xl ${isUser ? 'bg-blue-700 text-white rounded-tr-none' : 'bg-gray-800 text-gray-200 rounded-tl-none border border-gray-700'}`}>
                    <p className="text-sm leading-relaxed">{message.content}</p>
                    
                    {message.image_url && (
                        <div className="mt-4 rounded-xl overflow-hidden border border-gray-700 bg-white">
                            <img 
                                src={`http://127.0.0.1:8000/${message.image_url}`} 
                                alt="AI Visualization" 
                                className="w-full h-auto"
                            />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Message;