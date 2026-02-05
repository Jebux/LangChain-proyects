import { cn } from '@/lib/utils';
import ReactMarkdown from 'react-markdown';
import { User, Bot } from 'lucide-react';

interface MessageBubbleProps {
    role: 'user' | 'assistant';
    content: string;
    isStreaming?: boolean;
}

export default function MessageBubble({ role, content, isStreaming }: MessageBubbleProps) {
    const isUser = role === 'user';

    return (
        <div
            className={cn(
                'flex w-full mb-6 animate-in fade-in slide-in-from-bottom-2 duration-300',
                isUser ? 'justify-end' : 'justify-start'
            )}
        >
            <div className={cn('flex max-w-[80%] md:max-w-[70%] gap-3', isUser ? 'flex-row-reverse' : 'flex-row')}>
                {/* Avatar */}
                <div
                    className={cn(
                        'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
                        isUser ? 'bg-blue-600 text-white' : 'bg-emerald-600 text-white'
                    )}
                >
                    {isUser ? <User size={16} /> : <Bot size={16} />}
                </div>

                {/* Bubble */}
                <div
                    className={cn(
                        'p-4 rounded-2xl text-sm leading-relaxed shadow-md',
                        isUser
                            ? 'bg-blue-600 text-white rounded-tr-sm'
                            : 'bg-neutral-800 text-neutral-100 rounded-tl-sm border border-neutral-700'
                    )}
                >
                    <div className="prose prose-invert prose-sm max-w-none break-words">
                        <ReactMarkdown>{content}</ReactMarkdown>
                    </div>
                    {isStreaming && (
                        <span className="inline-block w-2 H-4 ml-1 align-middle bg-emerald-400 animate-pulse" />
                    )}
                </div>
            </div>
        </div>
    );
}
