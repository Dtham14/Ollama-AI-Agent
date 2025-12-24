import { ChatContainer } from './components/chat/ChatContainer';
import { SessionSidebar } from './components/sessions/SessionSidebar';

function App() {
  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">
      <SessionSidebar />
      <div className="flex-1 relative">
        <ChatContainer />
      </div>
    </div>
  );
}

export default App;
