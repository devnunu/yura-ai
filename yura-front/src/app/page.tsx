"use client";

import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [inputText, setInputText] = useState<string>('');
  const [outputText, setOutputText] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async () => {
    setLoading(true);  // 로딩 시작
    const userInput = inputText;  // 사용자 입력값을 저장
    setInputText('');  // 입력란 초기화
    try {
      const response = await axios.post('http://127.0.0.1:5000/process', { text: userInput });
      const processedText = `${userInput}\n\n---\n\n${response.data.processed_text}`;
      setOutputText(processedText);
    } catch (error) {
      console.error('Error:', error);
      setOutputText('An error occurred. Please try again.');
    } finally {
      setLoading(false);  // 로딩 종료
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-between items-center bg-gray-100 p-6">
      <header className="text-center text-3xl font-semibold text-gray-700 mb-6">
        Yura AI - UX Writer Assistant
      </header>

      {/* 결과값 또는 로딩 인디케이터 */}
      <div className="flex-grow flex items-center justify-center w-full max-w-3xl mb-6">
        {loading ? (
          <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-gray-400"></div>
        ) : (
          <div className="text-lg text-gray-600 whitespace-pre-wrap w-full p-4 bg-white rounded-md shadow">
            <p className="font-bold text-xl">입력값:</p>
            <p className="mb-4">{outputText.split('\n\n---\n\n')[0]}</p>
            <hr className="my-4 border-gray-300"/>
            <p className="font-bold text-xl">출력값:</p>
            <p>{outputText.split('\n\n---\n\n')[1]}</p>
          </div>
        )}
      </div>

      {/* 입력란 및 버튼 */}
      <div className="w-full max-w-3xl flex items-center mb-6">
        <textarea
          className="flex-grow p-4 border border-gray-300 rounded-md text-gray-700 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
          rows={3}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter your text here..."
        />
        <button
          className="ml-4 bg-blue-500 text-white px-6 py-3 rounded-md shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300 transition"
          onClick={handleSubmit}
        >
          Submit
        </button>
      </div>
    </div>
  );
}
