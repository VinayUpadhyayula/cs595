'use Client';
import Image from "next/image";
import { useState } from "react";


export default function Home() {
  const [text, setTweetText] = useState('');
  async function sendTweetData()
  {
    
  }
  const handleTweetChange = (event:any) =>{
    setTweetText(event.target.value);
  }
  return (
    <div className="flex min-h-screen bg-gradient-to-r from-slate-400 via-slate-600 to-slate-800 items-center justify-center">
  <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-md text-center">
    <h1 className="text-3xl font-semibold text-gray-800 mb-6">
      Twitter (X) Sentiment Analyzer
    </h1>
    <div className="flex flex-col space-y-4">
      <span className="text-gray-600">Enter or paste a tweet:</span>
      <textarea 
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
          rows = '4'
          placeholder="Type your tweet here..."
          onChange={handleTweetChange}
        ></textarea>
      <button 
        className="px-4 py-2 bg-blue-500 text-white font-semibold rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        onClick={sendTweetData}
      >
        Predict
      </button>
    </div>
  </div>
</div>
  );
}
