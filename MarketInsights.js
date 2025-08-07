import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function MarketInsights() {
  // Placeholder state for future API/scraped data
  const [listings, setListings] = useState([]);
  const [news, setNews] = useState([]);
  const [mortgageRate, setMortgageRate] = useState(null);
  const [appreciation, setAppreciation] = useState(null);
  const [newBuilds, setNewBuilds] = useState(null);
  const [listingLinks, setListingLinks] = useState([]);

  useEffect(() => {
    // Fetch mortgage rate
    axios.get("http://127.0.0.1:8000/market/mortgage").then(res => {
      setMortgageRate(res.data.rate);
    });
    // Fetch appreciation
    axios.get("http://127.0.0.1:8000/market/appreciation").then(res => {
      setAppreciation(res.data.appreciation);
    });
    // Fetch new builds
    axios.get("http://127.0.0.1:8000/market/newbuilds").then(res => {
      setNewBuilds(res.data.new_builds);
    });
    // Fetch news
    axios.get("http://127.0.0.1:8000/market/news").then(res => {
      setNews(res.data.news);
    });
    axios.get("http://127.0.0.1:8000/market/listings").then(res => {
      setListingLinks(res.data.links || []);
    });
    // Listings: optionally fetch from your backend if available
    // setListings([{address: '123 Main St', price: '$1,200,000', beds: 3, baths: 2}]);
  }, []);

  return (
    <div className="market-insights-panel">
      <div className="market-insights-title">Market Insights</div>
      <div className="market-insights-section">
        <b>Mortgage Rate:</b> {mortgageRate || <span style={{color:'#bbb'}}>Loading...</span>}
      </div>
      <div className="market-insights-section">
        <b>Appreciation:</b> {appreciation || <span style={{color:'#bbb'}}>Loading...</span>}
      </div>
      <div className="market-insights-section">
        <b>New Builds:</b> {newBuilds || <span style={{color:'#bbb'}}>Loading...</span>}
      </div>
      <div className="market-insights-section">
        <b>SF Bay Area Listings:</b>
        {listingLinks.length === 0 ? (
          <div style={{color:'#bbb'}}>Loading...</div>
        ) : (
          <ul>
            {listingLinks.map((l, i) => (
              <li key={i}>
                <a href={l.url} target="_blank" rel="noopener noreferrer" className="listing-link">{l.name}</a>
              </li>
            ))}
          </ul>
        )}
      </div>
      <div className="market-insights-section">
        <b>News:</b>
        {news.length === 0 ? (
          <div className="market-insights-news" style={{color:'#bbb'}}>Loading...</div>
        ) : (
          news.map((n, i) => (
            <div className="market-insights-news" key={i}>
              <a href={n.url} target="_blank" rel="noopener noreferrer">{n.title}</a>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default MarketInsights; 