import aiofiles

async def read_token() -> str:
    async with aiofiles.open('.env', 'r') as token_file:
        lines = await token_file.readlines()
        token = lines[0].strip()  
        return token
