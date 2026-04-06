#!/usr/bin/env python3
"""
MTProto Proxy для Telegram на Render
"""

import asyncio
import os
import sys

HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 8080))

# Telegram серверы
TG_SERVERS = [
    ('149.154.175.50', 443),
    ('149.154.175.100', 443),
    ('91.108.56.130', 443),
]

async def handle_client(reader, writer):
    try:
        # Подключаемся к Telegram
        tg_host, tg_port = TG_SERVERS[0]
        tg_reader, tg_writer = await asyncio.open_connection(tg_host, tg_port)
        
        async def forward(src, dst):
            try:
                while True:
                    data = await src.read(4096)
                    if not data:
                        break
                    dst.write(data)
                    await dst.drain()
            except:
                pass
            finally:
                try:
                    dst.close()
                except:
                    pass
        
        # Двусторонняя пересылка
        await asyncio.gather(
            forward(reader, tg_writer),
            forward(tg_reader, writer)
        )
    except Exception as e:
        print(f"Error: {e}", flush=True)
    finally:
        try:
            writer.close()
        except:
            pass

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"MTProto Proxy running on port {PORT}", flush=True)
    
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
