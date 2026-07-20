#!/usr/bin/env python3
import json, os, re, sys, urllib.parse, urllib.request
from pathlib import Path

README = Path('README.md')
REPOS = (
 'Yoddikko/kasetPlus','Yoddikko/terminal_portfolio','Yoddikko/GulliverWeb',
 'Yoddikko/yoddChatGPT','Yoddikko/TokenMaxxxxing-Claude-Code-X-Deepseek',
 'Yoddikko/GetGyroAndAccelerometerData','Yoddikko/ianygo-trial-reset',
 'Yoddikko/Now','Yoddikko/ASL-Recognizer',
 'Yoddikko/Be-Charge-Host-Hackaton2022','Yoddikko/DropDown',
)
ORGS = ('Automercatorum','AirBook-for-CrossPoint')
IANYGO_ROW = '''  <tr>
    <td width="72" align="center">
      <img src="https://github.com/user-attachments/assets/832c6a8f-f6b1-4332-aa59-f1048f064a34" width="48" alt="iAnyGo Trial Reset icon">
    </td>
    <td>
      <a href="https://github.com/Yoddikko/ianygo-trial-reset"><strong>iAnyGo Trial Reset</strong></a>&nbsp;&nbsp;&nbsp;<!-- repo-stats:Yoddikko/ianygo-trial-reset:start --><!-- repo-stats:Yoddikko/ianygo-trial-reset:end --><br>
      A macOS utility that resets and patches the iAnyGo v4.11.8 trial for research and educational use.<br>
      <sub>Shell · Swift · Python · macOS</sub>
    </td>
  </tr>
'''

def api(url, token):
 req=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','Authorization':f'Bearer {token}','User-Agent':'Yoddikko-profile-stats','X-GitHub-Api-Version':'2022-11-28'})
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)

def repo_totals(name, token):
 d=api(f'https://api.github.com/repos/{name}',token)
 return int(d.get('stargazers_count',0)),int(d.get('forks_count',0))

def org_totals(name, token):
 s=f=0;p=1
 while True:
  q=urllib.parse.urlencode({'type':'public','per_page':100,'page':p})
  rows=api(f'https://api.github.com/orgs/{name}/repos?{q}',token)
  if not rows:break
  s+=sum(int(x.get('stargazers_count',0)) for x in rows)
  f+=sum(int(x.get('forks_count',0)) for x in rows)
  if len(rows)<100:break
  p+=1
 return s,f

def render(stars,forks):
 out=[]
 if stars:
  out.append(f'<span title="{stars} {"star" if stars==1 else "stars"}"><img src="https://api.iconify.design/octicon:star-16.svg?color=%23F1C40F" width="16" height="16" alt="Stars">&nbsp;<strong>{stars}</strong></span>')
 if forks:
  out.append(f'<span title="{forks} {"fork" if forks==1 else "forks"}"><img src="https://api.iconify.design/octicon:repo-forked-16.svg?color=%238B949E" width="16" height="16" alt="Forks">&nbsp;<strong>{forks}</strong></span>')
 return '&nbsp;&nbsp;&nbsp;'.join(out)

def update_block(text,key,url,value):
 start=f'<!-- repo-stats:{key}:start -->';end=f'<!-- repo-stats:{key}:end -->'
 replacement=start+value+end
 text,count=re.subn(re.escape(start)+r'.*?'+re.escape(end),replacement,text,flags=re.S)
 if count==1:return text
 link=re.compile(rf'(<a href="{re.escape(url)}"><strong>.*?</strong></a>)')
 text,count=link.subn(rf'\1&nbsp;&nbsp;&nbsp;{replacement}',text,count=1)
 if count!=1:raise RuntimeError(f'Could not find README link for {key}')
 return text

def ensure_ianygo(text):
 if 'https://github.com/Yoddikko/ianygo-trial-reset' in text:return text
 tools=text.index('  Tools\n</h3>')
 table_end=text.index('</table>',tools)
 return text[:table_end]+IANYGO_ROW+text[table_end:]

def main():
 token=os.environ.get('GITHUB_TOKEN','').strip()
 if not token:return 1
 old=README.read_text(encoding='utf-8');new=ensure_ianygo(old)
 for name in REPOS:
  s,f=repo_totals(name,token);new=update_block(new,name,f'https://github.com/{name}',render(s,f))
 for name in ORGS:
  s,f=org_totals(name,token);new=update_block(new,name,f'https://github.com/{name}',render(s,f))
 if new!=old:README.write_text(new,encoding='utf-8')
 return 0

if __name__=='__main__':sys.exit(main())
