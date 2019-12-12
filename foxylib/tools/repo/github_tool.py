from github import Github

class GithubTool:
    class Config:
        TOKEN = "token"
        OWNER = "owner"
        REPOSITORY = "repo"
        BRANCH = "branch"
        TAG = "tag"

    @classmethod
    def owner(cls):
        return "proximiant"

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
        assert(token)

        return Github(token)

    @classmethod
    def j_config2repo(cls, j_config):
        github = cls.j_config2github(j_config)

        owner = cls.j_config2owner(j_config)
        repository = cls.j_config2repository(j_config)
        return github.get_repo("/".join([owner,repository]))


    @classmethod
    def release(cls, j_config):
        tag = cls.j_config2tag(j_config)
        assert(tag)

        branch = cls.j_config2branch(j_config)
        assert(branch)

        repo = cls.j_config2repo(j_config)
        j_response = repo.create_git_release(tag, tag, "", target_commitish=branch)
        return j_response