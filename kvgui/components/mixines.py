class MapIdsMixine:

    def init_ui(self):
        if hasattr(self, 'ids'):
            def map_id(uid, obj, i=0):
                if not hasattr(self, uid):
                    obj.id = uid
                    self.__setattr__(uid, obj)
                elif not hasattr(self, f'{uid}_{i}'):
                    obj.id = f'{uid}_{i}'
                    self.__setattr__(f'{uid}_{i}', obj)
                else:
                    map_id(f'{uid}_', obj, i+1)

            for uid, obj in self.ids.items():
                map_id(uid, obj)
