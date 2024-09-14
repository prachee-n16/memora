import { SignIn } from "@clerk/clerk-react";

export default function SignInPage() {
  return (
    <div className="auth-root">
      <SignIn />
    </div>
  );
}
