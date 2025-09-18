# P.i.f.k.o



How to run:

1. docker compose build
2. docker compose up




Optionally (restart scenario):

1. docker compose down -v  (erases everything)
2. docker compose build --no-cache
3. docker compose up



MOCKING: 

cd src/Pifko
uv run mock_db.py

CLEANING:

cd src/Pifko
uv run clean_db.py



mcp inspector:

npx @modelcontextprotocol/inspector


