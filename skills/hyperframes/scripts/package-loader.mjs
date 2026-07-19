#!/usr/bin/env node
// package-loader.mjs — Grok-ported HyperFrames dependency bootstrap helper
// Original from Codex hyperframes skill. Handles dynamic import or npm bootstrap
// for analysis scripts (animation-map, contrast-report) that need puppeteer/playwright + hyperframes packages.
//
// In Grok environments, full visual analysis requires Node + a headless browser toolchain.
// The authoring rules in the SKILL.md are the primary value and work without the scripts.

import { spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import { basename, delimiter, dirname, join, parse, resolve } from "node:path";
import { createInterface } from "node:readline/promises";
import { fileURLToPath, pathToFileURL } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const BOOTSTRAP_ENV = "HYPERFRAMES_SKILL_DEPS_BOOTSTRAPPED";
const BOOTSTRAP_CONFIRM_ENV = "HYPERFRAMES_SKILL_BOOTSTRAP_DEPS";
const NODE_MODULES_ENV = "HYPERFRAMES_SKILL_NODE_MODULES";

export async function importPackagesOrBootstrap(packageNames, options = {}) {
  const entries = new Map();
  const missing = [];

  for (const packageName of packageNames) {
    const entry = resolvePackageEntry(packageName);
    if (entry) entries.set(packageName, entry);
    else missing.push(packageName);
  }

  if (missing.length > 0 && !process.env[BOOTSTRAP_ENV]) {
    const npmPackages = options.npmPackages ?? missing;
    assertPinnedPackageSpecs(npmPackages);
    await confirmBootstrap(npmPackages);
    bootstrapWithNpmInstall(npmPackages);
  }

  // Re-resolve after potential bootstrap
  for (const name of missing) {
    const entry = resolvePackageEntry(name);
    if (entry) entries.set(name, entry);
  }

  return entries;
}

function resolvePackageEntry(packageName) {
  // Simplified resolution for Grok port; full original walks NODE_PATH and hyperframes package spec
  try {
    const req = createRequire(import.meta.url);
    const resolved = req.resolve(packageName + "/package.json");
    return resolved;
  } catch {
    return null;
  }
}

function assertPinnedPackageSpecs(packages) {
  // In real use, pin exact versions as in the original hyperframes skill
  if (!packages || packages.length === 0) throw new Error("No packages to bootstrap");
}

async function confirmBootstrap(packages) {
  if (process.env[BOOTSTRAP_CONFIRM_ENV] === "0") return;
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  const answer = await rl.question(
    `HyperFrames analysis requires npm packages: ${packages.join(", ")}. Install now into a temp dir? (y/N) `
  );
  rl.close();
  if (!/^y/i.test(answer)) {
    console.error("Aborting. Set HYPERFRAMES_SKILL_BOOTSTRAP_DEPS=0 to skip prompts.");
    process.exit(2);
  }
}

function bootstrapWithNpmInstall(packages) {
  const tmp = mkdtempSync(join(tmpdir(), "grok-hyperframes-"));
  const env = { ...process.env };
  env[BOOTSTRAP_ENV] = "1";

  const result = spawnSync("npm", ["install", "--prefix", tmp, ...packages], {
    stdio: "inherit",
    env,
  });

  if (result.status !== 0) {
    rmSync(tmp, { recursive: true, force: true });
    throw new Error("npm bootstrap failed");
  }

  process.env[NODE_MODULES_ENV] = join(tmp, "node_modules");
  console.log(`Bootstrapped into ${tmp}. Set ${NODE_MODULES_ENV} for future runs.`);
}

export const hyperframesPackageSpec = {
  // Pins would live here in a full port
};
