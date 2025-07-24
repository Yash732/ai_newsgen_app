"use client";
import { useState } from "react";

export default function ChatPage() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleQuery = async () => {
    setResponse("Loading...");
    try {
      const res = await fetch("http://localhost:8080/run_graph", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ mode: "query", user_input: query }),
      });
      const data = await res.json();
      setResponse(data.response || "No response returned.");
    } catch (error) {
      setResponse("Error sending query.");
    }
  };

  return (
    <main className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-semibold mb-4">🔍 Ask the AI Agent</h1>
      <textarea
        className="w-full border p-3 rounded mb-3 text-gray-400"
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

      <div className="mt-6 whitespace-pre-wrap text-gray-400">{response}</div>
    </main>
  );
}
