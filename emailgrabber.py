import requests
from base64 import b64decode

def get_email_from_cookie(cookie):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

    ## Custom request function to avoid bandwith waste caused by requesting
    ## error pages and what not
    def request(url):
        resp = requests.get(
            url=url,
            headers={"User-Agent": user_agent},
            cookies={".ROBLOSECURITY": cookie},
            allow_redirects=False)
        new_url = resp.headers.get("location")
        
        ## Do an exception on allow_redirects for 13> redirects
        if new_url and "web." in new_url:
            resp, new_url = request(new_url)
        
        return resp, new_url
        
    ## Devforum -> Roblox SSO
    resp, new_url = request("https://devforum.roblox.com/session/sso?return_path=%2F")
    if not new_url or not "/discourse/dev-forum?sso=" in new_url:
        return
    
    ## Devforum <- Roblox SSO
    resp, new_url = request(new_url)
    if not new_url or not "/session/sso_login?sso=" in new_url:
        return
    
    ## Grab base64-encoded SSO data and decode it
    data = new_url.split("/session/sso_login?sso=")[1].split("&")[0].replace("%3D", "=")
    data = b64decode(data.encode("utf-8")).decode("utf-8")
    
    ## Grab email param and URL-decode it
    email = data.split("email=")[1].split("&")[0]
    email = email.replace("%40", "@").replace("%2b", "+")
    
    return email


if __name__ == "__main__":
    cookie = input("Enter your cookie >> ")
    email = get_email_from_cookie(cookie)
    
    if not email:
        print("No email found, possibly unverified/banned?")
        input()
    
    print("Email:", email)
    input()