"use client";

import { useSignin } from "@/features/auth/hooks/use-signin";

export const SigninForm = () => {
  const { mutate, isPending } = useSignin();

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const data = Object.fromEntries(formData) as any;
    mutate(data);
  };

  const inputStyles = `
    w-full px-5 py-4 rounded-2xl bg-slate-50 border border-slate-200 
    outline-none transition-all duration-200
    placeholder:text-slate-400 text-slate-700
    focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10
  `;

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-5">
      <div className="space-y-1.5">
        <label className="text-sm font-bold text-slate-700 ml-1">
          Email Address
        </label>
        <input
          name="email"
          type="email"
          placeholder="name@example.com"
          required
          className={inputStyles}
        />
      </div>

      <div className="space-y-1.5">
        <label className="text-sm font-bold text-slate-700 ml-1">
          Password
        </label>
        <input
          name="password"
          type="password"
          placeholder="••••••••"
          required
          className={inputStyles}
        />
      </div>

      <button
        type="submit"
        disabled={isPending}
        className="mt-2 w-full bg-slate-900 hover:bg-slate-800 disabled:bg-slate-400 
                   text-white font-bold py-4 rounded-2xl shadow-lg shadow-slate-200 
                   transition-all duration-200 active:scale-[0.98] flex items-center justify-center gap-2"
      >
        {isPending ? (
          <>
            <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            Signing up...
          </>
        ) : (
          "Sign up"
        )}
      </button>
    </form>
  );
};
