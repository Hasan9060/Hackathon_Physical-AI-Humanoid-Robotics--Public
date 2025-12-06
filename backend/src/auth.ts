import { betterAuth } from "better-auth";
import express from "express";
import cors from "cors";
import dotenv from "dotenv";

dotenv.config();

export const auth = betterAuth({
  database: {
    provider: "sqlite",
    url: "./auth.db",
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Disable for testing
    minPasswordLength: 8,
    maxPasswordLength: 128,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
  user: {
    additionalFields: {
      name: {
        type: "string",
        required: false,
      },
    },
  },
});

// Start server
const port = process.env.AUTH_PORT || 3001;

const app = express();

app.use(cors({
  origin: "*",
  credentials: true,
}));

app.use(express.json());

app.use("/auth", auth.handler);

app.listen(port, () => {
  console.log(`🔐 Auth server running on http://localhost:${port}`);
});