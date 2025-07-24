import Link from "next/link";

export default function Nav() {
  return (
    <nav className="bg-gray-800 text-white p-4 flex gap-4">
      <Link href="/" className="hover:underline">Home</Link>
      <Link href="/chat" className="hover:underline">Chat</Link>
    </nav>
  );
}
