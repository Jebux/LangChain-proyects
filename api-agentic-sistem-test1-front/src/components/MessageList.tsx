import { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
}

interface MessageListProps {
    messages: Message[];
    isStreaming: boolean;
    streamingContent: string;
    isLoading?: boolean;
}

export default function MessageList({ messages, isStreaming, streamingContent, isLoading }: MessageListProps) {
    const bottomRef = useRef<HTMLDivElement>(null);

    console.log('MessageList Render:', { messageCount: messages.length, isStreaming, isLoading });

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, streamingContent, isStreaming, isLoading]);


    return (
        <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
            <div className="max-w-4xl mx-auto flex flex-col pt-4">
                {messages.map((msg) => (
                    <MessageBubble key={msg.id} role={msg.role} content={msg.content} />
                ))}

                {isStreaming && (
                    <MessageBubble
                        role="assistant"
                        content={streamingContent}
                        isStreaming={true}
                    />
                )}

                {isLoading && !isStreaming && (
                    <div className="flex justify-start w-full mb-6 animate-in fade-in slide-in-from-bottom-2">
                        <div className="flex max-w-[80%] gap-3">
                            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center text-white">
                                <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                            </div>
                            <div className="p-4 rounded-2xl rounded-tl-sm bg-neutral-800 border border-neutral-700 text-neutral-400 text-sm flex items-center gap-2">
                                <span>Thinking...</span>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={bottomRef} className="h-4" />
            </div>
        </div>
    );
}
