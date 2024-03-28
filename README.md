# Assignment for XXXX

## TODO

Design a scheduler to call and fetch results from YouTube and design API routes to view the recorded data.

## Environment Configuration

- I have shared `env.example` in the repo and will be attaching the actual env for the user to run the project.
- Have also added some fake YouTube API keys in the actual supplied env so as to test the key rotation feature bonus point of the assignment.

## Running the Project

To run the project, the user must have Docker installed on their system. The project can be run simply by running:
```docker-compose up```

The API container might fail twice or thrice at the beginning as it is creating the initial configuration for PostgreSQL.

## API Suites

I have built 2 API suites:
1. One to manage the cron scheduler.
2. One to fetch the data (along with search API).

I have added print statements to monitor the flow of the project.

## Final Note

YouTube API has a known issue with `publishedAfter`, and I am getting to see very old data.

Issue link: [GitHub Issue](https://github.com/googleapis/google-api-nodejs-client/issues/454)
