import json
import os
import re

from github import Github


def read_json(filepath):
    """
    Read a json file as a dictionary.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    data : dict

    """
    with open(filepath, 'r') as f:
        return json.load(f)


def get_actions_input(input_name):
    """
    Get a Github actions input by name.

    Parameters
    ----------
    input_name : str

    Returns
    -------
    action_input : str

    Notes
    -----
    GitHub Actions creates an environment variable for the input with the name:

    INPUT_<CAPITALIZED_VARIABLE_NAME> (e.g. "INPUT_FOO" for "foo")

    References
    ----------
    .. [1] https://help.github.com/en/actions/automating-your-workflow-with-github-actions/metadata-syntax-for-github-actions#example

    """
    return os.getenv('INPUT_{}'.format(input_name).upper())


def parse_issue_id(branch_name):
    """
    Parse an issue id from a branch name.

    Parameters
    ----------
    brach_name : str

    Returns
    -------
    issue_id : str

    Notes
    -----
    This function assumes a branch name follows the following format:

    xxx-yyy-branch-name (e.g. FOO-123-add-test)

    where xxx represents a project name and yyy represents an issue number.

    """
    m = re.match(r'^\w+-\d+', branch_name)
    return m.group(0) if m else ''


def create_issue_link(domain, issue_id):
    """
    Create a markdown issue link from domain and issue_id.

    Parameters
    ----------
    domain : str
    issue_id : str

    Returns
    -------
    issue_link : str

    """
    url = f'https://{domain}/browse/{issue_id}'
    return f'[{issue_id}]({url})'


def main():
    # search a pull request that triggered this action
    gh = Github(os.getenv('GITHUB_TOKEN'))
    event = read_json(os.getenv('GITHUB_EVENT_PATH'))
    head_branch = event['pull_request']['head']['label']
    repo = gh.get_repo(event['repository']['full_name'])
    prs = repo.get_pulls(state='open', sort='created', head=head_branch)
    pr = prs[0]

    # create an issue link as markdown
    domain = get_actions_input('domain')
    issue_id = parse_issue_id(head_branch.split(':')[-1])
    issue_link = create_issue_link(domain, issue_id)

    # fetch existing comments to check whether or not this pull request already has the issue link
    comments = [c.body for c in pr.get_issue_comments()]

    # if the issue link found, exit with 0
    if issue_link in comments:
        print('This pull request already has issue link for {}.'.format(issue_id))
        exit(0)

    # add the issue link as comment
    pr.create_issue_comment(issue_link)


if __name__ == '__main__':
    main()
