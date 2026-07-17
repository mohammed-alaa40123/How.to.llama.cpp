const CURRENT_SCHEMA_VERSION = "0.1.0";
const STORAGE_SCOPE = "local-only";
const MAX_BYTES = 512 * 1024;
const SHA_RE = /^[0-9a-f]{40}$/;
const SEMVER_RE = /^[0-9]+\.[0-9]+\.[0-9]+(?:-[a-z0-9.-]+)?$/;
const ID_RE = /^[a-z0-9][a-z0-9._-]{2,95}$/;
const FORBIDDEN_KEYS = new Set([
  "name", "email", "username", "user_id", "ip", "ip_address", "prompt",
  "raw_prompt", "response", "raw_response", "code", "raw_code", "telemetry",
  "session_id", "device_id"
]);

export class ProgressImportError extends Error {}

function requireValue(condition, message) {
  if (!condition) throw new ProgressImportError(message);
}

function walkForbidden(value, path = "$") {
  if (Array.isArray(value)) {
    value.forEach((item, index) => walkForbidden(item, `${path}[${index}]`));
  } else if (value && typeof value === "object") {
    for (const [key, child] of Object.entries(value)) {
      requireValue(!FORBIDDEN_KEYS.has(key), `${path}.${key}: forbidden privacy-sensitive field`);
      walkForbidden(child, `${path}.${key}`);
    }
  }
}

export function validateProgress(data) {
  requireValue(data && typeof data === "object" && !Array.isArray(data), "progress export must be an object");
  walkForbidden(data);
  const top = ["schema_version", "course_id", "course_version", "source_revision", "exported_at", "storage_scope", "lessons"];
  requireValue(Object.keys(data).sort().join("|") === [...top].sort().join("|"), "top-level fields must exactly match the progress contract");
  requireValue(data.schema_version === CURRENT_SCHEMA_VERSION, "unsupported schema_version");
  requireValue(data.course_id === "how-to-llama-cpp", "unexpected course_id");
  requireValue(SEMVER_RE.test(data.course_version), "course_version must be semantic version");
  requireValue(SHA_RE.test(data.source_revision), "source_revision must be a full immutable SHA");
  requireValue(typeof data.exported_at === "string" && !Number.isNaN(Date.parse(data.exported_at)) && /(Z|[+-]\d\d:\d\d)$/.test(data.exported_at), "exported_at must be timezone-aware ISO-8601");
  requireValue(data.storage_scope === STORAGE_SCOPE, "storage_scope must remain local-only");
  requireValue(Array.isArray(data.lessons) && data.lessons.length <= 128, "lessons must be a bounded array");
  const lessonIds = new Set();
  for (const lesson of data.lessons) {
    requireValue(lesson && typeof lesson === "object" && !Array.isArray(lesson), "lesson must be an object");
    requireValue(ID_RE.test(lesson.lesson_id), "lesson_id is invalid");
    requireValue(!lessonIds.has(lesson.lesson_id), `duplicate lesson_id: ${lesson.lesson_id}`);
    lessonIds.add(lesson.lesson_id);
    requireValue(SEMVER_RE.test(lesson.lesson_version), "lesson_version is invalid");
    requireValue(["not-started", "in-progress", "completed"].includes(lesson.status), "lesson status is invalid");
    requireValue(Array.isArray(lesson.checkpoints) && lesson.checkpoints.length <= 256, "checkpoints must be bounded");
    const checkpointIds = new Set();
    let passed = 0;
    let attempted = 0;
    for (const checkpoint of lesson.checkpoints) {
      requireValue(ID_RE.test(checkpoint.checkpoint_id), "checkpoint_id is invalid");
      requireValue(!checkpointIds.has(checkpoint.checkpoint_id), `duplicate checkpoint_id: ${checkpoint.checkpoint_id}`);
      checkpointIds.add(checkpoint.checkpoint_id);
      requireValue(["unanswered", "answered", "passed"].includes(checkpoint.state), "checkpoint state is invalid");
      requireValue(Number.isInteger(checkpoint.attempt_count) && checkpoint.attempt_count >= 0 && checkpoint.attempt_count <= 100, "attempt_count is invalid");
      requireValue(checkpoint.state !== "unanswered" || checkpoint.attempt_count === 0, "unanswered requires zero attempts");
      requireValue(checkpoint.state === "unanswered" || checkpoint.attempt_count > 0, "answered/passed requires an attempt");
      attempted += checkpoint.attempt_count > 0 ? 1 : 0;
      passed += checkpoint.state === "passed" ? 1 : 0;
    }
    const lastStep = lesson.last_step_id ?? null;
    if (lesson.status === "not-started") requireValue(attempted === 0 && lastStep === null, "not-started cannot contain attempts or last_step_id");
    if (lesson.status === "in-progress") requireValue(lastStep !== null || attempted > 0, "in-progress requires a step or attempt");
    if (lesson.status === "completed") requireValue(lesson.checkpoints.length > 0 && passed === lesson.checkpoints.length, "completed requires every checkpoint passed");
  }
  return data;
}

export function migrateProgress(data) {
  requireValue(data && typeof data === "object", "progress export must be an object");
  requireValue(data.schema_version === CURRENT_SCHEMA_VERSION, `no migration path for schema_version ${String(data.schema_version)}`);
  return structuredClone(data);
}

export function importProgress(rawText, currentState) {
  requireValue(typeof rawText === "string", "import must be UTF-8 JSON text");
  requireValue(new TextEncoder().encode(rawText).byteLength <= MAX_BYTES, `progress export exceeds ${MAX_BYTES} bytes`);
  let parsed;
  try { parsed = JSON.parse(rawText); } catch (error) { throw new ProgressImportError(`cannot parse progress JSON: ${error.message}`); }
  const candidate = migrateProgress(parsed);
  validateProgress(candidate);
  return { state: structuredClone(candidate), previousState: structuredClone(currentState) };
}

export function exportProgress(state) {
  validateProgress(state);
  return `${JSON.stringify(state, null, 2)}\n`;
}

export function createLocalStorageAdapter(storage, key = "how-to-llama-cpp.progress.v0") {
  requireValue(storage && typeof storage.getItem === "function" && typeof storage.setItem === "function" && typeof storage.removeItem === "function", "storage adapter is invalid");
  return {
    load() {
      const raw = storage.getItem(key);
      if (raw === null) return null;
      return importProgress(raw, null).state;
    },
    save(state) {
      const raw = exportProgress(state);
      storage.setItem(key, raw);
      return raw;
    },
    clear() { storage.removeItem(key); },
    import(rawText) {
      const previousRaw = storage.getItem(key);
      const previous = previousRaw === null ? null : importProgress(previousRaw, null).state;
      const result = importProgress(rawText, previous);
      storage.setItem(key, exportProgress(result.state));
      return result.state;
    },
    export() {
      const state = this.load();
      requireValue(state !== null, "no local progress exists");
      return exportProgress(state);
    }
  };
}

export const progressContract = Object.freeze({
  schemaVersion: CURRENT_SCHEMA_VERSION,
  storageScope: STORAGE_SCOPE,
  maxBytes: MAX_BYTES
});
