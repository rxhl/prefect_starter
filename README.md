# prefect_starter

![Architecture](/assets/arch.png)

Read the full article [here](https://rxhl.notion.site/Decoding-the-EL-in-ELT-f3f56ed7e2d947c0b1618b5bee293256).

## Getting started

Make sure you have a GitHub token (fine-grained) with the permission to create gists. See [here](https://github.blog/2022-10-18-introducing-fine-grained-personal-access-tokens-for-github/) for more details on creating one.

### Local development

Clone repo and prepare for installation

```
git clone <this repo>
cd <this repo>
cp .env.example .env
pipenv shell
pipenv install
```

Launch Prefect locally

```
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
prefect server start

# In a separate window
python ./app.py
```

## References

1. https://docs.prefect.io/2.11.4/tutorial/
