import React, { useState, useEffect, useRef } from "react";
import { askAI } from "./api";
import "./App.css";
import { useNavigate } from "react-router-dom";
import MarketInsights from "./MarketInsights";
import axios from "axios";

function Agent() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]); // ✅ Store full chat history
  const chatContainerRef = useRef(null); // ✅ For auto-scrolling
  const navigate = useNavigate();
  const [listings, setListings] = useState([]);

  const handleAskAI = async () => {
    if (!query.trim()) return;
    const aiResponse = await askAI(query);
    setMessages([{ user: query, bot: aiResponse }, ...messages]); // ✅ Latest message at top
    setQuery("");
  };

  // ✅ Auto-scroll effect for smooth experience
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = 0;
    }
  }, [messages]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/market/listings").then(res => {
      setListings(res.data.listings);
    });
  }, []);

  return (
    <div className="agent-main-layout">
      {/* Left: Chat Agent */}
      <div className="agent-left">
        <button className="back-btn" onClick={() => navigate("/")}>← Back to Home</button>
        <header className="hero agent-hero">
          <h1>💡 AI Real Estate Advisor</h1>
          <p>Get insights on home prices, investment trends, and property listings.</p>
        </header>
        <section className="query-box agent-query-box">
          <h2>Ask AI About Real Estate in the San Francisco Bay Area</h2>
          <div className="query-row">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask AI about home prices..."
              className="agent-input"
            />
            <button className="agent-search-btn" onClick={handleAskAI}>Search</button>
          </div>
        </section>
        <div className="response-box agent-response-box">
          {messages.map((msg, index) => {
            let images = [];
            let formattedBotText = "";
            let isListings = false;

            if (typeof msg.bot === "string") {
              const imageRegex = /(https?:\/\/.+?\.(?:png|jpg|jpeg|gif|webp))/gi;
              images = msg.bot.match(imageRegex) || [];
              const botText = msg.bot.replace(imageRegex, '').trim();
              formattedBotText = botText.replace(/(\$?\d{1,3}(,\d{3})*(\.\d+)?%?)/g, '<span class="highlight-number">$1</span>');
            } else if (msg.bot && msg.bot.listings) {
              isListings = true;
            }

            return (
              <div key={index} className="message-card agent-message-card">
                <div className="message-content">
                  <div className="message-text">
                    <p className="user-msg">YOU: {msg.user}</p>
                    {isListings ? (
                      <div>
                        <b>Listings:</b>
                        <ul>
                          {msg.bot.listings.map((listing, i) => (
                            <li key={i}>
                              {listing.address} — {listing.price} ({listing.beds}bd/{listing.baths}ba)
                            </li>
                          ))}
                        </ul>
                      </div>
                    ) : (
                      <p className="bot-msg" dangerouslySetInnerHTML={{ __html: `AI: ${formattedBotText}` }} />
                    )}
                  </div>
                  {!isListings && images.length > 0 && (
                    <div className="message-images">
                      {images.map((url, i) => (
                        <img key={i} src={url} alt="AI visual" className="response-image" />
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
      {/* Right: Market Insights */}
      <div className="agent-right">
        <MarketInsights listings={listings} />
      </div>
    </div>
  );
}

export default Agent; 