// src/app/page.tsx (Update flow - live news summaries)
"use client";
import { useEffect, useState } from "react";

export default function HomePage() {
  const [summary, setSummary] = useState("");

  const fetchNewsSummary = async () => {
    try {
      const res = await fetch("http://localhost:8080/run_graph", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ mode: "update" }),
      });
      const data = await res.json();
      setSummary(data.response || "No update received.");
    } catch (error) {
      setSummary("Error fetching update.");
    }
  };

  useEffect(() => {
    fetchNewsSummary();
    const interval = setInterval(fetchNewsSummary, 5 * 60 * 1000); // every 5 min
    return () => clearInterval(interval);
  }, []);

  return (
    <main className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">📰 AI News Summary (Live)</h1>
      <pre className="bg-gray-100 p-4 rounded whitespace-pre-wrap text-gray-800">
        {summary}
      </pre>
    </main>
  );
}
