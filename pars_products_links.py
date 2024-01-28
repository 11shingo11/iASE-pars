import urllib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


cookies = {
    'uc|GXj83XOdm|s-0': 'oblP60NVHBW|1|J39GyuWQq|1|nGKcQgAF|1|BJ_ocNjds-X|1|r1HocEjOiWm|1|BJ59EidsWQ|1|7mOrpUraa|1|PrLTkYnq|1|YLJp7oa1I|1|uQiyefbRi|1|8eIqa_sKr|1|F-REmjGq7|1|_YzvH8nm2|1|HkIVcNiuoZX|1|S1MLTlkEX|1|BJf5EjOi-X|1|rH1vNPCFR|1|S1hmcVouiZm|1|_SBGD5koD|1|Xl0HIOViY|1|BkZ_qViOj-7|1|S1kgcNo_j-m|1|MG6mo4hTJ|1|yLsP4len5|1|HJMSxqVj_ibm|1|UkROORpAd|1|N2vwT-gQn|1|Cf2NHO6q5|1|N5uvpK-j|1|gMYO_vhh|1|_P8Dj4_id|1|H1GSqEodjZX|1|HkPBYFofN|1|S1pcEj_jZX|1|BkWrc4j_s-Q|1|sZAqOmbXv|1|BJz7qNsdj-7|1|HyldcVsOo-m|1|0XIfeH9qx|1|LNZGBYJCq|1|Sy1naC5nN|1|65JrtAVaP|1|tnfBi7gwe|1|SkEscVsusbX|1|0V-E5N_GQ|1|BJTzqNi_i-m|1|SyUQ54odobQ|1|U8QkTd2W|1|ctDbl6j2y|1|j7Igy6o8D|1|H1PKqNodoWQ|1|Sy7BcNo_ib7|1|XYQZBUojc|1|9V8bg4D63|1|S1_9Vsuj-Q|1|rJJjcVouoZ7|1|JQ2XQxIk|1|Hkx754i_iWm|1|HkMucNoOjWX|1|ByBFq4idoZQ|1|r144c4odsbm|1|BgFFtPqMi|1|HkocEodjb7|1|gkEBFID-V|1|d_5HNF7Yc|1|Skj79NodobQ|1|Sk9kb5VoOi-7|1|0vHbD98mH|1|B1NA5VjdjbX|1|rJ99c4oOo-X|1|SkPc5EjOsWm|1|dsS7z9Hv4|1|r1EWc4iuj-X|1|rkqVqNoOib7|1|rkBBg94sdiW7|1|O97xcRJFR|1|M9Nj9klGy|1|rkT1x5Eo_ibm|1|H1dDqVjOjWX|1|a2XkayMLT|1|BJmZ9Nids-m|1|Hx4zBfT2s69AbN|1',
    'uc|v': '3',
    'ste_vi': 'vi_fv%3A1677133619336%7Cvi%3Ade80d7b65189f7be5c42f62ec27eb53f',
    'uc|hasinteracted': '1678130651108',
    'uc|GXj83XOdm|m': 'c|c3ce320b04e16f25294ee49e5d0745ad79d3fa3e2f27456be0f4cc6b29b58875|i|GXj83XOdm|l|de|v|127.39.327',
    'ASP.NET_SessionId': 'e4kkadhfhmcdw05ltaknx2xx',
    'RegionUrl': '/ru',
    'mall-tn': 'E250B82829DE2D483A05B3DF80171646|CatalogTree',
    'mall-us': 'E250B82829DE2D483A05B3DF80171646|EUR|',
    'checkBrowserCookies': 'set',
    'bm_mi': '77C1EBBC23E0E2375A8344DB0EE8AD32~YAAQlQVJFyqL/0aNAQAAlbfTSRYLkvWMS9kXBNsNpGdKkFpxc/9C4vqXBXqrotsoKUQ6UTebOFggSOf7Or8ZbrES0hSyJMD4ylyIc/+89s8AUeQM4FCNPHtQptFi0b0n2Nji4qTicZsZSgErStkGKMKYVcYGQtvYhhqhtHPpHyx1MR+KKvkNQdwQpI+U4Q3S8cRl4E67oS4yc8T8bflg2qemXaaoJe/kQofSZzJdittaihfMDNF7jLlcPZgFJBDU4dHp9Fa41Ep6trKYbZD5XKJB4ytjzauwFUvebSKp5wg8U4Q667nLBWstG6GQsGPeAgDmJZFQlJdUvPbnxCEDHDpHn66VRkiAXhtY16p8+rabsiNleyLu2kZGIcRQcOw=~1',
    'ak_bmsc': '4E47DF1E2F96A0192F5555458E61C93E~000000000000000000000000000000~YAAQlQVJF06L/0aNAQAAabrTSRbzDWl0/NP5EewirKKeI8WFkkJpGD6BN8osP62Olbe9yq8Z1xxwBR0MVr8fKCevxEyQEqDmLd5TNJ4TvAcKAPciCNyaLmTN12YkdHFFzOaYUcWagxsu3GtmZ3HgiczCzuHy/ilXPXQ1EH3gLirGGSiANDG701dwLukuSrlpGCDamdrI3CfkyCWuZzGH3zUBTIJVwjrvV+Z9KymvDlUdooOaxchmciy2bjOj3ecmIlUmd/xC0jtlsQ6F5NnUmrLMvnxzQY/cfvVfDBuaQkIsrO1NPd/NZuimO/K6BzKgCvbqQnGpS4xPBCWkfpJbzBx055F4Q5YezyQOL55rz5hbLRkNzUoEbdDyH3Ge3Oa4L/RPYdFbykWqUbsBV5lyPBw50p+omX1Wei9VtEkcXlUIHMsDKY5oyuTQw86umpiT4scla0R0SwNPW5f13z85qeaM6Sv6X3uMKcbdKl+rkyPnbozlLpxXqAegWRFaUOvZkWEFQtCgRi5tf3i9dgLqJ97CjMOxGfx2uD375Ka9wRpL7Eyr7+6yo8m/Diy6VIk=',
    'ak_bmsc': '37C528442E021B1419A07CAAAE5DBAC2~000000000000000000000000000000~YAAQlQVJF4GL/0aNAQAA8L7TSRY4fpUnbXjzWZE10o3a/La0vKd7HOGh3Fu0WI0nVHXQ5gSBD6muHMXlShvv0E7VvTF/+EHfQCvgpRUqYviCm9V0gUn4msWYBgCMdHMVkMaI2TjuN0wEDVDRAUy1CyE8wI21WKGf1ZZy8pzilp4JLypNBzpY+aAuMyGzOYyKNC9U78sglg+lvqkOfmIRIv80vo0iLCBKhuJwbNDQ4yBwksVEU3ZUi3uCcONMCTRobnnawr+osr7upEsHvaLLPvivraXen2eO26tHSqFsT5zwuUaURKcV/nGI092VFXnNuCo0Zj6laIWRbal6uvMQrMY4WmXDRcsh2h+Z1MEXp9VuufRhH2GAUdqIajDdzDRobmeZriBo1z4W5V3nosQElpNyfwM4TsOSlP1K4RkBmJx7FcNsTEoiz7sMUW5AnMB6r/V3741EoH4Nh5fOM361KbUBLm3dixT1KR1sIzioHfYuUOztYatnb0gcEbjdBtHjFnhL53TPVkLAXxgC10fFDhZdxbL2eAdO0sn10kjMqIKdyAhv8prk8QcKvfennTsD2XfZcPT2CouZGZMN6xdo/Bk=',
    '.ASPXAUTH': 'DB998A40F72189D0584627C29E9DC0957DD49BFD8C055A865EB4AFC95E2C6EBCA1CDB3979994BE8BD35FA3B73EE7104030607D123C43FD370F03A731575591B0896682C5FC8DD648710720C3DDD7459E3A17E9EB628C750F5BB00F88F4AACE02648E05C868B27A57B474834E97F8E8A40714D8EFE2EC7404FFFA3FA35911DE014C93F211',
    'mall-sd': '5350a608-4690-4abc-ba04-99e37d8007d5',
    'bm_sv': 'F93B5B073BF57EC286E7F8197408EEAA~YAAQlQVJF4GEAUeNAQAAwYHwSRbBq3yIEotaLYGBfvIVjXs5B3OpdXzbKd9FPAGo5zlIfJPkvN6YusL9iXSqIkLFi5xIJaIWdZzBSXC2lQ04dZSo2ZSryYEZtBfCdec1lau+ybqlkmOVhNBgFkD8fTSHP7zwi2lTCO0nWRkQo3KOxpxM+qTIvjgPnAnUv0YIiqKrHyqoZVQPM/7XH3G2Gxj25udv835ylGHsaiQg1cBUGVyFyPKcTXE1/ADwi6rI9tZ3JOxtog9bfko=~1',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    # 'Cookie': 'uc|GXj83XOdm|s-0=oblP60NVHBW|1|J39GyuWQq|1|nGKcQgAF|1|BJ_ocNjds-X|1|r1HocEjOiWm|1|BJ59EidsWQ|1|7mOrpUraa|1|PrLTkYnq|1|YLJp7oa1I|1|uQiyefbRi|1|8eIqa_sKr|1|F-REmjGq7|1|_YzvH8nm2|1|HkIVcNiuoZX|1|S1MLTlkEX|1|BJf5EjOi-X|1|rH1vNPCFR|1|S1hmcVouiZm|1|_SBGD5koD|1|Xl0HIOViY|1|BkZ_qViOj-7|1|S1kgcNo_j-m|1|MG6mo4hTJ|1|yLsP4len5|1|HJMSxqVj_ibm|1|UkROORpAd|1|N2vwT-gQn|1|Cf2NHO6q5|1|N5uvpK-j|1|gMYO_vhh|1|_P8Dj4_id|1|H1GSqEodjZX|1|HkPBYFofN|1|S1pcEj_jZX|1|BkWrc4j_s-Q|1|sZAqOmbXv|1|BJz7qNsdj-7|1|HyldcVsOo-m|1|0XIfeH9qx|1|LNZGBYJCq|1|Sy1naC5nN|1|65JrtAVaP|1|tnfBi7gwe|1|SkEscVsusbX|1|0V-E5N_GQ|1|BJTzqNi_i-m|1|SyUQ54odobQ|1|U8QkTd2W|1|ctDbl6j2y|1|j7Igy6o8D|1|H1PKqNodoWQ|1|Sy7BcNo_ib7|1|XYQZBUojc|1|9V8bg4D63|1|S1_9Vsuj-Q|1|rJJjcVouoZ7|1|JQ2XQxIk|1|Hkx754i_iWm|1|HkMucNoOjWX|1|ByBFq4idoZQ|1|r144c4odsbm|1|BgFFtPqMi|1|HkocEodjb7|1|gkEBFID-V|1|d_5HNF7Yc|1|Skj79NodobQ|1|Sk9kb5VoOi-7|1|0vHbD98mH|1|B1NA5VjdjbX|1|rJ99c4oOo-X|1|SkPc5EjOsWm|1|dsS7z9Hv4|1|r1EWc4iuj-X|1|rkqVqNoOib7|1|rkBBg94sdiW7|1|O97xcRJFR|1|M9Nj9klGy|1|rkT1x5Eo_ibm|1|H1dDqVjOjWX|1|a2XkayMLT|1|BJmZ9Nids-m|1|Hx4zBfT2s69AbN|1; uc|v=3; ste_vi=vi_fv%3A1677133619336%7Cvi%3Ade80d7b65189f7be5c42f62ec27eb53f; uc|hasinteracted=1678130651108; uc|GXj83XOdm|m=c|c3ce320b04e16f25294ee49e5d0745ad79d3fa3e2f27456be0f4cc6b29b58875|i|GXj83XOdm|l|de|v|127.39.327; ASP.NET_SessionId=e4kkadhfhmcdw05ltaknx2xx; RegionUrl=/ru; mall-tn=E250B82829DE2D483A05B3DF80171646|CatalogTree; mall-us=E250B82829DE2D483A05B3DF80171646|EUR|; checkBrowserCookies=set; bm_mi=77C1EBBC23E0E2375A8344DB0EE8AD32~YAAQlQVJFyqL/0aNAQAAlbfTSRYLkvWMS9kXBNsNpGdKkFpxc/9C4vqXBXqrotsoKUQ6UTebOFggSOf7Or8ZbrES0hSyJMD4ylyIc/+89s8AUeQM4FCNPHtQptFi0b0n2Nji4qTicZsZSgErStkGKMKYVcYGQtvYhhqhtHPpHyx1MR+KKvkNQdwQpI+U4Q3S8cRl4E67oS4yc8T8bflg2qemXaaoJe/kQofSZzJdittaihfMDNF7jLlcPZgFJBDU4dHp9Fa41Ep6trKYbZD5XKJB4ytjzauwFUvebSKp5wg8U4Q667nLBWstG6GQsGPeAgDmJZFQlJdUvPbnxCEDHDpHn66VRkiAXhtY16p8+rabsiNleyLu2kZGIcRQcOw=~1; ak_bmsc=4E47DF1E2F96A0192F5555458E61C93E~000000000000000000000000000000~YAAQlQVJF06L/0aNAQAAabrTSRbzDWl0/NP5EewirKKeI8WFkkJpGD6BN8osP62Olbe9yq8Z1xxwBR0MVr8fKCevxEyQEqDmLd5TNJ4TvAcKAPciCNyaLmTN12YkdHFFzOaYUcWagxsu3GtmZ3HgiczCzuHy/ilXPXQ1EH3gLirGGSiANDG701dwLukuSrlpGCDamdrI3CfkyCWuZzGH3zUBTIJVwjrvV+Z9KymvDlUdooOaxchmciy2bjOj3ecmIlUmd/xC0jtlsQ6F5NnUmrLMvnxzQY/cfvVfDBuaQkIsrO1NPd/NZuimO/K6BzKgCvbqQnGpS4xPBCWkfpJbzBx055F4Q5YezyQOL55rz5hbLRkNzUoEbdDyH3Ge3Oa4L/RPYdFbykWqUbsBV5lyPBw50p+omX1Wei9VtEkcXlUIHMsDKY5oyuTQw86umpiT4scla0R0SwNPW5f13z85qeaM6Sv6X3uMKcbdKl+rkyPnbozlLpxXqAegWRFaUOvZkWEFQtCgRi5tf3i9dgLqJ97CjMOxGfx2uD375Ka9wRpL7Eyr7+6yo8m/Diy6VIk=; ak_bmsc=37C528442E021B1419A07CAAAE5DBAC2~000000000000000000000000000000~YAAQlQVJF4GL/0aNAQAA8L7TSRY4fpUnbXjzWZE10o3a/La0vKd7HOGh3Fu0WI0nVHXQ5gSBD6muHMXlShvv0E7VvTF/+EHfQCvgpRUqYviCm9V0gUn4msWYBgCMdHMVkMaI2TjuN0wEDVDRAUy1CyE8wI21WKGf1ZZy8pzilp4JLypNBzpY+aAuMyGzOYyKNC9U78sglg+lvqkOfmIRIv80vo0iLCBKhuJwbNDQ4yBwksVEU3ZUi3uCcONMCTRobnnawr+osr7upEsHvaLLPvivraXen2eO26tHSqFsT5zwuUaURKcV/nGI092VFXnNuCo0Zj6laIWRbal6uvMQrMY4WmXDRcsh2h+Z1MEXp9VuufRhH2GAUdqIajDdzDRobmeZriBo1z4W5V3nosQElpNyfwM4TsOSlP1K4RkBmJx7FcNsTEoiz7sMUW5AnMB6r/V3741EoH4Nh5fOM361KbUBLm3dixT1KR1sIzioHfYuUOztYatnb0gcEbjdBtHjFnhL53TPVkLAXxgC10fFDhZdxbL2eAdO0sn10kjMqIKdyAhv8prk8QcKvfennTsD2XfZcPT2CouZGZMN6xdo/Bk=; .ASPXAUTH=DB998A40F72189D0584627C29E9DC0957DD49BFD8C055A865EB4AFC95E2C6EBCA1CDB3979994BE8BD35FA3B73EE7104030607D123C43FD370F03A731575591B0896682C5FC8DD648710720C3DDD7459E3A17E9EB628C750F5BB00F88F4AACE02648E05C868B27A57B474834E97F8E8A40714D8EFE2EC7404FFFA3FA35911DE014C93F211; mall-sd=5350a608-4690-4abc-ba04-99e37d8007d5; bm_sv=F93B5B073BF57EC286E7F8197408EEAA~YAAQlQVJF4GEAUeNAQAAwYHwSRbBq3yIEotaLYGBfvIVjXs5B3OpdXzbKd9FPAGo5zlIfJPkvN6YusL9iXSqIkLFi5xIJaIWdZzBSXC2lQ04dZSo2ZSryYEZtBfCdec1lau+ybqlkmOVhNBgFkD8fTSHP7zwi2lTCO0nWRkQo3KOxpxM+qTIvjgPnAnUv0YIiqKrHyqoZVQPM/7XH3G2Gxj25udv835ylGHsaiQg1cBUGVyFyPKcTXE1/ADwi6rI9tZ3JOxtog9bfko=~1',
    'Origin': 'https://mall.industry.siemens.com',
    'Pragma': 'no-cache',
    'Referer': 'https://mall.industry.siemens.com/mall/en/ru/Catalog/Products/10303433?tree=CatalogTree',
    'RequestVerificationToken': 'wckriXEXKbId2SQKYSk-taJV0FL5TtZ_G3dBdIxfSKyUr-r2ri3uFfn3x-3qy8Dx-7TU-qe1Kj8hM9yd3vmjAZUwxCA1:RFpshfhfMSEGvinl4CMLc4wrB9DZW4JVFIcgTLBMpcMeLE55GJcFWLsXGyaqjWhUYOZvVGxI7SAYf1Ws_YYkb8CiPr41',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}



# перебираем ссылки
with open("catalog_links.txt", "r") as file:
    products = file.readlines()
base_url= [line.strip().rstrip(',') for line in products]

for url in base_url:
# вычленяем номер продуктов из ссылки
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if 'tree' in query_params:
        del query_params['tree']
    product_number = parsed_url.path.split("/")[-1]
    print(product_number)

    json_data = {
        'nodeId': product_number,
        'page': 1,
        'filters': {
            'InitialLoad': True,
            'IsTechnicalSelectorsAvailable': False,
            'Selectors': [],
            'ShowWaitControl': True,
            'TechnicalSelectorVisible': True,
            'IsAccessories': False,
        },
        'treeName': 'CatalogTree',
        'isAccessories': False,
    }

    response = requests.post(
        'https://mall.industry.siemens.com/mall/Catalog/GetProducts/ProductsOrAccessories',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    # print(response.json()['HtmlContent'])
    soup = BeautifulSoup(response.json()['HtmlContent'], "lxml")
    products = soup.find_all('a', class_="internalLinkMultiLines")
    for product in products:
        print(product.get('href'))
        
