import os
from pydantic import BaseSettings

class FaissDBSettings(BaseSettings):
    base_dir: str = os.path.join(os.path.expanduser('~'), '.autoai', 'faissdb', 'data')
    class Config:
        env_prefix='faissdb_'