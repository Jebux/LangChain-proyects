import { useState, useRef, KeyboardEvent } from 'react';
import { Send, Paperclip, X, FileText } from 'lucide-react';
import { cn } from '@/lib/utils';

interface InputAreaProps {
    onSend: (message: string) => void;
    onUpload?: (file: File) => Promise<void>;
    isLoading?: boolean;
    disabled?: boolean;
}

export default function InputArea({ onSend, onUpload, isLoading, disabled }: InputAreaProps) {
    const [input, setInput] = useState('');
    const [file, setFile] = useState<File | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleSend = () => {
        if ((!input.trim() && !file) || isLoading || disabled) return;

        // If there's a file but no text, we can still "send" usually, 
        // but the backend API separates upload and chat. 
        // Usually we upload first, then chat.
        // For this UI, we might handle 'onUpload' when the file is selected or when send is clicked?
        // The prompt says: "Usuario sube un documento usando /upload ... Frontend recibe confirmación ... Usuario hace preguntas"
        // So maybe upload happens immediately upon selection or typically separate action.
        // Let's assume upload happens separately or we trigger it here if present.
        // For simplicity, let's keep it clean: Upload button triggers upload immediately or adds to 'staging' and uploads.
        // Given the API structure (Upload endpoint returns confirmation), let's make upload a separate action or auto-upload on select.
        // Let's implement auto-upload on selection for now or better, stage it and upload on separate triggers if needed.
        // Actually, "Usuario sube un documento usando /upload" implies a distinct action. 
        // But for a chat interface, usually you attach -> send.
        // Let's stick to text sending here. If a file is selected, we might want to upload it first.

        onSend(input);
        setInput('');
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            if (onUpload) {
                await onUpload(selectedFile);
            }
            // Clear input after upload attempt to allow re-selecting same file if needed
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto p-4">
            <div className="relative flex items-end gap-2 bg-neutral-800 p-3 rounded-xl border border-neutral-700 shadow-lg focus-within:ring-2 focus-within:ring-blue-500/50 transition-all">

                <input
                    type="file"
                    ref={fileInputRef}
                    className="hidden"
                    accept=".pdf,.txt"
                    onChange={handleFileSelect}
                />

                <button
                    onClick={() => fileInputRef.current?.click()}
                    disabled={isLoading || disabled}
                    className="p-2 text-neutral-400 hover:text-white transition-colors rounded-lg hover:bg-neutral-700"
                    title="Upload Document"
                >
                    <Paperclip size={20} />
                </button>

                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type a message..."
                    disabled={isLoading || disabled}
                    className="flex-1 bg-transparent text-white placeholder-neutral-500 resize-none max-h-32 min-h-[24px] py-2 focus:outline-none custom-scrollbar"
                    rows={1}
                    style={{ height: 'auto', minHeight: '24px' }}
                // Auto-resize could be added here
                />

                <button
                    onClick={handleSend}
                    disabled={(!input.trim() && !file) || isLoading || disabled}
                    className={cn(
                        "p-2 rounded-lg transition-all duration-200",
                        input.trim() || file
                            ? "bg-blue-600 text-white shadow-blue-500/20 shadow-md hover:bg-blue-500"
                            : "bg-neutral-700 text-neutral-500 cursor-not-allowed"
                    )}
                >
                    <Send size={20} />
                </button>
            </div>
            <div className="text-xs text-neutral-500 mt-2 text-center">
                AI Agent can verify documents and answer questions.
            </div>
        </div>
    );
}
