import requests

__our_session = "empty"
__verify = True

"""Vendor list harvested from the javascript on the GSA EIS WebPage.  These codes enable us to decode responses"""
__Vendors = ["v5_att", "v6_verizon", "v8_level3", "v12_centurylink", "v23_harris", "v53_btfederal", "v71_mettel",
             "v72_granite", "v73_coretech", "v76_microtech"]

"""Request Headers to use"""
__myHeaders = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "DNT": "1",
    "Host": "eis-public-pricer.nhc.noblis.org",
    "Pragma": "no-cache",
    "Referer": "https://eis-public-pricer.nhc.noblis.org/unit-pricer/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
    "X-Requested-With": "XMLHttpRequest"
}


# retrieve base page to establish session key
def __getBaseWebPage():
    global __verify
    global __our_session
    return __our_session.get("https://eis-public-pricer.nhc.noblis.org/unit-pricer/", verify=__verify)


def __SetSession():
    global __our_session
    __our_session = requests.session()
    __our_session.headers.update(__myHeaders)
    __getBaseWebPage()
    return


def __getSession():
    global __our_session
    if (__our_session == "empty"):
        __SetSession()
    return __our_session


# ===========================================================================================================
# verify the CLIN is good
def VerifyCLINData(clinCode):
    global __verify
    our_session = __getSession()
    query_str = "service_id=all&q=" + clinCode + "&page=1&sort=name"
    response = our_session.post("https://eis-public-pricer.nhc.noblis.org/ajax.php/clin-search/search", query_str,
                                verify=__verify)
    return response.text


# verify NSC is good
def VerifyNSCData(nscCode):
    global __verify
    our_session = __getSession()
    query_str = "type=80&q=" + nscCode
    response = our_session.post("https://eis-public-pricer.nhc.noblis.org/ajax.php/unit-pricer/get_locs", query_str,
                                verify=__verify)
    return response.text


# get the price infor to a particluar CLLI/NSC combo (currently only domestic)
def GetPriceData(clinCode, nscCode, service_id, btable_id, dates):
    global __verify
    our_session = __getSession()
    query_str = "service_id=" + service_id + "&clin=" + clinCode + "&btable_id=" + btable_id + "&loc_orig=" + nscCode + "&dates=" + dates
    response = our_session.post("https://eis-public-pricer.nhc.noblis.org/ajax.php/unit-pricer/price", query_str,
                                verify=__verify)
    return response.text


# retrieve vendor list
def getVendors():
    return __Vendors


# setSSLVerify
def set_ssl_verify(required_tf):
    global __verify
    __verify = required_tf
    return
