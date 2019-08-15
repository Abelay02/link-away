def index2url(ind):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    returl = ""
    
    while ind != 0:
        curr = ind%62
        returl = chars[curr] + returl
        ind = ind/62
    return returl

def url2index(url):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    ind = 0
    for i in range(len(url)):
        ind += 62**(len(url)-i-1) * chars.find(url[i])
    return ind

# inspired by https://www.geeksforgeeks.org/how-to-design-a-tiny-url-or-url-shortener/