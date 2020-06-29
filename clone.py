#!/usr/bin/env python

import os
import subprocess
from typing import List, Dict, Tuple

from pydantic.main import BaseModel
from requests import get


class Repo(BaseModel):
    name: str
    full_name: str
    permissions: Dict[str, bool]
    ssh_url: str
    default_branch: str


class GetRepoResponse(BaseModel):
    repos: List[Repo]


def git(*args, cwd=None):
    return subprocess.check_call(['git'] + list(args), cwd=cwd or "code/")


def github_get(url, token):
    return get(
        url,
        headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token}"
        }
    )


def main(token: str):
    failures: List[Tuple[Repo, Exception]] = []
    raw_response = github_get("https://api.github.com/user/repos", token)
    while raw_response and raw_response.status_code == 200:
        response = GetRepoResponse(repos=raw_response.json())
        for repo in response.repos:
            try:
                if not os.path.isdir(f"code/{repo.name}"):
                    git("clone", repo.ssh_url)
                else:
                    git("pull", "origin", repo.default_branch, cwd=f"code/{repo.name}")
            except Exception as e:
                failures.append((repo, e))
        if "next" in raw_response.links:
            print("Fetching the next page from github")
            raw_response = github_get(raw_response.links["next"]["url"], token)
        else:
            raw_response = None

    if failures:
        print("oh no!/n")
        print("/n".join(f"{repo.full_name}: {error}" for (repo, error) in failures))
    else:
        print("okay")


if __name__ == "__main__":
    main(os.environ["TOKEN"])
