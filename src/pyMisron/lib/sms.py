# Copyright (c) 2008 Roi Dayan
# This file is part of the pyMisron project.
# http://pymisron.googlecode.com

import appuifw
import e32

from settings import *
from interface import *
from httpUrl import *
alef=1488
taf=1514

def go_sms():
    if settings['icq_logins']=={}:
        msg("You must set icq logins first.",'red')
        return
    icq=chooseICQlogin()
    if icq==None:
        return
    lst=[u'Contact',u'Other']
    idx=listbox(lst,'Select:')
    if idx==None:
        return
    if idx==0:
        tr=chooseContact()
        if tr==None:
            return
        #appuifw.note(unicode(tr))
        pn=tr[1]
    else:
        pn=appuifw.query(u'Phone:','number')
        if pn==None:
            return
        pn=u'0'+str(pn)
    #saved=save_main()
    #choose=chooseContact()
    #choose.run()
    #restore_main(saved)
    #tr=choose.target
    #m=appuifw.query(u'Short message:','text')
    m=get_text()
    if m==None:
        return
    go_sms1(icq,pn,m)

def go_sms1(icq, target, message):
    import urllib, urlparse, re
    span=re.compile('<span class="([a-zA-Z]+)span">([^<]+)</span>')
    msg('ICQ: %s' %icq[0])
    msg('Target: %s' %target)
    m=message
    
    o=ord(message[1])
    if o>=alef and o<=taf:
        m=reverse(message)
    else:
        m=message
    
    a=settings['alias']
    if a!=None:
        message='(%s)\n%s' %(a,message)
        m='(%s)\n%s' %(a,m)
    
    msg('Message:')
    for i in m.splitlines():
        msg(i)
    msg('-----')

    apo=set_access_point()
    if apo==None:
        msg('User aborted.')
        return
    params={'posted':1,'uin':icq[0],'uin_password':icq[1].encode('utf-8'),
            'number':target,'smstext':message.encode('utf-8')}
    params = urllib.urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    parts = urlparse.urlsplit(settings['icq_gateway'])
    url=parts[1]
    req=parts[2]
    #if parts[0] == https use httpsUrl()
    try:
        conn = httpUrl(url,'POST',req,params,headers)
    except:
        harness()
        return
    response = conn.getresponse()
    status = response.status
    body = response.read()
    conn.close()
    apo.stop()
    log(unicode(str(status)))
    if status==502:
        msg('Connection error')
        return
    if status!=200:
        msg('Error gateway status: %s' %status, 'red')
        return
    #write_log(body)
    body=body.decode('utf-8','ignore')
    m=None
    for line in body.splitlines():
        if m==None:
            m=span.match(line)
            if m!=None:
                m=m.groups()
    if m==None:
        msg('icq_gateway error.','red')
        return
    msg(m[0])
    o=ord(m[1][1])
    if o>=alef and o<=taf:
        msg(reverse(m[1]))
    else:
        msg(m[1])
    return status


#def write_log(this=None):
#    import sys
#    import traceback
#    try:
#        f = open('pym_tr.txt','wt')
#        #f = codecs.open(my_config, 'w', 'utf-8')
#        #this=unicode('\n'.join(traceback.format_exception(*sys.exc_info())))
#        f.write(this)
#        f.close()
#    except:
#        raise Exception, "Error writing log file"


def makeConList():
        import contacts
        global contactIDS
        contactIDS={}
        target=None
        con=contacts.open()
        heb=[]
        abc=[]
        did=[]
        #self.lb=appuifw.Listbox([(u'',u'')],self.callback)
        for i in con.keys():
            if con[i].is_group==0:
                t=con[i].title
                p=gotPhone(con[i])
                if p!=None:
                    if t==None or t=='':
                        log('something is wrong with phone: %s' %p)
                    else:
                        #log('title: %s' %t)
                        l=t[0]
                        if not did.__contains__(t):
                            o=ord(l)
                            if o>=alef and o<=taf:
                                heb.append(t)
                            else:
                                abc.append(t)
                            did.append(t)
                            contactIDS[t]=con[i]
        heb.sort()
        abc.sort()
        for i in abc:
            heb.append(i)
        return heb

def chooseContact():
    global contactIDS
    list=makeConList()
    idx=selection_list('Choose contact:', list, 1)
    if idx==None:
        return None
    target=list[idx]
    con=contactIDS[target]
    phones=getPhones(con)
    idx2=listbox(phones,'Choose phone:')
    if idx2==None:
        return None
    phone=phones[idx2]
    return [target,phone]

def gotPhone(con):
    p=con.find('mobile_number')
    if len(p)>0:
        v=p[0].value
        vs=str(v)
        if v!=None and len(v)>=10:
            return v
    return None

def getPhones(con):
    p=con.find('mobile_number')
    phones=[]
    for i in p:
        v=i.value
        vs=str(v)
        if v!=None and len(vs)>=10:
            v=remAreaCode(vs)
            phones.append(unicode(vs))
    if phones==[]:
        return None
    return phones

def remAreaCode(phone):
        if phone[0]=='+':
            phone=u'0'+phone[4:]
        return phone

class chooseContact1:
    def __init__(self):
        self.makeList()
    
    def makeList(self):
        self.target=None
        self.con=contacts.open()
        alef=1488
        taf=1514
        heb=[]
        abc=[]
        did=[]
        self.lb=appuifw.Listbox([(u'',u'')],self.callback)
        for i in self.con.keys():
            if self.con[i].is_group==0:
                t=self.con[i].title
                p=self.getPhone(self.con[i])
                if p!=None:
                    ad=(t,p)
                    l=t[0]
                    if not did.__contains__(t):
                        o=ord(l)
                        if o>=alef and o<=taf:
                            heb.append(ad)
                        else:
                            abc.append(ad)
                        did.append(t)
        heb.sort()
        abc.sort()
        for i in abc:
            heb.append(i)
        self.list=heb
        self.lock=e32.Ao_lock()
    
    def run(self):
        self.refresh()
        self.lock.wait()
    
    def quit(self):
        self.lock.signal()
    
    def refresh(self):
        self.lb.set_list(self.list)
        appuifw.app.body=self.lb
        appuifw.app.exit_key_handler=self.quit
    
    def remAreaCode(self, phone):
        if phone[0]=='+':
            phone=u'0'+phone[4:]
        return phone
    
    def getPhone(self,con):
        p=con.find('mobile_number')
        if p.__len__()>0:
            v=str(p[0].value)
            if v!=None and len(v)>=10:
                v=self.remAreaCode(v)
                return unicode(v)
        return None
    
    def callback(self, idx=None):
        if (idx==None):
            idx=self.lb.current()
        c=self.list[idx]
        self.target=c
        self.quit()
"""
class queryText:
    def __init__(self):
        self.box=appuifw.Text()
        self.box.clear()
        self.lock=e32.Ao_lock()
    
    def run(self):
        self.refresh()
        self.lock.wait()
    
    def quit(self):
        self.lock.signal()
    
    def refresh(self):
        appuifw.app.body=self.box
        appuifw.app.exit_key_handler=self.quit

    def callback(self, idx=None):
        if (idx==None):
            idx=self.lb.current()
        c=self.list[idx]
"""

def chooseICQlogin():
    list=settings['icq_logins'].keys()
    list.sort()
    idx=selection_list('Choose ICQ login:', list, 0)
    if idx==None:
        return None
    l=list[idx]
    p=settings['icq_logins'][l]
    return [l,p]
