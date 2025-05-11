from pathlib import Path
rootFolder = "shock"

def getRootPath() -> Path:
    parts = Path.cwd().parts
    if(rootFolder in parts):
        index = parts.index(rootFolder)
        return Path(*parts[: index+1])
    raise ("Root Folder not in Path. Make sure the rootFolder is set correctly.")
