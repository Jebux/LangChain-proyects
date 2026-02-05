# AI Agentic System Frontend 🤖

Frontend interface for an AI Agentic System built with Next.js, React, and Tailwind CSS. This application serves as a chat interface that connects to a backend API to provide streaming AI responses and file upload capabilities.

## 🚀 Features

-   **Streaming Chat**: Real-time character-by-character responses (Server-Sent Events / Chunked Streaming).
-   **File Upload**: Support for uploading documents for RAG (Retrieval-Augmented Generation) context.
-   **Session Management**: Auto-generated unique session IDs for continuous conversations.
-   **Responsive Design**: Modern, dark-themed UI built with Tailwind CSS.
-   **Echo Filtering**: Intelligent handling of backend responses to ensure clean chat history without duplicated user queries.

## 🛠️ Tech Stack

-   **Framework**: [Next.js 16](https://nextjs.org/) (App Router)
-   **Language**: TypeScript
-   **Styling**: Tailwind CSS
-   **Icons**: Lucide React
-   **State Management**: React Hooks (useState, useEffect, useRef)

## 📂 Project Structure

```bash
src/
├── app/
│   ├── layout.tsx      # Root layout
│   └── page.tsx        # Main chat page
├── components/
│   ├── ChatContainer.tsx  # Main chat logic wrapper
│   ├── MessageList.tsx    # Scrollable list of messages
│   ├── MessageBubble.tsx  # Individual message UI component
│   └── InputArea.tsx      # Text input and file upload controls
├── hooks/
│   └── useChat.ts      # Core logic hook (streaming, upload, state)
└── lib/
    └── utils.ts        # Helper functions (cn class merger)
```

## ⚙️ Configuration & Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd api-agentic-sistem-test1-front
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Environment Variables**:
    Create a `.env.local` file in the root directory:
    ```env
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```

4.  **Run Development Server**:
    ```bash
    npm run dev
    ```

    Open [http://localhost:3000](http://localhost:3000) to view the application.

## 🧠 Key Logic Explanation

### `useChat` Hook
The heart of the application is the `useChat` custom hook (`src/hooks/useChat.ts`). It handles:

-   **Streaming**: It expects a JSON stream from the backend `POST /chat/stream`.
    -   It parses chunks looking for `{ "chunk": "..." }`.
    -   It also handles final full responses `{ "full_response": "..." }`.
    -   *Logic included to stripping user message echoes if the backend reflects the query.*
-   **File Uploading**: Sends files to `POST /upload`.
-   **Session Persistence**: Stores a `chat_session_id` in `localStorage` to maintain context across reloads.

### Backend Requirements
The frontend expects a backend running at `NEXT_PUBLIC_API_URL` with:
-   `POST /chat/stream`: Accepts `{ message, session_id }`, returns a stream or SSE.
-   `POST /upload`: Accepts `multipart/form-data` with a `file` field.

## 🎨 Customization

You can customize the look and feel by editing:
-   `src/app/globals.css`: Global styles and Tailwind base settings.
-   `tailwind.config.ts`: Theme colors and extension.
