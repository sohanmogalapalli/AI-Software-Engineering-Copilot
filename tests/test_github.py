import pytest
from backend.parsing.github_cloner import GitHubCloner

def test_parse_github_url():
    owner, repo = GitHubCloner.parse_github_url("https://github.com/pallets/flask")
    assert owner == "pallets"
    assert repo == "flask"

    owner, repo = GitHubCloner.parse_github_url("https://github.com/psf/requests.git")
    assert owner == "psf"
    assert repo == "requests"

    owner, repo = GitHubCloner.parse_github_url("git@github.com:torvalds/linux.git")
    assert owner == "torvalds"
    assert repo == "linux"

    with pytest.raises(ValueError):
        GitHubCloner.parse_github_url("https://notgithub.com/invalid")
