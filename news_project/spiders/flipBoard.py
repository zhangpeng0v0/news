import requests
import re


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
cookies = {
    'cookie': 'optimizelyEndUserId=oeu1555898913157r0.012884145836128402; _ga=GA1.2.274079488.1555898913; _gid=GA1.2.1350737489.1555898913; access_token=3097824449%7Cd7d1c63384108b77ecd679728702973e%7Cd70d91d795ac2e662ed5ea5ac84187ad; userid=3097824449; _csrfKey=oaq%2BvR8AUDy2ds0iKWNnNeXfTec%3D%7C3097824449%7ChojGkmlyKc2LJ4ybH1hk6hVirBG1JdR0EpKtrottaw6ilIdOb4%2FIGgG1PAKmUzKwtGanjMlOSeVs6GvD7akkew%3D%3D; f=wrxfLc6HSQKMqm6GOKjLFw; bk=1; hints={"carousel":{"hasSeen":true},"flip":{"hasSeen":true}}; fid2=flap-a34265ed-349c-4fc3-9ba3-c8ed7c6a1125; sid2=2cd6fbe9-c65b-40a1-87b3-e5c3c5b7a192; flap=i-04df96fe951e0fddc'
}
data = {
    'referer': 'https://flipboard.com/'
}



def dlipBoard(url):

    res = requests.get(url, headers= headers, cookies= cookies, params=data).text
    result = re.findall("\"sourceURL\":\\{([^\\}]*)\\}", res)

    print(result)



if __name__ == '__main__':


    listUrl = 'https://flipboard.com/api/social/commentary?' \
          'oid=flipboard-n4opZhzFQLKhQdXX5nMUJw%3Aa%3A132361178-1555979138' \
          '&oid=flipboard-UNLSaJXRQtmhHLWn4hcB0A%3Aa%3A2150299410-1555981677' \
          '&oid=flipboard-J8AzFxU_SMGkn7TzUqEL1Q%3Aa%3A1444157402-1555983002' \
          '&oid=flipboard-m24Z9iFiTN2AyImDvac-EA%3Aa%3A419161690-1555971290' \
          '&oid=flipboard-Syigb9cQSQWkSbzkXDSPWA%3Aa%3A3199676-1555964690' \
          '&oid=flipboard-36ce9a6882%2Faudioburst.com-1555977328' \
          '&oid=flipboard-BgAY9suvTsC3sYvmM_XzgA%3Aa%3A3195391-1555974801' \
          '&oid=flipboard-NnfPwKeRQC-QHupquuN1Bg%3Aa%3A132361178-1555982467' \
          '&oid=flipboard-7pk-B1gBSq2Somxc_5EBJA%3Aa%3A3199720-1555981380' \
          '&oid=flipboard-s95psk4VSIqaWtBAd5XXSg%3Aa%3A3195391-1555981287' \
          '&oid=flipboard-QxMowojhTFuKPgAyu-MMvw%3Aa%3A132361178-1555983199' \
          '&oid=flipboard-Sf8DZ1fvTgabkaC0BG2QYg%3Aa%3A460011909-1555974600' \
          '&oid=flipboard-J4k_XVXERdG0CgSUA3Tw1w%3Aa%3A132361178-1555967418' \
          '&oid=flipboard-54d586f80c%2Faudioburst.com-1555977254' \
          '&oid=flipboard-a6ac2a3b6e%2Faudioburst.com-1555976481' \
          '&oid=flipboard-4CQSSlJWSCCRn3SV4N04GQ%3Aa%3A3195393-1555964353' \
          '&oid=flipboard-ffc137405d%2Faudioburst.com-1555981817' \
          '&oid=flipboard-402c651555%2Faudioburst.com-1555976007' \
          '&oid=flipboard-74e2bd0845%2Fnytimes.com-1555961978' \
          '&oid=flipboard-b8fac7e7af%2Fcnn.com-1555945461' \
          '&oid=flipboard-RusJK1aKQHWHKvewBZMJfA%3Aa%3A3195428-1555958801' \
          '&oid=flipboard-vAc_M-bxSO6vlssVlbU1FQ%3Aa%3A47769541-1555956360' \
          '&oid=flipboard-a01e6195ba%2Fcnbc.com-1555945332' \
          '&oid=flipboard-Fp4xSZOqR-yMKGdu8zO0vg%3Aa%3A3199563-1555956382' \
          '&oid=flipboard-EPcdhsQsQNWKiL-Jm_MFHw%3Aa%3A3195441-1555963528' \
          '&oid=flipboard-tSkldqcJR3yjt2aaMFrFpQ%3Aa%3A132361178-1555961601' \
          '&oid=flipboard-742dd15c86%2Fnbcnews.com-1555950360' \
          '&oid=flipboard-fb04ac6b22%2Fengadget.com-1555949940' \
          '&oid=flipboard-c6f042c12f%2Fcnbc.com-1555948739' \
          '&oid=flipboard-htiFXZg_SzSklmr7X6KxBw%3Aa%3A80294823-1555963213'


    updateUrl = 'https://flipboard.com/api/users/updateFeed?' \
            'limit=30' \
            '&pageKey=flipboard-htiFXZg_SzSklmr7X6KxBw%3Aa%3A80294823-1555963213' \
            '&sections=flipboard%2Ftopic%252Fnews' \
            '&stream=1'


    dlipBoard(updateUrl)



