# SMTP RCPT probe (no DATA, no message sent). Runs in remote sandbox with port 25 open.
import socket, json, sys, random, string, time, urllib.request
FROM = 'verify@starrsystems.co'
HELO = 'mail.starrsystems.co'
def mx(domain):
    try:
        r = json.load(urllib.request.urlopen(f'https://dns.google/resolve?name={domain}&type=MX', timeout=10))
        a = sorted([(int(x['data'].split()[0]), x['data'].split()[1].rstrip('.')) for x in r.get('Answer', []) if x['type']==15])
        return [h for _, h in a]
    except Exception as e:
        return []
def rd(f):
    lines=[]
    while True:
        l=f.readline().decode('latin1')
        if not l: break
        lines.append(l.rstrip())
        if len(l)<4 or l[3]!='-': break
    return lines
def cmd(s,f,c):
    s.sendall((c+'\r\n').encode()); return rd(f)
def probe(email):
    dom = email.split('@')[1]
    hosts = mx(dom)
    res = {'email':email,'mx':hosts[:2]}
    if not hosts: res['status']='no_mx'; return res
    fake = ''.join(random.choices(string.ascii_lowercase,k=12))+'@'+dom
    for h in hosts[:2]:
        try:
            s=socket.create_connection((h,25),timeout=15); s.settimeout(20); f=s.makefile('rb')
            ban=rd(f)
            if not ban or not ban[0].startswith('220'): res['banner']=ban[:1]; s.close(); continue
            e=cmd(s,f,'EHLO '+HELO)
            m=cmd(s,f,'MAIL FROM:<'+FROM+'>')
            if not m or not m[0].startswith('250'):
                res['status']='mailfrom_rejected'; res['detail']=m[:1]; s.close(); continue
            r1=cmd(s,f,'RCPT TO:<'+email+'>')
            res['rcpt']=r1[:1]
            r2=cmd(s,f,'RSET'); m2=cmd(s,f,'MAIL FROM:<'+FROM+'>')
            r3=cmd(s,f,'RCPT TO:<'+fake+'>')
            res['fake']=r3[:1]
            cmd(s,f,'QUIT'); s.close()
            c1=r1[0][:3] if r1 else ''; c3=r3[0][:3] if r3 else ''
            if c1.startswith('250'):
                res['status']='catch_all' if c3.startswith('250') else ('deliverable' if c3.startswith('5') else 'accepted_fake_unclear')
            elif c1.startswith('5'): res['status']='rejected_5xx'
            else: res['status']='temp_or_unknown'
            res['host']=h
            return res
        except Exception as ex:
            res['err']=str(ex)[:100]
    res.setdefault('status','unreachable')
    return res
if __name__=='__main__':
    emails=sys.argv[1:]
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(8) as ex: out=list(ex.map(probe,emails))
    print(json.dumps(out,indent=0))
