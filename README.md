# prefect_starter

![Architecture](/assets/arch.png)

Read the full article [here]().

## Getting started

### Local development

Clone repo and prepare for installation

```
git clone <this repo>
cd <this repo>
cp .env.example .env
pipenv shell
pipenv install
```

Launch prefect locally

```
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
prefect server start

# In a separate window
python ./app.py
```

## References

1. https://docs.prefect.io/2.11.4/tutorial/
