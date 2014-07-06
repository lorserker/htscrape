import time
import datetime
import os
import os.path
import dryscrape
import settings

class HTScrape(object):

    def __init__(self):
        pass

    def create_session(self):
        sess = dryscrape.Session(base_url='http://www.hattrick.org/')
        return sess

    def login(self, sess):
        sess.visit('/')
        user_field = sess.at_css('#txtUserName')
        password_field = sess.at_css('#txtPassword')
        user_field.set(settings.USERNAME)
        password_field.set(settings.PASSWORD)
        login_button = sess.at_css('#butLogin')
        login_button.click()
        sess.render('logged_in_home.png')

    def go_to_trandfers(self, sess):
        world_menu = sess.at_xpath('//a[@href="/World/"]')
        world_menu.click()
        transfer_menu = sess.at_xpath('//a[@href="Transfers/"]')
        transfer_menu.click()
        
    def search_transfers(self, sess, search_criteria, result_dir):
        search_criteria.fillout_form(sess)
        sess.render('filled_out.png')
        search_button = sess.at_css('#ctl00_ctl00_CPContent_CPMain_butSearch')
        search_button.click()
        now = datetime.datetime.utcnow()
        sess.render('transfer_results_0.png')
        fout = open(os.path.join(result_dir, now.strftime('%Y_%m_%d_%H_%M_%S_transfer_results_0.html')), 'w')
        fout.write(sess.body())
        fout.close()
        page_1 = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ucPager_repPages_ctl01_p1')
        if page_1:
            page_1.click()
            #sess.render('transfer_results_1.png')
            fout = open(os.path.join(result_dir, now.strftime('%Y_%m_%d_%H_%M_%S_transfer_results_1.html')), 'w')
            fout.write(sess.body())
            fout.close()
        page_2 = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ucPager_repPages_ctl02_p2')
        if page_2:
            page_2.click()
            #sess.render('transfer_results_2.png')
            fout = open(os.path.join(result_dir, now.strftime('%Y_%m_%d_%H_%M_%S_transfer_results_2.html')), 'w')
            fout.write(sess.body())
            fout.close()
        page_3 = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ucPager_repPages_ctl03_p3')
        if page_3:
            page_3.click()
            #sess.render('transfer_results_3.png')
            fout = open(os.path.join(result_dir, now.strftime('%Y_%m_%d_%H_%M_%S_transfer_results_3.html')), 'w')
            fout.write(sess.body())
            fout.close()


class SearchCriteria(object):

    def __init__(self, age_min=None, age_max=None, skill_name='-1', skill_min='-1', skill_max='-1'):
        self.age_min = str(age_min) if age_min else None
        self.age_max = str(age_max) if age_max else None
        self.skill_name = str(skill_name) if skill_name else None
        self.skill_min = str(skill_min) if skill_min else None
        self.skill_max = str(skill_max) if skill_max else None

    def fillout_form(self, sess):
        if self.age_min:
            age_min_select = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ddlAgeMin')
            age_min_select.set(self.age_min)
        if self.age_max:
            age_max_select = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ddlAgeMax')
            age_max_select.set(self.age_max)
        if self.skill_name and self.skill_name != '-1':
            skill_select = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ddlSkill1')
            skill_select.set(self.skill_name)
        if self.skill_min and self.skill_min != '-1':
            skill_min_select = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ddlSkill1Min')
            skill_min_select.set(self.skill_min)
        if self.skill_max and self.skill_max != '-1':
            skill_max_select = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ddlSkill1Max')
            skill_max_select.set(self.skill_max)

skills = [None, 'keeper', None, 'defending', 'playmaking', 'winger', 'scoring', 'passing', 'setpieces']
agegroups = [(17, 18), (19, 21), (22, 28), (29, 99)]
skill_levels = [(6, 9), (10, 13), (14, 17)]

if __name__ == '__main__':
    hts = HTScrape()
    sess = hts.create_session()
    hts.login(sess)
    hts.go_to_trandfers(sess)
    for skill_ix, skill_name in enumerate(skills):
        if skill_name is None:
            continue
        print skill_name
        for age_min, age_max in agegroups:
            print 'age in [%d, %d]' % (age_min, age_max)
            for skill_min, skill_max in skill_levels:
                print 'level in [%d, %d]' % (skill_min, skill_max)
                hts.go_to_trandfers(sess)
                result_dir = os.path.join('..', 'results_%s_age_%d_%d_level_%d_%d' % (skill_name, age_min, age_max, skill_min, skill_max))
                search_criteria = SearchCriteria(age_min, age_max, skill_ix, skill_min, skill_max)
                try:
                    os.mkdir(result_dir)
                except:
                    pass
                hts.search_transfers(sess, search_criteria, result_dir)
                print '.'



