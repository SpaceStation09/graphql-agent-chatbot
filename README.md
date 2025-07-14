# GraphQL expert in Multi-agent system (WIP)

This project aims to build a demo for GraphQL expert agent which can be invoked in a multi-agent system (building with langGraph).

## Structure Design

```
User Input
    ↓
Orchestrator (Routing Decision)
    ↓
    ├── Graphql Agent (Graphql Queries) 
    └── format_response (Response Formatting)
    ↓
Return to User
```

## Usage

```bash
  uv run src/main.py
```



