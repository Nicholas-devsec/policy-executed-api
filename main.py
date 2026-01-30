
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ActionRequest(BaseModel):
    action: str


actions = {
        "health_check": {
            "command": ["systemctl", "is-active", "ssh"],
            "max_output": 1024
        },
        }

app = FastAPI()

@app.post("/execute")

def create_command(req: ActionRequest):
    if req.action not in actions:
        logger.warning("Denied action: %s", req.action)
        raise HTTPException(status_code=403, detail="Post Command Not Allowed")
        
     

    action = actions[req.action]
    cmd = action["command"]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=3
    )
    max_output = action["max_output"]
    logger.info("Executed action: %s return_code=%d", req.action, result.returncode)


    
    return {
    "action": req.action,
    "stdout": result.stdout[:max_output].strip(),
    "stderr": result.stderr[:max_output].strip(),
    "return_code": result.returncode
}
        