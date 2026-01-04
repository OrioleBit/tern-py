import { renderHook, waitFor } from "@testing-library/react";
import { useSignin } from "./use-signin";
import { signin } from "@/features/auth/api/signin";
import { useRouter } from "next/navigation";
import { describe, expect, test, vi, beforeEach } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// Mocks
vi.mock("@/features/auth/api/signin");
vi.mock("next/navigation");

describe("useSignin Hook", () => {
  // Fresh QueryClient for each test
  const createWrapper = () => {
    const queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false },
      },
    });

    return ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    );
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("should redirect to root (/) on successful signin", async () => {
    const pushMock = vi.fn();
    (useRouter as any).mockReturnValue({ push: pushMock });

    // Mocking successful login response (e.g., returning a token or user object)
    (signin as any).mockResolvedValue({
      token: "fake-jwt-token",
      user: { id: 1 },
    });

    const { result } = renderHook(() => useSignin(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({
      email: "user@example.com",
      password: "password123",
    });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
      expect(pushMock).toHaveBeenCalledWith("/");
    });
  });

  test("should NOT redirect if signin API fails", async () => {
    const pushMock = vi.fn();
    (useRouter as any).mockReturnValue({ push: pushMock });

    // Mocking an invalid credentials error
    (signin as any).mockRejectedValue(new Error("Invalid email or password"));

    const { result } = renderHook(() => useSignin(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({
      email: "wrong@example.com",
      password: "wrong password",
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    // Ensure user stays on the login page
    expect(pushMock).not.toHaveBeenCalled();
  });
});
