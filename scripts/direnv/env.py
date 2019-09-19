import logging
import os
from functools import reduce

from foxylib.tools.env.env_tools import EnvToolkit
from foxylib.tools.file.file_tools import FileToolkit

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*4, FILE_DIR)
ENV_DIR = REPO_DIR

logger = logging.getLogger(__name__)

def yaml_envname2kv_list(filepath_yaml, envname):
    yaml_str = FileToolkit.filepath2utf8(filepath_yaml)
    kv_list = EnvToolkit.yaml_str2kv_list(yaml_str, [envname, '_DEFAULT_'])

    logger.info({"kv_list": kv_list,
                 "filepath_yaml":filepath_yaml,
                 })

    s_env = "\n".join(["{0}={1}".format(k, v_yaml) for k, v_yaml in kv_list])
    return s_env

def main():
    logging.basicConfig(level=logging.INFO)
    envname = EnvToolkit.k2v("ENV")

    filepath_yaml = os.path.join(REPO_DIR,"config.yaml")
    filepath_dotenv = os.path.join(REPO_DIR, ".envrc")

    s_env = yaml_envname2kv_list(filepath_yaml, envname)

    FileToolkit.utf82file(s_env, filepath_dotenv)



if __name__== "__main__":
    main()
