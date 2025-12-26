import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Hello } from "../Hello";

describe("Hello component", () => {
  it("renders greeting with provided name", () => {
    render(<Hello name="Ali" />);

    expect(
      screen.getByRole("heading", { name: "Hello Ali" })
    ).toBeInTheDocument();
  });
});
