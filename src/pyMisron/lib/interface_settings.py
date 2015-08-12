# Copyright (c) 2008 Roi Dayan
# This file is part of the pyGSync project.
# http://pygsync.googlecode.com

import appuifw,e32,socket
app=appuifw.app

from settings import *
from interface_defs import *
import interface

def config_settings():
    try:
        config_settings1()
    except:
        harness(interface.applock,interface.txtLog)

def config_settings1():
    idx=0
    choices=[u'ICQ Logins', u'Alias', u'Default access point',u'Proxy settings']
    while idx!=None:
        tmp=None
        idx=selection_list("Settings",choices)
        if idx==0:
            config_settings_icq_logins()
        elif idx==1:
            tmp=query('Alias:','text',settings['alias'])
            if tmp==None:
                tmp=query('To clear alias?','query')
                if tmp==1:
                    msgbox('Alias cleared.','conf')
                    settings['alias']=None
            else:
                settings['alias']=tmp
        elif idx==2:
            tmp=config_settings_defaccesspoint()
        elif idx==3:
            config_settings_proxy()
        #write configuration if needed
        if tmp!=None:
            write_settings()

class proxy_settings:
    def __init__(self):
        self.choices=[(u'',u'')]
        self.lb=appuifw.Listbox(self.choices,self.callback)
        self.lock=e32.Ao_lock()
        
    def run(self):
        self.refresh()
        app.body=self.lb
        app.title=u"Proxy settings:"
        app.exit_key_handler=self.exit_key_handler
        app.menu=[(u'Back', self.exit_key_handler)]
        self.lock.wait()
        self.lb=None
        
    def refresh(self, idx=0):
        self.choices=[(u'Proxy access point:', unicode(apid_name(settings['proxy_ap']))), (u'Proxy:', unicode(settings['proxy'])),
            (u'Disable',u'Clear proxy access point')]
        self.lb.set_list(self.choices,idx)
        
    def exit_key_handler(self):
        self.lock.signal()
        
    def callback(self, idx=None):
        if idx==None:
            idx=self.lb.current()
        tmp=None
        if idx==0:
            tmp=socket.select_access_point()
            if tmp!=None:
                settings['proxy_ap']=tmp
        elif idx==1:
            tmp=config_settings_setproxy()
            if tmp!=None:
                settings['proxy']=tmp
        elif idx==2:
            settings['proxy_ap']=None
            tmp=1
        if tmp!=None:
            write_settings()
            self.refresh(idx)

def config_settings_proxy():
    proxyset=proxy_settings()
    saved=interface.save_main()
    interface.main_screen(proxyset.lb)
    proxyset.run()
    interface.restore_main(saved)

def config_settings_setproxy():
    lst=[u'IL Orange',u'IL Cellcom',u'Manual']
    idx=listbox(lst,'Set proxy:')
    if idx==0:
        return u'192.118.11.56:8080'
    elif idx==1:
        return u'172.31.29.37:8080'
    elif idx==2:
        tmp=query('Proxy: (ip:port)','text',settings['proxy'])
        return tmp

def config_settings_defaccesspoint():
    lst=[u'Set',u'Clear']
    idx=listbox(lst,'Default access point:')
    tmp=None
    if idx==0:
        tmp=socket.select_access_point()
        if tmp!=None:
            settings['default_ap']=tmp
    elif idx==1:
        settings['default_ap']=None
        tmp=1
    return tmp

def config_settings_icq_logins():
    set=config_icq_logins()
    saved=interface.save_main()
    interface.main_screen(set.lb)
    set.run()
    interface.restore_main(saved)

class config_icq_logins:
    def __init__(self):
        self.choices=[u'Empty']
        self.lb=appuifw.Listbox(self.choices,self.callback)
        self.lock=e32.Ao_lock()
        
    def run(self):
        self.refresh()
        app.body=self.lb
        app.title=u"ICQ Logins:"
        app.exit_key_handler=self.exit_key_handler
        app.menu=[(u'Add login', self.add_login), (u'Back', self.exit_key_handler)]
        self.lock.wait()
        self.lb=None
        
    def refresh(self, idx=0):
        self.choices=settings['icq_logins'].keys()
        self.choices.sort()
        if self.choices==[]:
            self.choices=[u'Empty']
        self.lb.set_list(self.choices,idx)
        
    def exit_key_handler(self):
        self.lock.signal()
        
    def callback(self, idx=None):
        global settings
        if idx==None:
            idx=self.lb.current()
        login=self.choices[idx]
        if login=='Empty':
            return
        tmp=None
        idx2=listbox([u'Set password',u'Delete'],'Action:')
        if idx2==0:
            tmp=query('password for %s:' %login,'code')
            if tmp!=None:
                settings['icq_logins'][login]=tmp
        if idx2==1:
            tmp=query('delete %s ?' %login,'query')
            if tmp==1:
                settings['icq_logins'].__delitem__(login)
            else:
                tmp=None
        if tmp!=None:
            write_settings()
            self.refresh(idx)
    
    def add_login(self):
        global settings
        l=query('ICQ Login:','number')
        if l==None:
            return
        p=query('ICQ Password:','code')
        if p==None:
            return
        settings['icq_logins'][unicode(l)]=p
        write_settings()
        self.refresh()
