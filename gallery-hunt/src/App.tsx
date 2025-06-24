import { useState, useEffect, useRef } from 'react'
import './App.css'

interface QuizResponse {
  question: string;
  artwork_info: string;
  session_id: string;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [sessionId, setSessionId] = useState<string>('');
  const [currentQuiz, setCurrentQuiz] = useState<string>('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isGeneratingQuiz, setIsGeneratingQuiz] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateQuiz = async () => {
    setIsGeneratingQuiz(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/quiz/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });

      if (!response.ok) {
        throw new Error('クイズの生成に失敗しました');
      }

      const data: QuizResponse = await response.json();
      setSessionId(data.session_id);
      setCurrentQuiz(data.question);
      setMessages([{
        role: 'assistant',
        content: `新しいクイズが始まります！\n\n${data.question}\n\n作品名を当ててください。ヒントが欲しい場合は「ヒント」と入力してください。`,
        timestamp: new Date(),
      }]);
    } catch (error) {
      console.error('Error generating quiz:', error);
      alert('クイズの生成に失敗しました。サーバーが起動しているか確認してください。');
    } finally {
      setIsGeneratingQuiz(false);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !sessionId || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: inputMessage,
        }),
      });

      if (!response.ok) {
        throw new Error('メッセージの送信に失敗しました');
      }

      const data = await response.json();
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'エラーが発生しました。もう一度お試しください。',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const resetChat = () => {
    setSessionId('');
    setCurrentQuiz('');
    setMessages([]);
    setInputMessage('');
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>美術館クイズチャット</h1>
        <p>美術作品を当てるクイズに挑戦しよう！</p>
      </header>

      <main className="app-main">
        {!sessionId ? (
          <div className="welcome-screen">
            <div className="welcome-content">
              <h2>ようこそ！</h2>
              <p>美術館の作品を当てるクイズゲームです。</p>
              <p>クイズを生成して、AIとの対話で正解を目指しましょう！</p>
              <button 
                className="start-button"
                onClick={generateQuiz}
                disabled={isGeneratingQuiz}
              >
                {isGeneratingQuiz ? 'クイズ生成中...' : 'クイズを始める'}
              </button>
            </div>
          </div>
        ) : (
          <div className="chat-container">
            <div className="quiz-info">
              <p><strong>現在のクイズ:</strong> {currentQuiz}</p>
              <button className="reset-button" onClick={resetChat}>
                新しいクイズ
              </button>
            </div>

            <div className="messages-container">
              {messages.map((message, index) => (
                <div 
                  key={index} 
                  className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
                >
                  <div className="message-content">
                    {message.content.split('\n').map((line, lineIndex) => (
                      <div key={lineIndex}>{line}</div>
                    ))}
                  </div>
                  <div className="message-time">
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="message assistant-message loading">
                  <div className="message-content">考え中...</div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="input-container">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="作品名を入力するか、「ヒント」と入力してください..."
                disabled={isLoading}
                className="message-input"
              />
              <button 
                onClick={sendMessage}
                disabled={isLoading || !inputMessage.trim()}
                className="send-button"
              >
                送信
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
