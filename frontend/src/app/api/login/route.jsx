"use server";
import { getToken, setToken } from "@/app/lib/auth";
import { NextResponse } from "next/server";

const DJANO_API_LOGIN_URL = "http://127.0.0.1:8000/api/token/pair";

export async function POST(request) {
  const requestData = await request.json();
  const response = await fetch(DJANO_API_LOGIN_URL, {
    method: "POST",
    body: JSON.stringify(requestData),
  });

  if (response.ok) {
    const responseData = await response.json();
    const { access, refresh } = responseData;
    setToken("auth-token", access);
    setToken("auth-refresh-token", refresh);

    return NextResponse.json({}, { status: 200 });
  }

  return NextResponse.json({}, { status: 400 });
}
