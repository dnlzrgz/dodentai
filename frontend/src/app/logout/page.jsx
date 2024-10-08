"use client";

import { useRouter } from "next/navigation";

export default function LogOut() {
  const router = useRouter();

  async function handleClick(event) {
    event.preventDefault();

    const response = await fetch("/api/logout/", {
      method: "POST",
      body: "",
    });

    if (response.ok) {
      router.replace("/");
    }
  }

  return <button onClick={handleClick}>Log Out</button>;
}
