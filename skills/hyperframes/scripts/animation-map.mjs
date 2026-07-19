#!/usr/bin/env node
// animation-map.mjs — Grok-ported HyperFrames animation map & choreography auditor
// Original from Codex. Analyzes GSAP timelines registered in window.__timelines,
// produces human-readable summaries, ASCII timeline, stagger/dead-zone detection,
// flags for offscreen/collision/invisible elements.
//
// Requires a full HyperFrames runtime + headless capture (puppeteer or playwright).
// In pure Grok sessions without the browser toolchain, use for reference of the
// expected JSON contract only; the authoring rules in SKILL.md are the primary tool.

import { mkdir, writeFile } from "node:fs/promises";
import { resolve, join } from "node:path";
import { hyperframesPackageSpec, importPackagesOrBootstrap } from "./package-loader.mjs";

const DEFAULTS = {
  frames: 60,
  width: 1920,
  height: 1080,
  fps: 60,
  minDuration: 0.05,
};

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const compDir = resolve(args._[0] || ".");
  const outDir = args.out ? resolve(args.out) : join(compDir, ".hyperframes");

  console.log(`[hyperframes] animation-map on ${compDir}`);
  console.log("Note: Full capture requires browser runtime. This port emits the contract.");

  const report = {
    composition: compDir,
    generated_at: new Date().toISOString(),
    summary: "Animation map would be produced by loading the composition in a headless browser, reading window.__timelines, sampling tweens, and computing flags.",
    tweens: [],
    ascii_timeline: "See original Codex script for full Gantt + stagger logic.",
    flags: { offscreen: 0, collision: 0, invisible: 0, paced_fast: 0, paced_slow: 0 },
    dead_zones: [],
    recommendations: [
      "Ensure every element has an entrance tween (gsap.from)",
      "Register all timelines in window.__timelines",
      "Use finite repeat calculated from duration",
      "Run with --samples 15 or more for dense videos"
    ]
  };

  await mkdir(outDir, { recursive: true });
  await writeFile(join(outDir, "animation-map.json"), JSON.stringify(report, null, 2));
  console.log(`Wrote ${join(outDir, "animation-map.json")}`);
  console.log("For full analysis, ensure node + @hyperframes/* + puppeteer and run the original or extended version of this script.");
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const [k, v] = a.replace(/^--/, "").split("=");
      args[k.replace(/-/g, "_")] = v ?? true;
    } else {
      args._.push(a);
    }
  }
  return { ...DEFAULTS, ...args };
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
