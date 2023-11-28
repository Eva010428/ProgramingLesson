# -*- coding: utf-8 -*-
import time
import asyncio



async def washing1():
    await asyncio.sleep(1)
    print('washer1 finished')

async def washing2():
    await asyncio.sleep(4)
    print('washer2 finished')

async def washing3():
    await asyncio.sleep(3)
    print('washer3 finished')

async def main():
    await asyncio.gather(washing1(),washing2(),washing3())

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print('AsyncWashingMachine Consumption : {}'.format(end_time-start_time))
