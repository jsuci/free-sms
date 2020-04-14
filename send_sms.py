from cfscrape import create_scraper, Session, HTTPAdapter
from fake_useragent import UserAgent
from urllib3.util.retry import Retry
from requests_html import HTML
from urllib.parse import urlparse, urlencode, quote_plus
from pathlib import Path
from PIL import Image
from io import BytesIO
from time import time_ns, sleep


def fetch_r(p):
    f_path = Path(p.hostname)
    c_path = Path("cookies")

    cf_sess = Session()
    retries = Retry(total=5, backoff_factor=1)
    cf_sess.mount(p.scheme, HTTPAdapter(max_retries=retries))
    cf = create_scraper(sess=cf_sess)

    ua = UserAgent().random
    headers = {"User-Agent": ua}

    r = cf.get(p.geturl(), headers=headers)

    print(r.headers)

    html = HTML(html=r.content)
    html.render()

    doc = html
    cookies = r.cookies

    with open(f_path, "w", encoding="utf-8") as fd:
        fd.write(doc.html)

    return (doc, cookies, cf)


def send_sms():

    def make_absolute(qs, p):
        return f"{p.scheme}://{p.netloc}{qs}"

    def show_captcha(img_url, ua):
        cf = create_scraper()
        headers = {
            "User-Agent": ua
        }
        r = cf.get(img_url, headers=headers)

        img = Image.open(BytesIO(r.content))
        img.show()

        return (r.cookies, r.headers["Set-Cookie"])

    p = urlparse("http://www.afreesms.com/intl/philippines")
    url = f"{p.scheme}://{p.hostname}"
    ua = UserAgent().random
    headers = {"User-Agent": ua}

    cf_sess = Session()
    retries = Retry(total=5, backoff_factor=1)
    cf_sess.mount(p.scheme, HTTPAdapter(max_retries=retries))
    cf = create_scraper(sess=cf_sess)

    r = cf.get(p.geturl(), headers=headers)
    cookies = r.cookies

    html = HTML(html=r.content)
    html.render()
    doc = html

    captcha = doc.xpath("//td//img[@id='captcha']", first=True).attrs["src"]
    img_url = make_absolute(captcha, p)

    # u_phone = input("Enter 10-digit #: ")
    u_phone = "9754238175"
    # u_message = input("Enter message (160 chars): ")
    u_message = "hellllllllllllooooooo worllldddddd"

    new_cookies, new_set_cookie = show_captcha(img_url, ua)

    u_captcha = input("Enter captcha: ")

    tag = doc.xpath("//input[@class='IL_OPTIMIZED']", first=True).attrs
    prefix = doc.xpath("//input[@value='63']", first=True).attrs
    number = doc.xpath("//input[@type='text']", first=True).attrs["name"]
    message = doc.xpath("//textarea", first=True).attrs["name"]
    msg_len = 160

    code = doc.xpath(
        "//td[@valign='top'][@colspan='2']/input", first=True).attrs["name"]

    hidden = doc.xpath("//td[@colspan=2][@align='left']/input")
    c_one = hidden[0].attrs
    c_two = hidden[1].attrs

    # Construct post request
    unix_time = str(time_ns())[:13]

    args = {
        prefix["name"]: prefix["value"],
        number: u_phone,
        message: u_message,
        "msgLen": msg_len - len(u_message),
        code: u_captcha,
        c_one["name"]: c_one["value"],
        c_two["name"]: c_two["value"]
    }

    xajaxargs = quote_plus(
        f"<xjxquery><q>IL_IN_TAG=1&{urlencode(args, doseq=True)}"
        f"&IL_IN_TAG=1</q></xjxquery>"
    )

    body = {
        "xajax": "processMsg",
        "xajaxr": unix_time,
        "xajaxargs[]": xajaxargs
    }

    headers["Content-Type"] = "application/x-www-form-urlencoded"

    cf_post = cf_sess.post(p.geturl(), data=body,
                           headers=headers)

    print(cf_post.content)


def main():
    send_sms()


if __name__ == "__main__":
    main()
