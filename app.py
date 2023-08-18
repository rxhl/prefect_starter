import os
from dotenv import load_dotenv

from datetime import timedelta
from github import InputFileContent
import nbformat
import jupytext
import pickle
from nbconvert.preprocessors import ExecutePreprocessor
import pandas as pd

from github import Github
from github import Auth
from prefect import flow, task, get_run_logger

load_dotenv()

REPO_NAME = "rxhl/django-cloudrun"
ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")


@task
def connect_github():
    auth = Auth.Token(ACCESS_TOKEN)
    github_api = Github(auth=auth)
    return github_api


@task
def github_stargazers_by_week(github_api):
    stargazers = list(
        github_api.get_repo(REPO_NAME).get_stargazers_with_dates()
    )
    df = pd.DataFrame(
        [
            {
                "users": stargazer.user.login,
                "week": stargazer.starred_at.date()
                + timedelta(days=6 - stargazer.starred_at.weekday()),
            }
            for stargazer in stargazers
        ]
    )
    return df.groupby("week").count().sort_values(by="week")


@task
def github_stars_notebook(github_stargazers_by_week):
    markdown = f"""
        # Github Stars

        ```python
        import pickle
        github_stargazers_by_week = pickle.loads({pickle.dumps(github_stargazers_by_week)!r})
        ```

        ## Github Stars by Week, last 52 weeks
        ```python
        github_stargazers_by_week.tail(52).reset_index().plot.bar(x="week", y="users")
        ```
    """
    nb = jupytext.reads(markdown, "md")
    ExecutePreprocessor().preprocess(nb)
    return nbformat.writes(nb)


@task
def github_stars_notebook_gist(github_api, github_stars_notebook):
    gist = github_api.get_user().create_gist(
        public=False,
        files={
            "github_stars.ipynb": InputFileContent(github_stars_notebook),
        },
    )
    return gist.html_url


@flow(retries=3, retry_delay_seconds=5)
def driver():
    api = connect_github()
    gazers = github_stargazers_by_week(api)
    nb = github_stars_notebook(gazers)
    gist_url = github_stars_notebook_gist(api, nb)

    logger = get_run_logger()
    logger.info(gist_url)


if __name__ == "__main__":
    driver()
