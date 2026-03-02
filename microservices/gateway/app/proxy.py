from fastapi import Request, Response
import httpx

async def forward(request: Request, upstream: str) -> Response:
    headers = dict(request.headers)
    headers.pop("host", None)

    body = await request.body()

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.request(
            method=request.method,
            url=upstream,
            params=dict(request.query_params),
            headers=headers,
            content=body,
        )
        return Response(content=r.content, status_code=r.status_code, headers=dict(r.headers))