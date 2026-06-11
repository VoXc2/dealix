export const metadata = {
  title: "Login — Dealix",
  description: "Admin login for the founder operating system.",
};

export default function LoginPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-md px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Admin Login</p>
          <h1 className="mt-3 text-3xl font-semibold">دخول المؤسس</h1>
          <p className="mt-3 text-sm text-white/70">
            Internal access only. Demo mode allows read access without login.
          </p>
        </header>

        <form className="mt-8 space-y-4" action="/api/auth/check" method="POST">
          <div>
            <label htmlFor="token" className="text-xs uppercase tracking-widest text-white/50">
              Admin token
            </label>
            <input
              id="token"
              name="token"
              type="password"
              required
              className="mt-1 w-full rounded-lg border border-white/10 bg-black/30 px-3 py-2 text-sm focus:border-amber-300/50 focus:outline-none"
              placeholder="paste DEALIX_ADMIN_TOKEN"
            />
          </div>
          <button
            type="submit"
            className="w-full rounded-lg border border-amber-300/30 bg-amber-300/10 px-4 py-2 text-sm text-amber-200 hover:border-amber-300/60"
          >
            Sign in
          </button>
        </form>

        <p className="mt-6 text-[10px] text-white/40">
          Production requires HTTPS, secure cookies, and CSRF protection. See docs/auth/PRODUCTION_AUTH_REQUIREMENTS.md.
        </p>
      </div>
    </main>
  );
}
