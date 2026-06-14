export type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonObject
  | JsonValue[];

export type JsonObject = {
  [key: string]: JsonValue;
};

export type TraceListItem = {
  trace_id: string;
  name: string;
  status: string;
  query: string;
  answer: string;
  duration_ms: number | null;
  warning_count: number;
  started_at: string;
};

export type TraceRecord = {
  trace_id: string;
  name: string;
  status: string;
  input: JsonObject;
  output: JsonObject;
  metadata: JsonObject;
  started_at: string;
  ended_at: string | null;
  duration_ms: number | null;
};

export type Span = {
  span_id: string;
  trace_id: string;
  parent_span_id: string | null;
  type: string;
  name: string;
  status: string;
  input: JsonObject;
  output: JsonObject;
  metadata: JsonObject;
  started_at: string;
  ended_at: string | null;
  duration_ms: number | null;
  error: JsonObject | null;
};

export type Warning = {
  warning_id: string;
  trace_id: string;
  span_id: string | null;
  type: string;
  severity: string;
  message: string;
  details: JsonObject;
  created_at: string;
};

export type TraceListResponse = {
  traces: TraceListItem[];
};

export type TraceDetailResponse = {
  trace: TraceRecord;
  spans: Span[];
  warnings: Warning[];
};

export type Chunk = {
  id?: string;
  text?: string;
  score?: number;
  rank?: number;
  source?: string;
  document_id?: string;
  metadata?: JsonObject;
};