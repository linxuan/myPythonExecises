import csv
import time


import requests
from fake_useragent import UserAgent
from lxml import etree


def get_page_source(lk):
    ua = UserAgent()
    header = {
        "user-agent": ua.random
    }
    return requests.get(url=lk, headers=header)


def get_data(text):
    tree = etree.HTML(text)
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
    return d


def save_result(it):
    global FILENAME, NUMBER_SUCCESS, NUMBER_FAIL
    i = 0
    for _ in it.values():
        if _ == '':
            i += 1
    if i == len(it):
        print('空数据，丢弃！')
        NUMBER_FAIL += 1
    else:
        with open(FILENAME, mode='a+', newline='', encoding='utf-8') as w:
            csv.writer(w).writerow(it.values())
            print(f"写入【{it['proj']}】的相关信息...OK!")
            NUMBER_SUCCESS += 1
        w.close()

if __name__ == '__main__':
    t_start = time.time()
    page_num = input("输入要抓取的页数: ")
    FILENAME = '中标结果情况表.csv'
    NUMBER_SUCCESS = 0
    NUMBER_FAIL = 0
    with open(FILENAME, mode='w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(
            ['项目编号', '项目名称', '采购人', '代理机构', '中标金额', '中标单位',
            '评审专家', '开标信息', '资格审查情况', '符合性审查情况',
            '评分明细表']
        )
        f.close()
    print(f'结果保存在{FILENAME}文件中,开始写入：')
    for num in range(1, int(page_num) + 1):
        url = f'https://ggzyjy.wenzhou.gov.cn/wzcms/zfcgzbgg/index_{num}.htm'
        print(f'开始采集第{num}页...')
        page = get_page_source(url)
        page.encoding = 'utf-8'
        links = etree.HTML(page.text).xpath(
            "/html/body/div[@class='Wrap']/div/div""/div/ul/li/a/@href")
        for link in links:
            link = f'https://ggzyjy.wenzhou.gov.cn{link}'
            save_result(get_data(get_page_source(link).text))
        time.sleep(0.1)
    t_end = time.time()
    print(f'完成{NUMBER_SUCCESS}行数据抓取，丢弃{NUMBER_FAIL}行数据！耗时{round(t_end-t_start,2)}秒!')
