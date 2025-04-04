from app.models import HelloRequest

async def handle_hello(request: HelloRequest):
  return request.content