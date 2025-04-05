import { defineConfig } from "drizzle-kit";

export default defineConfig({
  dialect: "postgresql",
  schema: "./configs/schema.js",
  dbCredentials: {
    url: "postgresql://neondb_owner:npg_ewdHv82qxRBo@ep-tiny-boat-a11gtlie-pooler.ap-southeast-1.aws.neon.tech/AI-Study-Material-Gen?sslmode=require",
  },
});
