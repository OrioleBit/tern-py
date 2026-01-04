import { SigninPayload, SigninResponse } from "../types";


export const signin = async (data: SigninPayload): Promise<SigninResponse> => {
    const response = await fetch("http://localhost:8000/users/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to sign in");
    }
    return response.json()
}