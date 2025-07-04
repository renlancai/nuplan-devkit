
import os
from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Set, List, Optional


class ConcurrentGzScanner:
    def __init__(self, max_workers=8):
        self.candidate_dirs = set()
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.is_shutdown = False
    
    def _scan_subdir(self, subdir):
        for gz_file in Path(subdir).rglob("*.gz"):
            with self.lock:
                self.candidate_dirs.add((gz_file.parent))
                if (len(self.candidate_dirs) % 1000 == 0):
                    print(len(self.candidate_dirs))
                    # print(f"Found {len(self.candidate_dirs)} candidate directories so far")

    
    def _scan_root(self, subdir):
        for gz_file in Path(subdir).glob("*.gz"):
            with self.lock:
                self.candidate_dirs.add((gz_file.parent))
                

    def scan(self, root_dir):
        # print(f"Scanning directory: {root_dir}")
        root = Path(root_dir)
        subdirs = [str(d) for d in root.iterdir() if d.is_dir()]
        
        self._scan_root(root_dir)
        
        for subdir in subdirs:
            self.executor.submit(self._scan_subdir, subdir)
        
        self.executor.shutdown(wait=True)
        return self.candidate_dirs



class ConcurrentFeatureMatcher:
    def __init__(self, feature_names: Set[str], max_workers: int = 32):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.feature_names = feature_names
        self.lock = threading.Lock()
        self.scenario_cache_paths = []
    
    def _match_single(self, path: str):
        # import pdb; pdb.set_trace()
        path_obj = Path(path)
        if not path_obj.exists():
            print(f"warning: path dose not exists: {path}")
            return None
        try:
            existing_features = {f.stem for f in path_obj.iterdir()}
            if not (self.feature_names - existing_features):
                with self.lock:
                    self.scenario_cache_paths.append(path)
        except PermissionError:
            print(f"no access: {path}")
            return None
        except Exception as e:
            print(f"process {path} wrong: {str(e)}")
            return None

    def batch_match(self, paths):
        for path in paths:
            # print(path)
            self.executor.submit(self._match_single, path)
        
        self.executor.shutdown(wait=True)
        return self.scenario_cache_paths
