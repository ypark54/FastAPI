from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path

app = FastAPI()
root = Path("C:/Users/yep/Desktop/CM_Projects")

@app.get("/")
async def main():
    items = root.iterdir()
    link_dir = ''
    link_file = ''
    for item in items:
        if item.is_dir():
            link_dir += f'<a href="/{item.name}/">{item.name}/</a><br>'
        else:
            link_file += f'<a href="/{item.name}">{item.name}</a><br>'
    links = link_dir + link_file
    
    return HTMLResponse(content=f"""
    <html>
        <head>
            <title>Root</title>
        </head>
        <body>
            {links}
        </body>
    </html>
    """)

@app.get("/{path:path}")
async def branch(path: str):  # Fix 1: Receive path as a string
    path_full = root / path
    path_full = path_full.resolve()  # Security check to resolve the actual path
    
    if root not in path_full.parents and path_full != root:  # Fix 3: Security check
        raise HTTPException(status_code=404, detail="Not allowed")

    if not path_full.is_dir():
        return FileResponse(path=path_full, filename=path_full.name)
    else:
        # Fix 2: Correctly calculate the parent directory's relative URL
        parent_path = path_full.parent.relative_to(root)
        parent_url = f"/{parent_path}/" if parent_path != root else "/"
        link_dir = f'<a href="{parent_url}">Parent Directory/</a><br>'
        link_file = ''
        items = path_full.iterdir()
        for item in items:
            if item.is_dir():
                link_dir += f'<a href="/{path}/{item.name}/">{item.name}/</a><br>'
            else:
                link_file += f'<a href="/{path}/{item.name}">{item.name}</a><br>'
        links = link_dir + link_file
        return HTMLResponse(content=f"""
        <html>
            <head>
                <title>{path_full.name}</title>
            </head>
            <body>
                {links}
            </body>
        </html>
        """)
