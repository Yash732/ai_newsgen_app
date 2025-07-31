import Link from "next/link";

export default function Nav() {
  return (
    <nav className="bg-gray-800 text-white p-4 flex gap-4">
      <Link href="/" className="hover:underline">Home</Link>
      <Link href="/chat" className="hover:underline">Chat</Link>
      <Link href="/genre/finance" className="hover:underline">Finance</Link>
      <Link href="/genre/sports" className="hover:underline">Sports</Link>
      <Link href="/genre/tech" className="hover:underline">Tech</Link>
      <Link href="/genre/politics" className="hover:underline">Politics</Link>
      <Link href="/genre/gaming" className="hover:underline">Gaming</Link>
    </nav>
  );
}
