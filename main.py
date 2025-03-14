import json
import subprocess

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from functions import get_song_by_id

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/update")
async def update(key: str = Query(..., description="Secret key for update")):
    if key != "YoisakiKanade0210":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        result = subprocess.run(
            ['git', 'pull'],
            cwd='assets',
            capture_output=True,
            text=True,
            check=True
        )
        return {"message": "Update successful", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Git pull failed: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/chunithm/song/all")
async def chunithm_song():
    filepath = "./assets/chunithm/data/music-ex.json"
    with open(filepath, 'r') as all_song :
        return all_song.read()

@app.get("/chunithm/song/{songid}/", response_model=dict)
async def song_info(songid: str):
    # 添加输入验证（可选）
    if not songid.isdigit():
        raise HTTPException(status_code=400, detail="Invalid song ID format")

    # 处理数据获取
    try:
        song_data = await get_song_by_id(songid)
        if not song_data:
            raise HTTPException(status_code=404, detail="Song not found")
        return song_data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid music data format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/chunithm/cover/{songid}")
async def song_cover(songid: str):
    try:
        song_data = await get_song_by_id(songid)
        if not song_data:
            raise HTTPException(status_code=404, detail="Song not found")

        image_filename = song_data.get("image")
        if not image_filename:
            raise HTTPException(status_code=404, detail="Image not found for the song")

        filepath = f"./assets/chunithm/jacket/{image_filename}"
        return FileResponse(filepath)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid music data format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")