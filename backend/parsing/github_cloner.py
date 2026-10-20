import os
import re
import shutil
import stat
import subprocess
from pathlib import Path
from typing import Optional, Tuple
import urllib.request
import zipfile

from backend.utils.config import settings
from backend.utils.logging import logger

def force_remove_tree(path: Path | str) -> None:
    """Robustly delete directory tree on Windows handling read-only files."""
    p = Path(path)
    if not p.exists():
        return

    def on_rm_error(func, file_path, exc_info):
        try:
            os.chmod(file_path, stat.S_IWRITE)
            func(file_path)
        except Exception:
            pass

    shutil.rmtree(p, onerror=on_rm_error)

class GitHubCloner:
    @staticmethod
    def parse_github_url(url: str) -> Tuple[str, str]:
        """
        Extract (owner, repo_name) from various GitHub URL formats:
        - https://github.com/owner/repo
        - https://github.com/owner/repo.git
        - git@github.com:owner/repo.git
        """
        clean_url = url.strip()
        clean_url = re.sub(r"\.git/?$", "", clean_url)

        match = re.search(r"github\.com[:/]([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-]+)", clean_url)
        if not match:
            raise ValueError(f"Invalid GitHub repository URL: {url}")

        owner, repo = match.group(1), match.group(2)
        return owner, repo

    @staticmethod
    def clone_repository(
        github_url: str,
        target_dir: Optional[Path | str] = None,
        branch: Optional[str] = None,
        force: bool = False
    ) -> Path:
        """
        Clone a GitHub repository using shallow git clone (depth 1),
        with fallback to ZIP archive download.
        """
        owner, repo_name = GitHubCloner.parse_github_url(github_url)

        if target_dir is None:
            settings.repository_dir.mkdir(parents=True, exist_ok=True)
            dest_path = settings.repository_dir / repo_name
        else:
            dest_path = Path(target_dir)

        if dest_path.exists():
            if force:
                logger.info(f"Target directory exists. Removing for fresh clone: {dest_path}")
                force_remove_tree(dest_path)
            else:
                logger.info(f"Repository already cloned at: {dest_path}. Using existing files.")
                return dest_path

        logger.info(f"Cloning GitHub repository [cyan]{github_url}[/cyan] into [green]{dest_path}[/green]...")

        # 1. Try git clone --depth 1 (with branch if provided)
        if branch:
            cmd = ["git", "clone", "--depth", "1", "--branch", branch, github_url, str(dest_path)]
            try:
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                logger.info(f"Successfully cloned branch '{branch}' via git: {dest_path}")
                return dest_path
            except subprocess.CalledProcessError as e:
                logger.warning(f"git clone with branch '{branch}' failed. Retrying with default branch...")
                force_remove_tree(dest_path)

        # 1b. Try git clone --depth 1 without branch
        cmd_default = ["git", "clone", "--depth", "1", github_url, str(dest_path)]
        try:
            subprocess.run(cmd_default, capture_output=True, text=True, check=True)
            logger.info(f"Successfully cloned default branch via git: {dest_path}")
            return dest_path
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.warning(f"git clone failed ({e}). Attempting zip archive download fallback...")
            force_remove_tree(dest_path)

        # 2. Fallback: Download ZIP archive from GitHub
        zip_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/{branch or 'main'}.zip"
        temp_zip = settings.repository_dir / f"{repo_name}_temp.zip"

        try:
            logger.info(f"Downloading archive from {zip_url}...")
            urllib.request.urlretrieve(zip_url, temp_zip)

            with zipfile.ZipFile(temp_zip, "r") as z:
                root_extracted = z.namelist()[0].split("/")[0]
                z.extractall(settings.repository_dir)

                extracted_path = settings.repository_dir / root_extracted
                if extracted_path != dest_path:
                    force_remove_tree(dest_path)
                    shutil.move(str(extracted_path), str(dest_path))

            if temp_zip.exists():
                temp_zip.unlink()

            logger.info(f"Successfully extracted zip archive to: {dest_path}")
            return dest_path
        except Exception as zip_err:
            if temp_zip.exists():
                temp_zip.unlink()
            raise RuntimeError(f"Failed to clone or download repository from {github_url}: {zip_err}")
