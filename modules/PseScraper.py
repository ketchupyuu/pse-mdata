import urllib2


class PseScraper:
    def init(self):
        pass

    def get_html_response(self,url):
        try:
            req = urllib2.Request(url)
            req.add_header('Cache-Control','max-age=0')
            content = urllib2.urlopen(req)
            html    = content.read()
            #print "content:",content
            #print "html:",html
        except urllib2.HTTPError as e:
            print('HTTP Error:', e.code,url)
        except urllib2.URLError as e:
            print('URL Error:',e.code,url)
        return html

    def download_from_url(self,dl_url,file_path):
        content = self.get_html_response(dl_url)
        try:
            with open(file_path,"wb") as targ_file:
                targ_file.write(content)
            print("Content downloaded to %s" % file_path)
        except IOError as e:
            print('Could not write to file [%s] % file_path')
            print('ERROR:',e.errorno,e.strerror) 
