"use client";

import { useState } from 'react';
import MessageList from './MessageList';
import InputArea from './InputArea';
import { useChat } from '@/hooks/useChat'; // We will create this next
import { Upload } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function ChatContainer() {
    // We'll replace this with the real hook soon
    const {
        messages,
        sendMessage,
        uploadFile,
        isStreaming,
        streamingContent,
        isLoading
    } = useChat();

    return (
        <div className="flex flex-col h-full w-full bg-neutral-900">
            {/* Header (Optional, clean look might just be content) */}
            <header className="p-4 border-b border-neutral-800 flex items-center justify-between bg-neutral-900/50 backdrop-blur-md sticky top-0 z-10">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse" />
                    <span className="font-semibold text-neutral-200">AI Agent</span>
                </div>
                <div className="text-xs text-neutral-500">
                    Session Active
                </div>
            </header>

            <MessageList
                messages={messages}
                isStreaming={isStreaming}
                streamingContent={streamingContent}
                isLoading={isLoading}
            />

            <div className="p-4 bg-neutral-900 border-t border-neutral-800">
                <InputArea
                    onSend={sendMessage}
                    onUpload={uploadFile}
                    isLoading={isLoading || isStreaming}
                />
            </div>
        </div>
    );
}
