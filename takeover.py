#!/usr/bin/env python
# -*- coding: utf-8 -*-
#SubDomain Takeover Scanner by 0x94

import Queue,threading,sys,optparse
queue = Queue.Queue()

try:
    import dns.resolver
except:
    print("Python dns.resolver eklentisi bulunamadi , onu yukledikten sonra calistirin")
    sys.exit(1)




class hazirla:
    def __init__(self,domain,wordlist,thread):
        self.domain=domain
        self.wordlist=wordlist
        self.thread=thread
        
    def thbaslat(self,sublar):
        
        lock    = threading.Lock()
        for subum in sublar:
            if subum.strip():
                queue.put(subum.strip()+"."+self.domain)
                
        threads = []
                
        for i in range(self.thread):
            t = DnsSorgu(queue,lock)
            t.setDaemon(True)
            threads.append(t)
            t.start()
            
        try:
            for x in threads:
                t.join() 
        except KeyboardInterrupt:
            print "Program sona erdi"
            sys.exit(1)        

            
        
    def main(self):
        try:
            dosya  = open(self.wordlist)
        except IOError:
            print "dosya bulunamadi %s" % (self.wordlist)
            sys.exit(0)
        try:
            self.thbaslat(dosya.xreadlines()) 
        except (KeyboardInterrupt,SystemExit):
            self.stop = True
            print "iptal edildi"
            exit()
            
class DnsSorgu(threading.Thread):
    def __init__(self, queue,lock):
        threading.Thread.__init__(self)
        self.queue      = queue
        self.lock       = lock
           
        
        self.firma={"createsend":"https://www.zendesk.com/",
                    "cargocollective":"https://cargocollective.com/",
                    "cloudfront":"https://aws.amazon.com/cloudfront/",
                    "desk.com":"https://www.desk.com/",
                    "fastly.net":"https://www.fastly.com/",
                    "feedpress.me":"https://feed.press/",
                    "freshdesk.com":"https://freshdesk.com/",
                    "ghost.io":"https://ghost.org/",
                    "github.io":"https://pages.github.com/",
                    "helpjuice.com":"https://helpjuice.com/",
                    "helpscoutdocs.com":"https://www.helpscout.net/",
                    "herokudns.com":"https://www.heroku.com/",
                    "herokussl.com":"https://www.heroku.com/",
                    "herokuapp.com":"https://www.heroku.com/",
                    "pageserve.co":"https://instapage.com/",
                    "pingdom.com":"https://www.pingdom.com/",
                    "amazonaws.com":"https://aws.amazon.com/s3/",
                    "myshopify.com":"https://www.shopify.com/",
                    "stspg-customer.com":"https://www.statuspage.io/",
                    "sgizmo.com":"https://www.surveygizmo.com/",
                    "surveygizmo.eu":"https://www.surveygizmo.com//",
                    "sgizmoca.com":"https://www.surveygizmo.com/",
                    "teamwork.com":"https://www.teamwork.com/",
                    "tictail.com":"https://tictail.com/",
                    "domains.tumblr.com":"https://www.tumblr.com/",
                    "unbouncepages.com":"https://unbounce.com/",
                    "uservoice.com":"https://www.uservoice.com/",
                    "wpengine.com":"https://wpengine.com/",
                    "bitbucket":"https://bitbucket.org/",
                    "squarespace.com":"https://www.squarespace.com/",
                    "unbouncepages.com":"https://unbounce.com/",
                    "unbounce.com":"https://unbounce.com/",                    
                    "zendesk.com":"https://www.zendesk.com/"}        
    def run(self):
        while not self.queue.empty(): 
            try:
                gelenq=self.queue.get()
                sys.stdout.write("Taraniyor : "+gelenq + "                                     \r")
                sys.stdout.flush()                
                answers = dns.resolver.query(gelenq, 'CNAME')
                #answers.timeout = 0.2
                #answers.lifetime = 0.10
                for rdata in answers:
                    #self.lock.acquire()
                    print answers.qname,' CNAME:', rdata.target
                    self.takeover(rdata.target,gelenq)
                    #self.lock.release()
            except:
                hata ="hata"
               
            self.queue.task_done() 
                
    def takeover(self,domain,subdomain):
        for firmap in self.firma.keys():
            if firmap in str(domain):
                yollanacak="-- Firma: "+firmap+" Sitesi :"+self.firma[firmap]
                open("takeover.txt","a+").write(subdomain+" --> "+str(domain)+yollanacak+"\n")
                print yollanacak    
   
    

if __name__ == '__main__':
    try:             
        parser = optparse.OptionParser()
        parser.add_option('-d',
            action = "store", 
            dest   = "domain",
            type   = "string", 
            help = "ornek: ./takeover.py -d host.com")
        parser.add_option('-w',
            action = "store", 
            dest   = "wordlist",
            type   = "string", 
            help = "ornek: ./takeover.py -d host.com -w wordlist.txt ")  
        parser.add_option('-t',
            action = "store", 
            dest   = "thread",
            type   = "int", 
            help = "ornek: ./takeover.py -d host.com -w wordlist.txt  -t 10")        
        (option,args) = parser.parse_args()
        if not option.domain:
            print "domain girmedin"
            print "ornek: ./takeover.py -d host.com -w wordlist.txt  -t 10" 
            sys.exit(0)   
            
        if not option.wordlist:
            print "wordlist girmedin"
            print "ornek: ./takeover.py -d host.com -w wordlist.txt" 
            sys.exit(0)  
            
        if option.thread:
            threadsayisi=option.thread
        else:
            threadsayisi=20
            
        print"""
        #######################################################
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #              SubDomain TakeOver v1.0                #
        #                    Coder: 0x94                      #
        #                  twitter.com/0x94                   #
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #######################################################  
        """          
        x=hazirla(option.domain,option.wordlist,threadsayisi)
        x.main()    
    except KeyboardInterrupt:
        print('\n Bir tusa basildi.')
        sys.exit(0)
