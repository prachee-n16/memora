import React from "react";
import { Outlet } from "react-router-dom";
import { ClerkProvider } from "@clerk/clerk-react";

import Navbar from "../components/Navbar";
const Dashboard = () => {
  const PUBLISHABLE_KEY = process.env.REACT_APP_VITE_CLERK_PUBLISHABLE_KEY;

  if (!PUBLISHABLE_KEY) {
    throw new Error("Missing Publishable Key");
  }

  return (
    <ClerkProvider
      publishableKey={PUBLISHABLE_KEY}
      signInFallbackRedirectUrl="/dashboard"
    >
      <Navbar />
      <main>
        <Outlet />
      </main>
    </ClerkProvider>
  );
};

export default Dashboard;
