import ChatContainer from '@/components/ChatContainer';

export default function Home() {
  return (
    <main className="h-full w-full flex flex-col items-center justify-center p-60">
      <div className="border border-neutral-800 rounded-lg max-w-[400px]">
        <ChatContainer />
      </div>
    </main>
  );
}
