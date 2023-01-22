from .fetch import profile

class FetchFeaturedClient:
  async def get_profile(self, user_id):
    profile(self.headers, user_id)

  async def followers(self):
    pass
