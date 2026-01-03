import { render, screen, fireEvent } from "@testing-library/react";
import { SignupForm } from "./signup-form";
import { beforeEach, describe, expect, test, vi } from "vitest";
import { useSignup } from "@/features/auth/hooks/use-signup";

// Mock کردن هوک
vi.mock("@/features/auth/hooks/use-signup");

describe("SignupForm Integration", () => {
  const mockMutate = vi.fn();

  beforeEach(() => {
    (useSignup as any).mockReturnValue({
      mutate: mockMutate,
      isPending: false,
    });
  });

  test("should submit form with correct data", () => {
    render(<SignupForm />);

    fireEvent.change(screen.getByPlaceholderText(/john doe/i), {
      target: { value: "John doe" },
    });
    fireEvent.change(screen.getByPlaceholderText(/name@example.com/i), {
      target: { value: "john@doe.com" },
    });
    fireEvent.change(screen.getByPlaceholderText(/••••••••/i), {
      target: { value: "123456" },
    });

    fireEvent.click(screen.getByRole("button", { name: /sign up/i }));

    expect(mockMutate).toHaveBeenCalledWith({
      name: "John doe",
      email: "john@doe.com",
      password: "123456",
    });
  });

  test("should disable button and show loading state when isPending is true", () => {
    (useSignup as any).mockReturnValue({
      mutate: mockMutate,
      isPending: true,
    });

    render(<SignupForm />);

    const button = screen.getByRole("button");
    expect(button).toBeDisabled();
    expect(screen.getByText(/signing up/i)).toBeInTheDocument();
  });
});
