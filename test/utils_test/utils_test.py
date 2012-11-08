import time
import project_config

p=project_config.path_config("paths")
import utils


tmp=utils.tmp_dir_handler()
tmp.add_dir("/tmp/houde_trans","TRANS")
tmp.add_dir("/tmp/houde_pers","PERS")
time.sleep(5)

tmp.clean()


