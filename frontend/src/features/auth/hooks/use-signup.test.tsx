import { renderHook, waitFor } from "@testing-library/react";
import { useSignup } from "./use-signup";
import { signup } from "@/features/auth/api/signup";
import { useRouter } from "next/navigation";
import { describe, expect, test, vi, beforeEach } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// Mocks
vi.mock("@/features/auth/api/signup");
vi.mock("next/navigation");

describe("useSignup Hook", () => {
  // Function to create a fresh QueryClient for each test to avoid cache pollution
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

  test("should redirect to root (/) on successful signup", async () => {
    const pushMock = vi.fn();
    (useRouter as any).mockReturnValue({ push: pushMock });

    // Mocking a successful API response
    (signup as any).mockResolvedValue({
      id: "user_123",
      email: "test@example.com",
    });

    const { result } = renderHook(() => useSignup(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({
      name: "David",
      email: "david@test.com",
      password: "securePassword123",
    });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
      expect(pushMock).toHaveBeenCalledWith("/");
    });
  });

  test("should NOT redirect if signup API fails", async () => {
    const pushMock = vi.fn();
    (useRouter as any).mockReturnValue({ push: pushMock });

    // Mocking an API failure
    (signup as any).mockRejectedValue(new Error("Internal Server Error"));

    const { result } = renderHook(() => useSignup(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({
      name: "David",
      email: "error@test.com",
      password: "password123",
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    // Ensure router.push was never called
    expect(pushMock).not.toHaveBeenCalled();
  });
});
