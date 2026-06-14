import type { JsonValue } from "../types";

type Props = {
  value: JsonValue;
};

export default function JsonViewer({ value }: Props) {
  return <pre className="json-viewer">{JSON.stringify(value, null, 2)}</pre>;
}