"use client";

import { useRouter } from "next/navigation";

export default function LogIn() {
  const router = useRouter();

  async function onSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);
    const formObject = Object.fromEntries(formData);
    const response = await fetch("/api/login/", {
      method: "POST",
      body: JSON.stringify(formObject),
    });

    if (response.ok) {
      router.replace("/");
    }
  }

  return (
    <form onSubmit={onSubmit}>
      <input type="text" name="username" placeholder="Username" required />
      <input type="password" name="password" placeholder="Password" required />
      <input type="submit" name="submit" value="Log In" />
    </form>
  );
}
