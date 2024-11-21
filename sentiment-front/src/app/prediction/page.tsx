"use client";
import { ok } from "assert";
import Image from "next/image";
import { useEffect, useState } from "react";
import config from "../../../../config.json"
enum SentimentEnum {
  Negative = 0,
  Neutral = 1,
  Positive = 2
}
export default function Home() {
  const [text, setTweetText] = useState('');
  const [prediction, setPrediction] = useState('');
  const [showPrediction, setShowPrediction] = useState(false);
  const [enableButton, setButtonStatus] = useState(true);
  useEffect(()=>{
    if(text == '')
    {
      setShowPrediction(false);
      setButtonStatus(true);
    }
    else
    {
      setButtonStatus(false);
    }
  },[text]);
  async function sendTweetData()
  {
    setPrediction('');
    if(text != '')
    {
      const data = {
        text : text
       }
    await fetch(config.apiUrl,{
      method: "POST",
      headers:{
        "Content-Type" : "application/json",
      },
      body : JSON.stringify(data),
    }
    ).then((response) => response.json())
    .then((result)=>
    {
      // console.log(result);
      setShowPrediction(true);
      setPrediction(SentimentEnum[result.prediction])
    })
    .catch((error)=>
    {
      throw new Error("Error predicting  Sentiment of the tweet");
    });
  }
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
          rows = {4}
          placeholder="Type your tweet here..."
          onChange={handleTweetChange}
        ></textarea>
      <button 
        className={`px-4 py-2 font-semibold rounded-md focus:outline-none focus:ring-2 
        ${!enableButton ? "bg-blue-500 hover:bg-blue-600" : "bg-gray-300 text-gray-500 cursor-not-allowed"}`}
        onClick={sendTweetData}
        disabled={enableButton}
      >
        Predict
      </button>
          {showPrediction ? <span className={`px-3 py-1 font-semibold text-white rounded ${
        prediction === "Positive"
          ? "bg-green-500"
          : prediction === "Negative"
          ? "bg-red-500"
          : "bg-yellow-500"
      }`}>Predicted sentiment Class: {prediction}</span> : <></>}
    </div>
  </div>
</div>
  );
}
