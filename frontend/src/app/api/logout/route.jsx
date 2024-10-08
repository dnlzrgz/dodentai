import { removeToken } from "@/app/lib/auth";
import { NextResponse } from "next/server";

export async function POST(request) {
  removeToken("auth-token");
  removeToken("auth-refresh-token");
  return NextResponse.json({}, { status: 200 });
}
