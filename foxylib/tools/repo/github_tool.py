import requests
from github import Github

from foxylib.tools.collections.collections_tool import IterTool


class GithubTool:
    class Config:
        TOKEN = "token"
        OWNER = "owner"
        REPOSITORY = "repo"
        BRANCH = "branch"
        TAG = "tag"

    @classmethod
    def j_config2token(cls, j_config):
        return j_config[cls.Config.TOKEN]

    @classmethod
    def j_config2owner(cls, j_config):
        return j_config[cls.Config.OWNER]

    @classmethod
    def j_config2repository(cls, j_config):
        return j_config[cls.Config.REPOSITORY]

    @classmethod
    def j_config2branch(cls, j_config):
        return j_config[cls.Config.BRANCH]

    @classmethod
    def j_config2tag(cls, j_config):
        return j_config[cls.Config.TAG]

    @classmethod
    def j_config2github(cls, j_config):
        token = cls.j_config2token(j_config)
        assert (token)

        return Github(token)

    @classmethod
    def j_config2repo(cls, j_config):
        github = cls.j_config2github(j_config)

        owner = cls.j_config2owner(j_config)
        repository = cls.j_config2repository(j_config)
        return github.get_repo("/".join([owner, repository]))

    @classmethod
    def release(cls, j_config):
        tag = cls.j_config2tag(j_config)
        assert (tag)

        branch = cls.j_config2branch(j_config)
        assert (branch)

        repo = cls.j_config2repo(j_config)
        j_response = repo.create_git_release(tag, tag, "", target_commitish=branch)
        return j_response

    @classmethod
    def repo2j_pr_list(cls, token, repo, j_payload):
        url = repo.pulls_url.format(**{"/number": ""})

        headers = {
            'Content-Type': "application/json",
            'Authorization': "token {}".format(token),
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': "api.github.com",
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "64",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, json=j_payload, headers=headers)
        return response.json()

    @classmethod
    def j_pr2pull(cls, repo, j_pr):
        return repo.get_pull(j_pr["number"])


    @classmethod
    def pull2is_approved(cls, pull):
        reviews = pull.get_reviews()
        is_empty = IterTool.iter2is_empty(filter(lambda review:review.state == "APPROVED", reviews))
        return not is_empty



    # @classmethod
    # def pr_list(cls, j_config, j_parameter):
    #     repo = cls.j_config2repo(j_config)
    #     return repo.get_pulls(**j_parameter)





    # @classmethod
    # def j_config2j_headers(cls, j_config):
    #     token = cls.j_config2token(j_config)
    #     assert (token)
    #
    #     return {
    #         'Content-Type': "application/json",
    #         'Authorization': "token {}".format(token),
    #         'Accept': "*/*",
    #         'Cache-Control': "no-cache",
    #         'Host': "api.github.com",
    #         'Accept-Encoding': "gzip, deflate",
    #         'Content-Length': "148",
    #         'Connection': "keep-alive",
    #         'cache-control': "no-cache"
    #     }

    # @classmethod
    # def j_config2url_base(cls, j_config):
    #     g = Github("user", "password")
    #
    #     owner = cls.j_config2owner(j_config)
    #     repo = cls.j_config2repo(j_config)
    #
    #     return "https://api.github.com/repos/{}/{}".format(owner, repo)

    # @classmethod
    # def release(cls, j_config):
    #     j_headers = cls.j_config2j_headers(j_config)
    #
    #     tag = cls.j_config2tag(j_config)
    #     assert (tag)
    #
    #     branch = cls.j_config2branch(j_config)
    #     assert (branch)
    #
    #     url_base = cls.j_config2url_base(j_config)
    #     url = "/".join([url_base,"releases"])
    #
    #
    #     j_payload = {"tag_name": version,
    #                  "target_commitish": branch,
    #                  "name": version,
    #                  "body": "Release",
    #                  "draft": False,
    #                  "prerelease": False,
    #                  }
    #
    #     response = requests.request("POST", url, json=j_payload, headers=j_headers)
    #     return response

    # @classmethod
    # def j_release2is_success(cls, j_release):
    #     return bool(jdown(j_release, ["created_at"]))


    # @classmethod
    # def pr_list(cls, j_config, j_parameter):
    #     url_base = cls.j_config2url_base(j_config)
    #     url = "?".join(["/".join([url_base, "pulls"]),
    #                     urllib.parse.urlencode(j_parameter),
    #                     ])
    #
    #     j_headers = cls.j_config2j_headers(j_config)
    #     response = requests.request("GET", url, headers=j_headers)
    #     return response

    # """ PUT /repos/:owner/:repo/pulls/:pull_number/merge """
    # @classmethod
    # def pr_number2merge(cls, j_config, pull_number):
    #     url_base = cls.j_config2url_base(j_config)
    #     url = "/".join([url_base, "pulls", pull_number])
    #
    #     j_headers = cls.j_config2j_headers(j_config)
    #     response = requests.request("PUT", url, headers=j_headers)
    #     return response



