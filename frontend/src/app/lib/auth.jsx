import { cookies } from "next/headers";

export function getToken(tokenName) {
  const authToken = cookies().get(tokenName);
  return authToken?.value;
}

export function setToken(tokenName, token, max_age = 3600) {
  cookies().set({
    name: tokenName,
    value: token,
    httpOnly: true, // limit client-side js access
    sameSite: "strict",
    secure: process.env.NODE_ENV != "development",
    maxAge: max_age,
  });
}

export function removeToken(tokenName) {
  cookies().delete(tokenName);
}
