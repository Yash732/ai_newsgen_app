"use client";
import { useState } from "react";

type NewsItem = {
  title: string;
  news: string;
};

export default function ChatPage() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<NewsItem[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleQuery = async () => {
    setLoading(true);
    setError("");
    setResponse(null);
    try {
      // for local testing
      // const res = await fetch("http://localhost:8080/run_graph",{
      const res = await fetch("https://fastapi-backend-n2gy.onrender.com/run_graph", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ mode: "query", user_input: query }),
      });
      const data = await res.json();

      // If the response is a valid JSON array
      if (Array.isArray(data.response)) {
        setResponse(data.response);
      } else {
        setError("Unexpected response format.");
      }
    } catch (error) {
      setError("Error sending query.");
    }
    setLoading(false);
  };

  return (
    <main className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-semibold mb-4">🔍 Ask the AI Agent</h1>
      <textarea
        className="w-full border p-3 rounded mb-3 text-gray-700"
        rows={4}
        placeholder="e.g. What’s the latest update on SpaceX or Apple stock?"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        onClick={handleQuery}
      >
        Ask
      </button>

      <div className="mt-6 text-gray-700">
        {loading && <p>Loading...</p>}
        {error && <p className="text-red-500">{error}</p>}

        {response &&
          response.map((item, idx) => (
            <div key={idx} className="bg-white shadow-md rounded p-4 mb-4 border border-gray-200">
              <h2 className="text-lg font-bold mb-2">{item.title || "Untitled"}</h2>
              <p className="text-sm text-gray-600 whitespace-pre-line">{item.news || "No details available."}</p>
            </div>
          ))}
      </div>
    </main>
  );
}
