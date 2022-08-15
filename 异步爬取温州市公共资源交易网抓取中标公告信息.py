import asyncio
import csv
import time
from concurrent.futures import ThreadPoolExecutor

import aiofiles
import aiohttp
import requests
from fake_useragent import UserAgent
from lxml import etree


async def aio_get_content(url):
    global FILENAME, NUMBER_SUCCESS, NUMBER_FAILED
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            tree = etree.HTML(await resp.text())
            proj_id = tree.xpath(
                "/html/body/div[2]/div[3]/div/div[2]/div[2]/p[1]/span/span/text()")
            proj = tree.xpath(
                "/html/body/div[2]/div[3]/div/div[2]/div[2]/p[2]/span/text()")
            price = tree.xpath(
                "/html/body/div[2]/div[3]/div/div[2]/div[2]/div[1]/table[1]/tbody/tr/td[2]/text()")
            supplier = tree.xpath(
                "/html/body/div[2]/div[3]/div/div[2]/div[2]/div[1]/table[1]/tbody/tr/td[3]/text()")
            judges = tree.xpath(
                "/html/body/div[2]/div[3]/div/div[2]/div[2]/div[2]/p[3]/span/samp/text()")
            kbqk = tree.xpath(
                "/html/body/div[2]/div[3]/div/div[2]/div[2]/div[2]/p[6]/samp/a/@href")
            zgsc = tree.xpath(
                "/html/body/div[2]/div[3]/div/div[2]/div[2]/div[2]/p[8]/samp/a/@href")
            fhxsc = tree.xpath(
                "/html/body/div[2]/div[3]/div/div[2]/div[2]/div[2]/p[10]/samp/a/@href")
            pf = tree.xpath(
                "/html/body/div[2]/div[3]/div/div[2]/div[2]/div[2]/p[14]/samp/a/@href")
            buyer = tree.xpath(
                "/html/body/div[2]/div[3]/div/div[2]/div[2]/div[3]/p[2]/span/span/text()")
            agent = tree.xpath(
                "/html/body/div[2]/div[3]/div/div[2]/div[2]/div[3]/p[11]/span/span/text()")
            if len(proj_id) == 0:
                proj_id.append('')
            if len(proj) == 0:
                proj.append('')
            if len(buyer) == 0:
                buyer.append('')
            if len(agent) == 0:
                agent.append('')
            if len(price) == 0:
                price.append('')
            if len(supplier) == 0:
                supplier.append('')
            if len(judges) == 0:
                judges.append('')
            if len(kbqk) == 0:
                kbqk.append('')
            if len(zgsc) == 0:
                zgsc.append('')
            if len(fhxsc) == 0:
                fhxsc.append('')
            if len(pf) == 0:
                pf.append('')
            d = {}
            d['proj_id'] = proj_id[0]
            d['proj'] = proj[0]
            d['buyer'] = buyer[0]
            d['agent'] = agent[0]
            d['price'] = price[0]
            d['supplier'] = supplier[0]
            d['judges'] = judges[0]
            d['kbqk'] = kbqk[0]
            d['zgsc'] = zgsc[0]
            d['fhxsc'] = fhxsc[0]
            d['pf'] = pf[0]

            async with aiofiles.open(FILENAME, mode='a+', newline='', encoding='utf-8') as w:
                i = 0
                for _ in d.values():
                    if _ == '':
                        i += 1
                if i == len(d):
                    NUMBER_FAILED += 1
                else:
                    await csv.writer(w).writerow(d.values())
                    NUMBER_SUCCESS += 1


def get_page_source(url):
    ua = UserAgent()
    header = {
        "user-agent": ua.random
    }
    return requests.get(url=url, headers=header)


def get_target_page_urls(url):
    global TARGET_PAGE_URLS
    target_page = get_page_source(url)
    target_page.encoding = 'utf-8'
    target_page_url = etree.HTML(target_page.text).xpath(
        "/html/body/div[@class='Wrap']/div/div""/div/ul/li/a/@href")
    for _ in target_page_url:
        TARGET_PAGE_URLS.append(f'https://ggzyjy.wenzhou.gov.cn{_}')


if __name__ == "__main__":
    t_start = time.time()
    
    NUMBER_SUCCESS = 0
    NUMBER_FAILED = 0
    
    FILENAME = '结果情况表.csv'
    with open(FILENAME, mode='w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(['项目编号', '项目名称', '采购人', '代理机构', '中标金额',
                                '中标单位', '评审专家', '开标信息', '资格审查情况', '符合性审查情况', '评分明细表'])
    f.close()
    
    page_num = int(input("输入要抓取的页数: "))
    list_page_urls = [
        f'https://ggzyjy.wenzhou.gov.cn/wzcms/zfcgzbgg/index_{num}.htm' for num in range(1, page_num + 1)]
    
    TARGET_PAGE_URLS = []
    with ThreadPoolExecutor(20) as thread:
        for list_page_url in list_page_urls:
            thread.submit(get_target_page_urls, url=list_page_url)
            
    tasks = []
    for target_page_url in TARGET_PAGE_URLS:
        tasks.append(aio_get_content(target_page_url))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    
    t_end = time.time()
    print(f'完成{NUMBER_SUCCESS}行数据抓取，失败{NUMBER_FAILED}行！运行耗时{round(t_end-t_start,2)}秒!')