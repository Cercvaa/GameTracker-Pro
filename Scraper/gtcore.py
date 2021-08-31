import discord,asyncio,requests,bs4,re,tabulate
from tabulate import tabulate
from bs4 import BeautifulSoup


class GTcore():
    def __init__(self, ip):
        self.ip = ip
        self.page = requests.get("https://www.gametracker.com/server_info/" + self.ip)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

    def banner(self):
        image = self.soup.find("img", class_="item_560x95")
        return image['src']

    def map(self):
        map_text = self.soup.find('div', class_="si_map_header").text.strip()

        return map_text

    def mapimage(self):

        image = self.soup.find("img", class_="item_160x120")
        return image['src']

    def maps(self):

        g = list()
        for image in self.soup.find_all("img", class_="item_260x170"):
            g.append(image['src'])

        return g[1]

    def rank_image(self):

        g = list()
        for image in self.soup.find_all("img", class_="item_260x170"):
            g.append(image['src'])

        return g[2]

    def name(self):
        try:
            h = self.soup.find("span", class_="blocknewheadertitle").text.strip()

            return h
        except AttributeError:
            return "--"

    def players(self):
        spans = list()
        for span in self.soup.find_all("span", id = True):
            spans.append(span.text)

        players = spans[0]
        return players

    def rank(self):
        try:
            ranks = list()
            ranks1 = self.soup.find_all("span", class_="item_color_title")
            for rank in ranks1:
                rank = rank.next_sibling
                ranks.append(rank.strip())

            rank_finnaly = ''
            text = ranks[7]
            text1 = text.replace('(', '')

            text2 = ranks[12]
            text2_ = text2.replace('(', '')
            if len(text1) > len(text2_):
                rank_finnaly = text1
            else:
                rank_finnaly = text2_

            return rank_finnaly
        except AttributeError:
            return "--"

    def status(self):
        try:
            status = self.soup.find("span", class_="item_color_success").text.strip()
            if status == "Alive" : statusi = "🟢 **Active**"
            else: statusi = "🔴 **Offline**"
            return statusi
        except AttributeError:
            return "--"


    def playersrefresher(self):
        pl = list()
        for player in self.soup.find_all("a", href = re.compile("^/player")):
            pl.append(player.text.strip())

        table = self.soup.find("table", class_="table_lst table_lst_stp")
        
        scores = list()
        rows = table.find_all("tr")
        for tr in rows:
            td = tr.find_all("td")[2]
            scores.append(td.text.strip())
        scores.pop(0)

        time_played = list()
        rows = table.find_all("tr")
        for tr in rows:
            td = tr.find_all("td")[3]
            time_played.append(td.text.strip())
        time_played.pop(0)

        headers = ["Name", "Score", "Time Played"]
        make_table = zip(pl, scores, time_played)
        return tabulate(make_table, headers = headers)