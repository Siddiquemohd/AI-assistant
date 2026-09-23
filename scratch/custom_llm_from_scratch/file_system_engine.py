import os

class FileSystemAutomatorEngine:
    """
    Automated Local File System Management & Organization Engine.
    Performs file sorting, batch renaming, file tree inspection, and directory cleanups.
    """

    def inspect_directory(self, dir_path: str = ".") -> dict:
        if not os.path.exists(dir_path):
            return {"status": "Error", "error": f"Directory '{dir_path}' not found."}

        files = []
        dirs = []
        for entry in os.listdir(dir_path):
            full_p = os.path.join(dir_path, entry)
            if os.path.isdir(full_p):
                dirs.append(entry)
            else:
                files.append(entry)

        return {
            "status": "Success",
            "directory": os.path.abspath(dir_path),
            "file_count": len(files),
            "subdir_count": len(dirs),
            "files": files[:20],
            "subdirectories": dirs[:20]
        }
