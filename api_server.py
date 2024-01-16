#!/usr/bin/env python

from fastapi import FastAPI
from langserve import add_routes

from secon_d_summary.chain import build_chain

app = FastAPI(title="secon dev diary summarizer")
chain = build_chain().with_types(input_type=str, output_type=dict)
add_routes(app, chain)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
