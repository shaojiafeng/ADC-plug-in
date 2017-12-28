from crm import models


class XXX(object):
    users = None # [1,2,1,2,3,1,...]
    iter_users = None # iter([1,2,1,2,3,1,...])
    reset_status = False

    @classmethod
    def fetch_users(cls):
        # [obj(销售顾问id,num),obj(销售顾问id,num),obj(销售顾问id,num),obj(销售顾问id,num),]
        sales = models.SaleRank.objects.all().order_by('-weight')

        # v = [短期, 番禺, 富贵, 秦晓, 短期, 番禺, 富贵, 秦晓, 番禺, 富贵, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓...]
        v = []
        cls.users = v

    @classmethod
    def get_sale_id(cls):
        if not cls.users:
            cls.fetch_users()
        if not cls.iter_users:
            cls.iter_users = iter(cls.users)
        try:
            user_id = next(cls.iter_users)
        except StopIteration as e:
            if cls.reset_status:
                cls.fetch_users()
                cls.reset_status = False
            cls.iter_users = iter(cls.users)
            user_id = cls.get_sale_id()
        return user_id

    @classmethod
    def reset(cls):
        cls.reset_status = True