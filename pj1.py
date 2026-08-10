import os
import runpy

current_dir = os.path.dirname(os.path.abspath(__file__))
target_app = os.path.join(current_dir, "app", "app.py")

if __name__ == "__main__":
    runpy.run_path(target_app, run_name="__main__")
else:
    runpy.run_path(target_app)