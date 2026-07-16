import { mkdir } from "node:fs/promises";
import { chromium } from "playwright";

const baseUrl = (process.env.BASE_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
const artifactDir = process.env.BROWSER_SMOKE_ARTIFACT_DIR ?? "browser-smoke-artifacts";

const routes = [
  { path: "/", name: "home" },
  { path: "/architecture/", name: "architecture" },
  { path: "/architecture/system-ownership-and-execution-map/", name: "diagram" },
  { path: "/interactive/inference-workflow/", name: "interactive", expectsIframe: true },
];

const viewports = [
  { name: "desktop", width: 1440, height: 1000 },
  { name: "mobile", width: 390, height: 844 },
];

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

async function inspectRoute(browser, route, viewport) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    colorScheme: "light",
    reducedMotion: "reduce",
  });
  const page = await context.newPage();
  const browserErrors = [];

  page.on("pageerror", error => browserErrors.push(`pageerror: ${error.message}`));
  page.on("console", message => {
    if (message.type() === "error") {
      browserErrors.push(`console: ${message.text()}`);
    }
  });

  const url = `${baseUrl}${route.path}`;
  try {
    const response = await page.goto(url, { waitUntil: "networkidle", timeout: 30_000 });
    assert(response !== null, `${route.name}/${viewport.name}: navigation returned no response`);
    assert(response.ok(), `${route.name}/${viewport.name}: HTTP ${response.status()} for ${url}`);

    assert(await page.locator("main").count() === 1, `${route.name}/${viewport.name}: expected exactly one main landmark`);
    assert(await page.locator("h1").count() === 1, `${route.name}/${viewport.name}: expected exactly one h1`);
    assert((await page.locator("h1").innerText()).trim().length > 0, `${route.name}/${viewport.name}: h1 is empty`);

    const searchInput = page.locator('input[type="text"][placeholder*="Search"], input[data-md-component="search-query"]');
    assert(await searchInput.count() >= 1, `${route.name}/${viewport.name}: search input is not discoverable`);

    const hasHorizontalOverflow = await page.evaluate(() => {
      const root = document.documentElement;
      return root.scrollWidth > root.clientWidth + 1;
    });
    assert(!hasHorizontalOverflow, `${route.name}/${viewport.name}: page has horizontal overflow`);

    const reducedMotionMatches = await page.evaluate(() => window.matchMedia("(prefers-reduced-motion: reduce)").matches);
    assert(reducedMotionMatches, `${route.name}/${viewport.name}: reduced-motion browser preference was not applied`);

    if (route.name === "architecture") {
      const architectureLinks = await page.locator('main a[href*="architecture/"]').count();
      assert(architectureLinks >= 6, `${route.name}/${viewport.name}: expected at least six architecture entry links, found ${architectureLinks}`);
    }

    if (route.expectsIframe) {
      const iframe = page.locator("main iframe");
      assert(await iframe.count() >= 1, `${route.name}/${viewport.name}: expected an interactive iframe`);
      const title = ((await iframe.first().getAttribute("title")) ?? "").trim();
      assert(title.length > 0, `${route.name}/${viewport.name}: iframe has no accessible title`);
    }

    await page.keyboard.press("Tab");
    const focusState = await page.evaluate(() => {
      const element = document.activeElement;
      if (!element || element === document.body) return null;
      const rect = element.getBoundingClientRect();
      const style = getComputedStyle(element);
      return {
        tag: element.tagName,
        width: rect.width,
        height: rect.height,
        visibility: style.visibility,
        display: style.display,
      };
    });
    assert(focusState !== null, `${route.name}/${viewport.name}: first Tab did not reach a focusable element`);
    assert(focusState.width > 0 && focusState.height > 0, `${route.name}/${viewport.name}: focused element has no visible box`);
    assert(focusState.visibility !== "hidden" && focusState.display !== "none", `${route.name}/${viewport.name}: focused element is hidden`);

    assert(browserErrors.length === 0, `${route.name}/${viewport.name}: browser errors:\n${browserErrors.join("\n")}`);
    console.log(`PASS ${route.name}/${viewport.name}: ${url}`);
  } catch (error) {
    await mkdir(artifactDir, { recursive: true });
    const screenshotPath = `${artifactDir}/${route.name}-${viewport.name}.png`;
    await page.screenshot({ path: screenshotPath, fullPage: true }).catch(() => {});
    throw new Error(`${error.message}\nFailure screenshot: ${screenshotPath}`);
  } finally {
    await context.close();
  }
}

const browser = await chromium.launch({ headless: true });
try {
  for (const viewport of viewports) {
    for (const route of routes) {
      await inspectRoute(browser, route, viewport);
    }
  }
} finally {
  await browser.close();
}

console.log(`Browser smoke validation passed for ${routes.length} routes across ${viewports.length} viewports.`);
