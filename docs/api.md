# API Documentation

Base URL: `http://localhost:8000/api/v1`

## `POST /search`
Create a case and run initial public-source discovery.

### Request
```json
{
  "case_name": "Investigation A",
  "description": "Public OSINT scan",
  "identifiers": [
    {"input_type": "username", "value": "janedoe"}
  ]
}
```

### Response
- `case_id`
- `profiles[]`
- `timeline[]`
- `risk`

## `GET /health`
Health probe endpoint.

## Planned Endpoints
- `POST /cases`
- `GET /cases/{id}`
- `POST /reports/{case_id}/export?format=pdf|html|json|csv`
- `POST /watchlists`


## `GET /websearch?q=<query>&limit=8`
Runs live public web search against DuckDuckGo HTML endpoint and returns normalized web hits.


## Notes
- Web search is live and uses public search results only.
- Platform analysis modules do not depend on external AI APIs.
