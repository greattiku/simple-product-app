# app/core/env.py

import os
from dotenv import load_dotenv

load_dotenv()
AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(5)
print(f"ALGORITHM = {repr(ALGORITHM)}")
print(f"AUTH_SECRET_KEY = {repr(AUTH_SECRET_KEY)}")