// Bundles SupplyDemandPlanner.jsx + React + Recharts into one self-contained
// standalone.html you can open in a browser or drop behind /mocks/demand-planner.
//   npm install && npm run build
import * as esbuild from "esbuild";
import fs from "node:fs";

const entry = `
import React from "react";
import { createRoot } from "react-dom/client";
import SupplyDemandPlanner from "./SupplyDemandPlanner.jsx";
createRoot(document.getElementById("root")).render(<SupplyDemandPlanner />);
`;
const r = await esbuild.build({
  stdin: { contents: entry, loader: "jsx", resolveDir: process.cwd() },
  bundle: true, minify: true, write: false, format: "iife", jsx: "automatic", target: ["es2019"],
  define: { "process.env.NODE_ENV": '"production"' }, logLevel: "warning",
});
const js = r.outputFiles[0].text.replace(/<\/script>/g, "<\\/script>");
const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Supply & Demand Planner</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>html,body{margin:0;background:#0A0D13;color-scheme:dark;}</style></head>
<body><div id="root"></div><script>${js}</script></body></html>`;
fs.writeFileSync("standalone.html", html);
console.log("wrote standalone.html", (html.length / 1024).toFixed(0) + " KB");
