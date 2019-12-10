# Create Jira issue link

GitHub Actions to create a Jira issue link on pull reqests.

## Usage

```yml
uses: harupy/create-jira-issue-link@master
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
with:
  domain: example.atlassian.net
```

## Example

[example](./.github/workflows/example.yml)
