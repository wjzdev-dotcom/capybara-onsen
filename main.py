import os, json, uvicorn, random, uuid, hashlib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

app = FastAPI()

class LevelGenerator:
    def __init__(self):
        # 预定义的简单模板，确保可玩性
        self.templates = [
            # 模板1: 简单布局
            [
                [1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,3,0,0,3,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,2,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,4,0,0,0,4,0,0,1],
                [1,0,0,0,3,0,4,0,0,1],
                [1,1,1,1,1,1,1,1,1,1]
            ],
            # 模板2: 对称布局
            [
                [1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,3,0,0,0,0,3,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,2,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,4,0,0,0,4,0,0,1],
                [1,0,0,0,3,0,4,0,0,1],
                [1,1,1,1,1,1,1,1,1,1]
            ],
            # 模板3: 角落布局
            [
                [1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,3,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,2,0,0,0,0,1],
                [1,0,0,0,0,0,3,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,4,0,0,0,4,0,0,1],
                [1,0,0,0,3,0,4,0,0,1],
                [1,1,1,1,1,1,1,1,1,1]
            ],
            # 模板4: 分散布局
            [
                [1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,3,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,2,0,0,0,0,0,0,1],
                [1,0,0,0,0,3,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,4,0,0,0,4,0,0,1],
                [1,0,0,0,3,0,4,0,0,1],
                [1,1,1,1,1,1,1,1,1,1]
            ],
            # 模板5: 简单挑战
            [
                [1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,3,0,0,3,0,3,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,2,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,4,4,4,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1]
            ]
        ]
    
    def generate_grid(self):
        """从模板中随机选择一个并轻微修改"""
        template = random.choice(self.templates)
        grid = [row[:] for row in template]  # 深拷贝
        
        # 对网格进行轻微随机调整
        for _ in range(random.randint(0, 5)):
            r = random.randint(1, 8)
            c = random.randint(1, 8)
            if grid[r][c] == 0:  # 如果是空地
                # 随机变为墙、箱子或目标
                grid[r][c] = random.choice([1, 3, 4])
        
        # 确保数量正确
        self.validate_grid(grid)
        return grid
    
    def validate_grid(self, grid):
        """确保网格有正确的元素数量"""
        player_count = 0
        box_count = 0
        goal_count = 0
        
        # 统计当前元素
        for r in range(10):
            for c in range(10):
                if grid[r][c] == 2:
                    player_count += 1
                elif grid[r][c] == 3:
                    box_count += 1
                elif grid[r][c] == 4:
                    goal_count += 1
        
        # 确保只有一个玩家
        if player_count != 1:
            # 移除多余的玩家
            found_one = False
            for r in range(10):
                for c in range(10):
                    if grid[r][c] == 2:
                        if found_one:
                            grid[r][c] = 0
                        else:
                            found_one = True
        
        # 确保有3个箱子
        if box_count != 3:
            # 添加或移除箱子
            while box_count < 3:
                # 添加箱子
                for r in range(1, 9):
                    for c in range(1, 9):
                        if grid[r][c] == 0:
                            grid[r][c] = 3
                            box_count += 1
                            break
                    if box_count == 3:
                        break
            
            while box_count > 3:
                # 移除箱子
                for r in range(1, 9):
                    for c in range(1, 9):
                        if grid[r][c] == 3:
                            grid[r][c] = 0
                            box_count -= 1
                            break
                    if box_count == 3:
                        break
        
        # 确保有3个目标
        if goal_count != 3:
            # 添加或移除目标
            while goal_count < 3:
                # 添加目标
                for r in range(1, 9):
                    for c in range(1, 9):
                        if grid[r][c] == 0:
                            grid[r][c] = 4
                            goal_count += 1
                            break
                    if goal_count == 3:
                        break
            
            while goal_count > 3:
                # 移除目标
                for r in range(1, 9):
                    for c in range(1, 9):
                        if grid[r][c] == 4:
                            grid[r][c] = 0
                            goal_count -= 1
                            break
                    if goal_count == 3:
                        break

generator = LevelGenerator()

@app.post("/api/generate-level")
async def generate_level():
    try:
        # 生成唯一种子
        unique_seed = str(uuid.uuid4())
        
        # 如果有AI可用，尝试生成地图
        if client:
            try:
                # 准备AI生成提示
                prompt = f"""
                Create a 10x10 Sokoban puzzle for a game called "Ghost Capybara".
                Grid values: 0=empty, 1=wall, 2=player (ONE only), 3=yuzu fruit (EXACTLY THREE), 4=onsen/hot spring (EXACTLY THREE).
                
                Requirements:
                1. Outer border must be walls (row 0, row 9, col 0, col 9 are all 1)
                2. Exactly 1 player (2), 3 yuzu fruits (3), 3 onsens (4)
                3. Make it solvable - no deadlocks
                4. Keep it simple for beginners
                5. Return ONLY this JSON format: {{"grid": [[10 arrays of 10 numbers]]}}
                
                Level ID: {unique_seed}
                """
                
                # 使用正确的模型名称
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                
                # 解析响应
                data = json.loads(response.text)
                grid = data.get("grid", [])
                
                # 验证AI生成的网格
                if len(grid) == 10 and len(grid[0]) == 10:
                    # 验证元素数量
                    player_count = sum(row.count(2) for row in grid)
                    box_count = sum(row.count(3) for row in grid)
                    goal_count = sum(row.count(4) for row in grid)
                    
                    if player_count == 1 and box_count == 3 and goal_count == 3:
                        # AI生成成功
                        response_data = {
                            "grid": grid,
                            "dialogues": [
                                "Push the yuzu fruits to the onsen!",
                                "Careful not to drop them in water!",
                                "Three yuzu, three hot springs."
                            ],
                            "seed": unique_seed[:8],
                            "source": "ai_generated"
                        }
                        
                        # 添加禁止缓存的头部
                        headers = {
                            "Cache-Control": "no-store, no-cache, must-revalidate",
                            "Pragma": "no-cache",
                            "X-Level-Seed": unique_seed[:8]
                        }
                        
                        return JSONResponse(content=response_data, headers=headers)
                
            except Exception as e:
                print(f"AI generation failed: {e}")
                # 继续使用本地生成
        
        # 本地生成关卡
        grid = generator.generate_grid()
        
        # 生成对话
        dialogues = [
            "Welcome to Capybara Onsen!",
            "Push yuzu fruits to hot springs.",
            "Relax and enjoy the puzzle!",
            "Use arrow keys to move.",
            "You can push but not pull yuzu.",
            "Three yuzu need three onsens."
        ]
        selected_dialogues = random.sample(dialogues, min(3, len(dialogues)))
        
        response_data = {
            "grid": grid,
            "dialogues": selected_dialogues,
            "seed": unique_seed[:8],
            "source": "local_generated"
        }
        
        # 添加禁止缓存的头部
        headers = {
            "Cache-Control": "no-store, no-cache, must-revalidate",
            "Pragma": "no-cache",
            "X-Level-Seed": unique_seed[:8]
        }
        
        return JSONResponse(content=response_data, headers=headers)
        
    except Exception as e:
        print(f"Error generating level: {e}")
        # 终极回退
        return JSONResponse(content={
            "grid": [
                [1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,3,0,0,0,0,3,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,2,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,0,4,0,0,0,4,0,0,1],
                [1,0,0,0,3,0,4,0,0,1],
                [1,1,1,1,1,1,1,1,1,1]
            ],
            "dialogues": ["Fallback level loaded!", "Push yuzu to onsens!"],
            "seed": "fallback",
            "source": "fallback"
        })

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

# 确保static目录存在
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)