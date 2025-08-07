import axios from "axios";

// ✅ Function to communicate with AI Chatbot (Ollama API via FastAPI)
export const askAI = async (query) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/ask?query=${query}`);
    return response.data.response; // AI-generated real estate insights
  } catch (error) {
    console.error("Error fetching AI response:", error);
    return "Something went wrong. Please try again.";
  }
};

// ✅ Function to fetch property listings (Zillow API)
export const getPropertyListings = async (city, priceRange) => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/properties?city=${city}&price=${priceRange}`
    );
    return response.data.listings; // Real estate properties
  } catch (error) {
    console.error("Error fetching property listings:", error);
    return [];
  }
};
