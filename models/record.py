import path.structure


class MediaCenterRecord(path.structure.MediaCenterPath):
    def __init__(self, mpath, mtype):
        super().__init__(mpath, mtype, True)
