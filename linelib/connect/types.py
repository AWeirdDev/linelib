class Profile:
    name: str
    id: str
    language: str
    picture_url: str
    status_message: str


class Group:
    count: int
    id: str
    name: str
    picture_url: str

    async def leave():
        """
        Leaves the group. *(New in version 2.2)*
        """
