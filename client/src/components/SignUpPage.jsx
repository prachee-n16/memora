import { SignUp } from "@clerk/clerk-react";

export default function SignUpPage() {
  return (
    <div
      className="auth-root"
      style={{
        backgroundImage: `url(${process.env.PUBLIC_URL}/background.jpg)`, // Replace with your image name
        backgroundSize: "cover",
        backgroundPosition: "center",
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <SignUp />
    </div>
  );
}