import io
from functools import partial
from pprint import pformat

from PIL import Image
from future.utils import lmap, lrange, lfilter
from nose.tools import assert_equal

from foxylib.tools.collections.collections_tool import list2singleton, lproduct, zip_strict
from foxylib.tools.function.function_tool import f_a2t


class PillowTool:
    @classmethod
    def point_offset2move(cls, p, offset):
        return lmap(sum, zip_strict(p,offset))

    @classmethod
    def rgb_pair2dist_squared(cls, rgb1, rgb2,):
        return sum(lmap(f_a2t(lambda v1,v2: (v1-v2)**2), zip_strict(rgb1, rgb2)))

    # https://pillow.readthedocs.io/en/latest/reference/open_files.html#file-handling
    @classmethod
    def filepath2img(cls, filepath):
        with open(filepath, 'rb') as f:
            img = Image.open(io.BytesIO(f.read()))
        return img

    @classmethod
    def img2file(cls, img, filepath, format=None):
        img.save(filepath, format=format)

    @classmethod
    def img2rgb_ll(cls, img):
        l = list(img.getdata())
        assert_equal(len(l), img.width*img.height, 0)

        n_ROW,n_COL = (img.height,img.width)
        ll = [l[i*n_COL:(i+1)*n_COL]
            for i in range(n_ROW)]
        return ll

    @classmethod
    def img2chunk(cls, img, ll_ij2is_valid,):
        ll = cls.img2rgb_ll(img)
        n_ROW, n_COL = (img.height, img.width)

        f_valid = partial(ll_ij2is_valid, ll)
        ij_list_ALL = lproduct(lrange(n_COL),lrange(n_ROW))
        ij_list = lfilter(f_valid, ij_list_ALL)
        raise Exception(pformat(ij_list),)

    @classmethod
    def img2xy_list(cls, img,):
        ll = cls.img2rgb_ll(img)
        n_ROW, n_COL = (img.height, img.width)

        xy2is_valid = None

        xy_list_ALL = lproduct(lrange(n_COL), lrange(n_ROW))
        xy_list_VALID = lfilter(xy2is_valid, xy_list_ALL)
        return xy_list_VALID

    @classmethod
    def rgb_ll_rgb2xy_list(cls, rgb_ll, rgb_TARGET,):
        n_ROW, n_COL = (len(rgb_ll), list2singleton(lmap(len,rgb_ll)))

        xy_list_ALL = lproduct(lrange(n_COL), lrange(n_ROW))
        xy_list_VALID = [(x,y) for x,y in xy_list_ALL if rgb_ll[y][x] == rgb_TARGET]
        return xy_list_VALID

    @classmethod
    def point_size2bounds(cls, p, size,):
        x,y = p
        w,h = size
        return [x,y,x+w,y+h]