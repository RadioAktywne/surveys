from asyncio import Future


class Read(Future):
    """A read lock is compatible with other read locks, but not with write locks."""

    @staticmethod
    def is_compatible(holds):
        return not holds[Write]


class Write(Future):
    """A write lock is compatible with neither read nor write locks."""

    @staticmethod
    def is_compatible(holds):
        return not holds[Read] and not holds[Write]
