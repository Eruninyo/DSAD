import asyncio
import httpx

TOKEN = ""  # とけん

WHITELIST = [
    1111111111111111111,
    2222222222222222222,
    3333333333333333333,
    4444444444444444444,
    5555555555555555555,
    6666666666666666666
]

DELETE_DELAY_MS = 3000  #削除間隔(ms)

HEADERS = {
    "Authorization": TOKEN,
    "User-Agent": "DiscordBot (https://discord.com, v1)"
}

async def delete_guild(client, guild_id):
    """サーバー削除（オーナーのみ可能）"""
    await asyncio.sleep(DELETE_DELAY_MS / 1000)
    url = f"https://discord.com/api/v10/guilds/{guild_id}"
    response = await client.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"{guild_id}を削除したよ！")
    else:
        print(f"{guild_id}の削除に失敗しました...: {response.status_code} - {response.text}")

async def leave_guild(client, guild_id):
    """サーバー退出（オーナーじゃない場合に使う）"""
    await asyncio.sleep(DELETE_DELAY_MS / 1000)
    url = f"https://discord.com/api/v10/users/@me/guilds/{guild_id}"
    response = await client.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"{guild_id}を抜けたよ！")
    else:
        print(f"{guild_id}の退出に失敗しました...: {response.status_code} - {response.text}")

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://discord.com/api/v10/users/@me/guilds", headers=HEADERS)
        if response.status_code != 200:
            print(f"サーバーの取得エラー: {response.status_code} - {response.text}")
            return

        guilds = response.json()
        print(f"{len(guilds)}個のサーバーに入ってるよ！")

        for guild in guilds:
            guild_id = int(guild["id"])
            if guild_id in WHITELIST:
                print(f"{guild_id}をスキップしたよ！")
                continue

            # 自分がオーナーかどうか判定
            if guild.get("owner", False):
                await delete_guild(client, guild_id)
            else:
                await leave_guild(client, guild_id)

if __name__ == "__main__":
    asyncio.run(main())