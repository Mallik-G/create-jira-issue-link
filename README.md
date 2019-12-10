# Create Jira issue link

GitHub action to create a Jira issue link on pull reqests.

## Usage

```yml
uses: harupy/create-jira-issue-link@master
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
with:
  domain: example.atlassian.net
```

## Example

[workflow](./.github/workflows/example.yml)
[pull request](https://github.com/harupy/create-jira-issue-link/pull/1)
