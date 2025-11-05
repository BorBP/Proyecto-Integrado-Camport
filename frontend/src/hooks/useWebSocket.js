import { useState, useEffect, useCallback } from 'react';
import ReconnectingWebSocket from 'reconnecting-websocket';

const useWebSocket = (url) => {
  const [socket, setSocket] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);

  useEffect(() => {
    const ws = new ReconnectingWebSocket(url);

    ws.addEventListener('open', () => {
      console.log('WebSocket conectado');
      setIsConnected(true);
    });

    ws.addEventListener('close', () => {
      console.log('WebSocket desconectado');
      setIsConnected(false);
    });

    ws.addEventListener('message', (event) => {
      try {
        const data = JSON.parse(event.data);
        setLastMessage(data);
      } catch (error) {
        console.error('Error parsing message:', error);
      }
    });

    ws.addEventListener('error', (error) => {
      console.error('WebSocket error:', error);
    });

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, [url]);

  const sendMessage = useCallback((data) => {
    if (socket && isConnected) {
      socket.send(JSON.stringify(data));
    }
  }, [socket, isConnected]);

  return { isConnected, lastMessage, sendMessage };
};

export default useWebSocket;
