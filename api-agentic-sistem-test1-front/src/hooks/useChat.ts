import { useState, useRef, useEffect } from 'react';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
}

interface UseChatReturn {
    messages: Message[];
    sendMessage: (message: string) => Promise<void>;
    uploadFile: (file: File) => Promise<void>;
    isLoading: boolean;
    isStreaming: boolean;
    streamingContent: string;
    sessionId: string;
}

export function useChat(): UseChatReturn {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isStreaming, setIsStreaming] = useState(false);
    const [streamingContent, setStreamingContent] = useState('');
    const [sessionId, setSessionId] = useState('');

    // Monitor messages state
    useEffect(() => {
        console.log('Current Messages State:', messages);
    }, [messages]);

    // Initialize Session ID on mount
    useEffect(() => {
        const storedSession = localStorage.getItem('chat_session_id');

        if (storedSession) {
            setSessionId(storedSession);
        } else {
            const newSessionId = crypto.randomUUID();
            setSessionId(newSessionId);
            localStorage.setItem('chat_session_id', newSessionId);
        }
    }, []);

    const sendMessage = async (content: string) => {
        console.log('Sending message:', content, 'SessionID:', sessionId);

        const userMessage: Message = {
            id: crypto.randomUUID(),
            role: 'user',
            content,
        };

        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);
        setIsStreaming(true);
        setStreamingContent('');

        try {
            console.log('Initiating fetch to:', `${process.env.NEXT_PUBLIC_API_URL}/chat/stream`);
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat/stream`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: content,
                    session_id: sessionId,
                }),
            });
            console.log('Fetch response status:', response.status);


            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            if (!response.body) {
                throw new Error('Response body is null');
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let accumulatedText = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                // console.log('Received chunk:', chunk);


                // The backend sends Server-Sent Events style or raw chunks?
                // User request says: "Un flujo continuo de datos (Server-Sent Events) donde cada paquete contiene: Un fragmento de texto (chunk)..."
                // But also "Recibe: Un flujo continuo..."
                // Typically custom streaming endpoints might just dump text or be proper SSE.
                // If it's proper SSE ("data: ..."), we need to parse it. 
                // If it's just raw text streaming, we just append.
                // The description says: "word by word... like ChatGPT".
                // Let's assume raw text stream for simplicity or basic SSE parsing if usually standard.
                // Re-reading: "Recibe frontend? ... Un fragmento de texto (chunk), Un indicador de si ya terminó... Al final, la respuesta completa"
                // This suggests a structured JSON stream or custom format.
                // BUT, often with "chunk", people mean raw text.
                // Given "Server-Sent Events", it usually follows format `data: ...\n\n`.
                // Let's implement a basic SSE parser or robust reader.

                // Let's try to parse as SSE if it looks like it, otherwise raw.
                // A common pattern in simple python backends is just `yield text`.
                // IF it is SSE, lines start with 'data: '.
                // Let's assume the backend might just send raw text chunks for simplicity in this demo unless 'Server-Sent Events' was strict strict.
                // "Un flujo continuo de datos (Server-Sent Events)" -> Valid SSE.
                // Let's handle SSE.

                const lines = chunk.split('\n');
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') continue; // Common convention
                        try {
                            // Try to parse if it's JSON, otherwise treat as text
                            const parsed = JSON.parse(data);

                            // Handle backend specific keys
                            if (parsed.chunk) {
                                accumulatedText += parsed.chunk;
                                setStreamingContent(prev => prev + parsed.chunk);
                            } else if (parsed.content) {
                                accumulatedText += parsed.content;
                                setStreamingContent(prev => prev + parsed.content);
                            }

                            // Always trust full_response if provided at the end
                            if (parsed.full_response) {
                                accumulatedText = parsed.full_response;
                            }
                        } catch (e) {
                            // Not JSON, maybe just text
                            accumulatedText += data;
                            setStreamingContent(prev => prev + data);
                        }
                    } else if (line.trim() !== '') {
                        // Fallback for non-SSE or raw stream
                        // If the backend isn't strictly SSE formatted but just streaming text
                        // We might just append 'chunk' directly if it doesn't look like SSE at all.
                        // But wait, the user said "Server-Sent Events".
                        // I will try to support both roughly.
                        // If raw chunk doesn't contain "data:", treat as raw text?
                        // Or maybe the prompt meant "conceptually like SSE".
                        // Let's assume standard behavior: if it contains "data:", parse it. else append raw.
                        if (!chunk.includes('data:')) {
                            console.log('Processing as raw chunk:', chunk);
                            accumulatedText += chunk;

                            setStreamingContent(prev => prev + chunk);
                            break; // moved pointer
                        }
                    }
                }
            }

            // Finalize message - ensure we strip the echo if it exists in the final accumulated text
            let finalContent = accumulatedText;
            if (content && accumulatedText.startsWith(content)) {
                finalContent = accumulatedText.slice(content.length);
            }

            setMessages((prev) => [
                ...prev,
                {
                    id: crypto.randomUUID(),
                    role: 'assistant',
                    content: finalContent,
                },
            ]);
        } catch (error) {
            console.error('Error sending message:', error);
            // Optional: Add error message to chat
            setMessages((prev) => [
                ...prev,
                {
                    id: crypto.randomUUID(),
                    role: 'assistant',
                    content: 'Sorry, I encountered an error. Please try again.',
                },
            ]);
        } finally {
            setIsLoading(false);
            setIsStreaming(false);
            setStreamingContent('');
        }
    };

    const uploadFile = async (file: File) => {
        setIsLoading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/upload`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Upload failed');

            const data = await response.json();

            // Notify user of success (maybe via a system message in chat?)
            setMessages((prev) => [
                ...prev,
                {
                    id: crypto.randomUUID(),
                    role: 'assistant',
                    content: `📄 **File Uploaded**: ${data.filename || file.name}\n${data.message || 'Ready to answer questions about it.'}`
                }
            ]);

        } catch (error) {
            console.error("Upload error", error);
            setMessages((prev) => [
                ...prev,
                {
                    id: crypto.randomUUID(),
                    role: 'assistant',
                    content: `⚠️ Failed to upload ${file.name}. Please try again.`
                }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    return {
        messages,
        sendMessage,
        uploadFile,
        isLoading,
        isStreaming,
        streamingContent,
        sessionId,
    };
}
