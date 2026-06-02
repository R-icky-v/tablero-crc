import sys
import os

# agrega la raíz del proyecto al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.infraestructura.app import app