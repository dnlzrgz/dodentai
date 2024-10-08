"use client";

export default function Home() {
  async function fetchAPITokens() {
    const response = await fetch("http://127.0.0.1:8000/api/profile/daniel");
    const data = await response.json();
    console.log(data);
  }

  async function handleClick() {
    await fetchAPITokens();
  }

  return <button onClick={handleClick}>Click me</button>;
}
