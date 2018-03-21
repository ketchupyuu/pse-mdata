#!/usr/bin/python
import os,sys
import re
import bs4
sys.path.append(os.path.join(os.getcwd(),'modules'))
from PseScraper import PseScraper

class PseWebsite():

    def __init__(self):
        self.edge_base_url = 'http://edge.pse.com.ph/'
        self.scrap   = PseScraper()
        self.curr_dir   = os.getcwd()
        self.out_dir    = 'out'

    def get_comp_page_links(self):
        """
        Get company page urls from stock directory page
        """
            
        self.comp_page_form_list   = []
        cmpy_id_dict    = {}

        for page_num in range(1,10):

            stock_dir  = 'companyDirectory/search.ax'
            stock_dir_form    ='?cmpySortType=ASC&companyId=&dateSortType=DESC&keyword=&pageNo=%s&sector=ALL&sortType=&subsector=ALL&symbolSortType=ASC' % page_num
            url = self.edge_base_url + stock_dir + stock_dir_form
            cm_detail_regex = re.compile('(?<=cmDetail\(\')(.*)(?=\')')

            """
            WORKING BLOCK - using html_res
            """
            html_res    = self.scrap.get_html_response(url)
            for line in html_res.split("\n"):
                cm_detail   = cm_detail_regex.search(line)
                if cm_detail:
                    #DEBUG
                    cmpy_id,security_id = cm_detail.group().split("','")
                    #comp_page_form   = 'companyPage/stockData.do?cmpy_id=%s&security_id=%s' % (cmpy_id,security_id)
                    #security_id = security_id.replace("'","")
                    #cmpy_id     = cmpy_id.replace("'","")
                    if cmpy_id in ('370','237'):
                        print line
                    try:
                       #self.comp_page_form_list.append(comp_page_form)
                        if cmpy_id not in cmpy_id_dict:
                            cmpy_id_dict[cmpy_id] = security_id
                    except Exception as e:
                        #print 'ERROR: %s' % e.message
                        #print 'LEN OF LIST: %s' % len(self.comp_page_form_list)
                        #print 'COMP_PAGE_URL: %s' % comp_page_form
                        sys.exit(1)
            """
            END OF BLOCK
            """

            """
            WORKING BLOCK - writing html file
            """
            # FOR DEBUGGING HTML RES
            #html_dump   = os.path.join(self.curr_dir,self.out_dir,'dump.html')
            #self.scrap.download_from_url(url,html_dump)
            #with open(html_dump,'rw') as f:
            #    for line in f:
            #        cm_detail   = cm_detail_regex.search(line)
            #        if cm_detail:
            #            #DEBUG
            #            #print cm_detail.group()
            #            cmpy_id,security_id = cm_detail.group().split(',')
            #            comp_page_form   = 'companyPage/stockData.do?cmpy_id=%s&security_id=%s' % (cmpy_id,security_id)
            #            security_id = security_id.replace("'","")
            #            #print "security_id: %s" % security_id.replace("'","")
            #            try:
            #               self.comp_page_form_list.append(comp_page_form)
            #            except:
            #                print 'TYPE OF COMP_PAGE_URL: %s' % type(comp_page_form)
            #                print 'TYPE OF LIST: %s' % type(self.comp_page_form_list)
            #                print 'LEN OF LIST: %s' % len(self.comp_page_form_list)
            #                print 'COMP_PAGE_URL: %s' % comp_page_form
            #                sys.exit(1)
            """
            END OF BLOCK
            """

        print len(cmpy_id_dict.keys())
        self.cmpy_id_dict   = cmpy_id_dict
        #for cmpy_id,sec_id in cmpy_id_dict.iteritems():
        #    print "cmpy: %s sec: %s" % (cmpy_id,sec_id)
        
    def get_comp_names(self):
        for cmpy_id,sec_id in self.cmpy_id_dict.iteritems():
            #print "cmpy: %s sec: %s" % (cmpy_id,sec_id)
            comp_page_form   = 'companyPage/stockData.do?cmpy_id=%s&security_id=%s' % (cmpy_id,sec_id)
            comp_page_url    = self.edge_base_url + comp_page_form
            html_res    = self.scrap.get_html_response(comp_page_url)
            soup = bs4.BeautifulSoup(html_res,'lxml')
            #for name in soup.find_all('div',{'class': "compInfo"}):
            #    text = name.get_text().lstrip('\n').rstrip('\n')
            #    print "Company name is: %s" % text
            #    #print "End here"

            name = soup.find('div',{'class': "compInfo"}).contents[1].get_text()
            #print name


            comp_info_fields = ['Status','Issue Type','ISIN','Listing Date','Board Lot','Par Value','Market Capitalization','Outstanding Shares','Listed Shares','Issued Shares', 'Free Float Level(%)','Foreign Ownership Limit(%)']
            comp_info_str = cmpy_id + "|" + sec_id + "|" + name

            comp_info_fields = [
                'Last Traded Price',
                'Value',
                'Volume',
                'Open',
                'High',
                'Low',
                'Average Price',
                '52-Week High',
                '52-Week Low',
                'Previous Close and Date',
                #'P/E Ratio',                # Blank
                #'Sector P/E Ratio',         # Blank
                #'Book Value',               # Blank
                #'P/BV Ratio',               # Blank
                'Status',
                'ISIN',
                'Listing Date',
                'Board Lot',
                'Par Value',
                ]

            for field in comp_info_fields:
                text = soup.find('th',text=field).find_next_sibling('td').get_text()
                if field == 'Previous Close and Date':
                        text = text.split()[0]
                #text = text.lstrip('\n').rstrip('\n')   # Remove newline and padding
                text = text.lstrip().rstrip()
                #text = text.replace('\n','')
                comp_info_str += text + "|"

            print comp_info_str
                
            #text = name.lstrip('\n').rstrip('\n')
            #print "Company name is: %s" % text
            #print "End here"

def main():
    pse =   PseWebsite()
    pse.get_comp_page_links()
    pse.get_comp_names()


if __name__ == "__main__":
    main()
