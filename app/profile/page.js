// app/profile/page.js — Route: /profile

export const metadata = {
  title: "Profile | Artisan Market",
  description: "Your profile and account settings.",
};

export default function ProfilePage() {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "80vh",
        padding: "48px 32px",
        textAlign: "center",
        gap: "16px",
      }}
    >
      <div
        style={{
          width: "88px",
          height: "88px",
          borderRadius: "50%",
          background: "linear-gradient(135deg, var(--color-accent-light), var(--color-accent))",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          boxShadow: "0 6px 24px rgba(193,98,47,0.28)",
        }}
        aria-hidden="true"
      >
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
          <circle cx="12" cy="7" r="4" />
        </svg>
      </div>
      <h1
        style={{
          fontSize: "1.5rem",
          fontWeight: "800",
          color: "var(--color-text-primary)",
          fontFamily: "var(--font-display)",
        }}
      >
        Profile
      </h1>
    </div>
  );
}
