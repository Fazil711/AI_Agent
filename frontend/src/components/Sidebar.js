import React from 'react';
import { uploadFiles, clearHistory } from '../services/api';
import { Settings, PlusCircle, Trash2 } from 'lucide-react';

function Sidebar({ model, setModel, setMessages }) {
    const handleFileUpload = async (e) => {
        const files = Array.from(e.target.files);
        if (files.length === 0) return;
        
        try {
            alert("Digesting documents...");
            await uploadFiles(files);
            alert("Brain Updated!");
        } catch (err) {
            alert("Failed to upload files.");
        }
    };

    const handleReset = async () => {
        if (window.confirm("Perform lobotomy? All memory will be cleared.")) {
            await clearHistory();
            setMessages([]);
        }
    };

    return (
        <aside className="w-80 h-full bg-gray-800/50 p-6 flex flex-col border-r border-gray-700 flex-shrink-0 overflow-y-auto">
            <div className="flex items-center gap-2 mb-8 text-blue-400">
                <Settings size={20} />
                <h2 className="uppercase text-[10px] font-bold tracking-[0.2em]">Brain Settings</h2>
            </div>

            <div className="space-y-3 mb-10">
                {['Google Gemini', 'OpenAI GPT-4o'].map(m => (
                    <label key={m} className={`flex items-center space-x-3 p-3 rounded-xl cursor-pointer transition-all border ${model === m ? 'bg-blue-600/10 border-blue-500/50 text-white' : 'bg-transparent border-transparent text-gray-400 hover:bg-gray-700/50'}`}>
                        <input 
                            type="radio" 
                            name="model" 
                            checked={model === m} 
                            onChange={() => setModel(m)}
                            className="hidden" 
                        />
                        <div className={`w-4 h-4 rounded-full border-2 ${model === m ? 'border-blue-400 bg-blue-400' : 'border-gray-500'}`} />
                        <span className="text-sm font-medium">{m}</span>
                    </label>
                ))}
            </div>

            <div className="mb-8">
                <div className="flex items-center gap-2 mb-4 text-green-400">
                    <PlusCircle size={20} />
                    <h2 className="uppercase text-[10px] font-bold tracking-[0.2em]">Feed the Brain</h2>
                </div>
                <div className="relative group">
                    <input 
                        type="file" 
                        multiple 
                        onChange={handleFileUpload}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                    />
                    <div className="p-4 border-2 border-dashed border-gray-600 rounded-xl text-center group-hover:border-blue-500 transition">
                        <p className="text-xs text-gray-400">Upload PDF, CSV, or TXT</p>
                    </div>
                </div>
            </div>

            <button 
                onClick={handleReset}
                className="mt-auto flex items-center justify-center gap-2 w-full py-3 bg-red-600/10 text-red-400 border border-red-600/30 rounded-xl hover:bg-red-600 hover:text-white transition-all group"
            >
                <Trash2 size={18} className="group-hover:animate-pulse" />
                <span className="text-sm font-bold uppercase tracking-tight">Clear Brain</span>
            </button>
        </aside>
    );
}

export default Sidebar;