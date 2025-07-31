"use client";
import { useEffect, useState } from "react";

type NewsItem = {
  title: string,
  news: string
};

export default function GenreNews({ genre }: { genre: string }) {
  const [newsArray, setNewsArray] = useState<NewsItem[]>([]);
  const [error, setError] = useState("");

  const fetchNewsSummary = async () => {
    try {
      const res = await fetch("http://localhost:8080/run_graph", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ mode: "update", genre }),
      });
      const data = await res.json();

      if (Array.isArray(data.response)) {
        setNewsArray(data.response);
        setError("");
      } else {
        setError("Response was not in the expected array format.");
        setNewsArray([]);
      }
    } catch (err) {
      setError("Error fetching update.");
      setNewsArray([]);
    }
  };

  useEffect(() => {
    fetchNewsSummary();
    const interval = setInterval(fetchNewsSummary, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, [genre]);

  return (
    <main className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">📰 {genre.toUpperCase()} News</h1>

      {error && (
        <div className="bg-red-100 text-red-800 p-4 rounded mb-4">{error}</div>
      )}

      {newsArray.length === 0 && !error && (
        <div className="text-gray-500">Loading news...</div>
      )}

      <div className="grid gap-4">
        {newsArray.map((item, idx) => (
          <div key={idx} className="bg-white shadow-md p-4 rounded border">
            <h2 className="font-semibold text-lg text-blue-700 mb-2">
              {item.title}
            </h2>
            <p className="text-gray-800 whitespace-pre-wrap">{item.news}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
