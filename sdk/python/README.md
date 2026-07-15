# SledTrace Python SDK

Python SDK for sending local RAG pipeline traces to SledTrace.

## Install (v0.4.1 local path)

```bash
pip install -e /path/to/sledtrace/sdk/python
```

## Basic Usage

```python
from sledtrace import trace

user_query = "What is the refund policy?"

with trace(name="my-rag-request", query=user_query) as t:
    # Run retriever
    retrieved_chunks = [
        {
            "id": "refund_policy_1",
            "text": "Refunds are accepted within 30 days with proof of purchase.",
            "score": 0.92,
            "source": "refund_policy.md",
        }
    ]

    # Convert retriever-native results into SledTrace-style chunk dicts
    t.retrieval(
        query=user_query,
        chunks=retrieved_chunks,
        top_k=1,
    )

    # Build prompt
    context = "\n\n".join(chunk["text"] for chunk in retrieved_chunks)
    prompt = f"Question: {user_query}\n\nContext:\n{context}"

    # Run answerer/LLM
    answer = "You can request a refund within 30 days with proof of purchase."
    t.llm(
        provider="local-demo",
        model="mock-answerer",
        prompt=prompt,
        output_text=answer,
    )

# Flush after the with-block
t.flush()
```

## Collector URL

Default collector URL: [http://localhost:4319](http://localhost:4319)

Bash:

```bash
export SLEDTRACE_COLLECTOR_URL=http://localhost:4319
```

PowerShell:

```powershell
$env:SLEDTRACE_COLLECTOR_URL="http://localhost:4319"
```

## More Docs

- ../../docs/product/USER_ONBOARDING.md
- ../../docs/integrations/PYTHON_SDK_GUIDE.md

Repository examples such as examples.custom_pipeline_demo are local examples, not part of the public installed SDK API.




