import time
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
        sess.render('transfers.png')
        age_min = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ddlAgeMin')
        age_min.set('17')
        time.sleep(2)
        sess.render('transfers_min_age.png')
        age_max = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ddlAgeMax')
        age_max.set('18')
        skill_name = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ddlSkill1')
        skill_name.set('1')
        skill_min = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ddlSkill1Min')
        skill_min.set('6')
        skill_max = sess.at_css('#ctl00_ctl00_CPContent_CPMain_ddlSkill1Max')
        skill_max.set('9')
        sess.render('transfer_form_filled.png')
        search_button = sess.at_css('#ctl00_ctl00_CPContent_CPMain_butSearch')
        search_button.click()
        time.sleep(2)
        sess.render('transfer_results.png')


if __name__ == '__main__':
    hts = HTScrape()
    sess = hts.create_session()
    hts.login(sess)
    hts.go_to_trandfers(sess)



